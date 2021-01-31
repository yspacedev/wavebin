"""
wavebin
https://github.com/sam210723/wavebin

Waveform capture viewer for Keysight oscilloscopes.
"""

from collections import namedtuple
import numpy as np
from pathlib import Path
import struct

class WaveParser():
    def __init__(self, config):
        self.config = config


    def parse(self, path):
        self.config['file'] = Path(path)

        # Open capture file
        print(f"Opening \"{self.config['file'].name}\"")
        self.log(f"Full path \"{self.config['file']}\"\n")
        self.file = open(self.config['file'], mode="rb")

        # Parse file header
        if not self.parse_file_header(self.file.read(0x0C)):
            return False
        
        # Loop through waveforms
        self.waveforms = []
        for i in range(self.file_header.waveforms):
            self.log(f"Waveform {i + 1}:")

            # Parse waveform header
            header = self.parse_waveform_header()

            # Parse waveform data header
            data = self.parse_waveform_data()

            # Add waveform to global list
            self.waveforms.append({
                "header": header,
                "data":   data
            })

            # Print waveform info
            p = self.waveforms[i]['header'].points
            self.log(f"  - Sample Points:  {self.human_format(p)}")
            sr = round(1 / self.waveforms[i]['header'].x_increment)
            self.log(f"  - Sample Rate:    {sr / 1e9} Gsps")
            self.log(f"  - Device Model:   {self.waveforms[i]['header'].frame.decode().split(':')[0]}")
            self.log(f"  - Device Serial:  {self.waveforms[i]['header'].frame.decode().split(':')[1]}\n")

        self.file.close()

        # Update UI elements
        self.config['app'].config['file'] = self.config['file']
        self.config['app'].update()
        self.config['plot'].update()

        return True


    def parse_file_header(self, data):
        # Unpack file header
        file_header_tuple = namedtuple(
            "FileHeader",
            "magic version size waveforms"
        )
        fields = struct.unpack("2s2s2i", data)
        self.file_header = file_header_tuple(*fields)

        # Check file magic
        if self.file_header.magic != b'AG':
            print("Unknown file format")
            return False

        # Print file header info
        self.log("File Header:")
        self.log(f"  - Waveforms: {self.file_header.waveforms}")
        self.log(f"  - File Size: {self.human_format(self.file_header.size, binary=True)}B\n")

        return True


    def parse_waveform_header(self):
        # Read data from file
        length = int.from_bytes(self.file.read(1), byteorder="little")
        data = bytes([length]) + self.file.read(length - 1)

        # Unpack waveform header
        waveform_header_tuple = namedtuple(
            "WaveformHeader",
            "size wave_type buffers points average "\
            "x_d_range x_d_origin x_increment x_origin "\
            "x_units y_units date time frame label "\
            "time_tags segment"
        )
        fields = struct.unpack("5if3d2i16s16s24s16sdI", data)
        header = waveform_header_tuple(*fields)

        return header


    def parse_waveform_data(self):
        header = self.parse_waveform_data_header()
        data = self.file.read(header.length)

        # Get waveform data type
        if header.data_type in [1, 2, 3]:
            data_type = np.float32
        elif header.data_type == 6:
            data_type = np.uint8
        else:
            data_type = np.float32

        # Parse buffer into numpy array
        arr = np.frombuffer(data, dtype=data_type)

        return arr


    def parse_waveform_data_header(self):
        # Read data from file
        length = int.from_bytes(self.file.read(1), byteorder="little")
        data = bytes([length]) + self.file.read(length - 1)

        # Unpack waveform data header
        waveform_data_header_tuple = namedtuple(
            "WaveformDataHeader",
            "size data_type bpp length"
        )
        fields = struct.unpack("i2hi", data)
        
        return waveform_data_header_tuple(*fields)


    def ui(self, app, plot):
        self.config['app'] = app
        self.config['plot'] = plot


    def human_format(self, num, binary=False):
        if binary:
            div = 1024.0
        else:
            div = 1000.0
        
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= div:
            magnitude += 1
            num /= div
        return '{}{}'.format('{:f}'.format(round(num, 2)).rstrip('0').rstrip('.'), ['', 'k', 'M', 'G', 'T'][magnitude])


    def log(self, msg):
        if self.config['verbose']: print(msg)

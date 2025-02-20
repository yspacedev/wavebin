# <img src="https://raw.githubusercontent.com/sam210723/wavebin/master/icon.ico" width=24 /> Oscilloscope Waveform Capture Viewer

[![GitHub release](https://img.shields.io/github/release/sam210723/wavebin.svg)](https://pypi.org/project/wavebin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wavebin)](https://pypi.org/project/wavebin/)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/wavebin)](https://pypi.org/project/wavebin/)
[![GitHub license](https://img.shields.io/github/license/sam210723/wavebin.svg)](https://github.com/sam210723/wavebin/master/LICENSE)

**wavebin** reads binary capture files generated by Agilent, Keysight and Rigol oscilloscopes and renders the waveforms in an interactive plot. Waveforms can be inspected, [filtered](#filtering), [clipped](#clipping), [subsampled](#subsampling) and exported to [sigrok PulseView](#export-to-pulseview) or [WAV files](#export-to-wav).

![](https://raw.githubusercontent.com/sam210723/wavebin/master/screenshots/wavebin.png)

**wavebin** has been tested with capture files from a [**Keysight DSO-X 1102G**](https://www.keysight.com/en/pdx-2766207-pn-DSOX1102G/oscilloscope-70-100-mhz-2-analog-channels), [**Keysight MSO-X 4154A**](https://www.keysight.com/en/pdx-x201943-pn-MSOX4154A/mixed-signal-oscilloscope-15-ghz-4-analog-plus-16-digital-channels) and [**Rigol MSO5074**](https://www.rigolna.com/products/digital-oscilloscopes/MSO5000/). If you have access to waveform files from other Agilent, Keysight or Rigol oscilloscopes, please submit them for testing through the [Sample Waveforms issue](https://github.com/sam210723/wavebin/issues/1).

![](https://raw.githubusercontent.com/sam210723/wavebin/master/screenshots/console.png)


## Getting Started
**wavebin** is available via the [Python Package Index (PyPI)](https://pypi.org/project/wavebin/) and is installed using [pip](https://pip.pypa.io/en/stable/).

```
> pip3 install wavebin
```

Keysight oscilloscopes save capture files to external USB Mass Storage devices for easy transfer to a PC. These files use the `.bin` extension.
To open a capture file in **wavebin**, start the application by running:

```
> python3 -m wavebin
```

Next, click *File* &#8594; *Open* and navigate to the `.bin` file.


Alternatively a capture file path can be specified when running **wavebin** using the `-i` argument.

```
> python3 -m wavebin -i [PATH TO BIN FILE]
```

For more information about the **wavebin** command-line arguments run:

```
> python3 -m wavebin -h
                              __    _
   _      ______ __   _____  / /_  (_)___
  | | /| / / __ `/ | / / _ \/ __ \/ / __ \
  | |/ |/ / /_/ /| |/ /  __/ /_/ / / / / /
  |__/|__/\__,_/ |___/\___/_.___/_/_/ /_/  v2.2

             vksdr.com/wavebin


usage: wavebin [-h] [-i FILE] [-v] [--no-opengl] [--no-limit]

Waveform capture viewer for Keysight oscilloscopes.

optional arguments:
  -h, --help   show this help message and exit
  -i FILE      path to Keysight waveform capturefile (.bin)
  -v           enable verbose logging mode
  --no-opengl  disable hardware accelerated rendering with OpenGL
  --no-limit   disable subsampling limit (may cause slow frame rates with large captures)
```

## Features
### Export to PulseView
[PulseView](https://sigrok.org/wiki/PulseView) by [sigrok](https://sigrok.org) is a logic analysis tool typically used with hardware logic analyser devices. It is capable of decoding many serial and parallel protocols with its built-in decoders.

Below is a 115200bd UART waveform captured on a **DSO-X 1102G**, loaded into **wavebin** with [clipping](#clipping) enabled to create a clean digital waveform, exported to PulseView and decoded using the PulseView UART protocol decoder.

![](https://raw.githubusercontent.com/sam210723/wavebin/master/screenshots/pulseview.png)

To export waveforms to PulseView, click *File* &#8594; *Export to PulseView* then navigate to a save location. The produced [`.sr` file](https://sigrok.org/wiki/File_format:Sigrok/v2) can then be opened directly in PulseView.

### Export to WAV
WAV files can be opened in most media players (e.g. [VLC](https://www.videolan.org/vlc/)) and audio editors (e.g. [Audacity](https://www.audacityteam.org/)).

![](https://raw.githubusercontent.com/sam210723/wavebin/master/screenshots/wav.png)

To export waveforms to WAV files, click *File* &#8594; *Export to WAV file* then navigate to a save location. This will produce a mono `.wav` file for each waveform. The WAV files names follow the format `*_[n].wav`, where `n` is the waveform number starting at `0`.


### Filtering
A [Savitzky-Golay low pass filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter) is included in **wavebin** for smoothing waveforms. This filter can be enabled using the *Filter Type* dropdown menu.

![](https://raw.githubusercontent.com/sam210723/wavebin/master/screenshots/filtering.png)


### Clipping
The clipping option converts analog waveforms to digital waveforms in a similar way to a Schmitt trigger.

The [filtering](#filtering) and clipping options can be used simultaneously. Clipping is always applied after filtering.

![](https://raw.githubusercontent.com/sam210723/wavebin/master/screenshots/clipping.png)


### Subsampling
When a waveform capture is first loaded, all available sample points will be used to render the waveform.
The subsampling option renders the waveform using an equally-spaced subset of points.

Below is a 62.5 MHz wave being rendered with all `20,000` points in the capture file, and then with only `1250` points.

![](https://raw.githubusercontent.com/sam210723/wavebin/master/screenshots/subsampling.png)

By default, waveforms with over `50,000` points will automatically be subsampled. This can be overridden using the `--no-limit` switch.

## Resources
  - [FaustinCarter/agilent_read_binary](https://github.com/FaustinCarter/agilent_read_binary)
  - [yodalee/keysightBin](https://github.com/yodalee/keysightBin/)
  - [Input output formats - sigrok](https://sigrok.org/wiki/Input_output_formats)
  - [File format:sigrok/v2 - sigrok](https://sigrok.org/wiki/File_format:Sigrok/v2)

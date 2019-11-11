# SD9Tool

## Overview
A simple Python script to extract audio from / import audio into SD9 files.

Credit to **RHKirby** for posting an excellent breakdown of the SD9 header.

## Features
* Export audio from SD9 file
* Import audio into SD9 file
* Set audio volume
* Set section loop start and stop

## Requirements
* Python 3.6 or higher

## Usage
To get the help dialogue, run `python sd9tool.py --help`. See below for argument details:

**General Options**
* `--sd9 <FILE>` - SD9 file you wish to modify
* `--clobber` - Overwrite file on save. For saving SD9 files, **not** providing this will save the data into "your_file.sd9_out" instead

**SD9 Operations**
* `--print` - Output SD9 header information
* `--modify` - Only modify SD9 header parameters (see below)
* `--import <FILE>` - Replace audio file with the one provided. *Note: File provided must already be saved in Microsoft ADPCM format*
* `--export <FILE>` - Export audio file in SD9

**SD9 Parameters**
If none of the options below are specified, whatever is in the file will be used.
* `--loop <True|False>` - Enable portion of the track to loop
* `--loop-start` - Sample number indicating the start of the loop
* `--loop-end` - Sample number indicating the end of the loop. *Note: this may be needed if your audio file is not looping smoothly*
* `--volume` - Set the volume of the audio track, range is 0 - 125 (loudest)

## Examples
Import audio into SD9, set the volume to 95, and set the start and end sample:
```bash
python sd9tool.py --sd9 8thstyle.sd9 --import ddr4m.wav --volume 95 --loop --loop-start 0 --loop-end 1016063
```

Export audio from SD9 to a file:
```bash
python sd9tool.py --sd9 8thstyle.sd9 --export 8thstyle.wav
```
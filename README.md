# Overview

This repo contains two scripts for working with proprietary audio files:
* `sd9tool.py` - Extracts audio from / imports audio into SD9 files
* `ssp2wav.py` - Extracts all audio files from SSP files in WAV or SD9 format

Credit to **RHKirby** for posting an excellent breakdown of the SD9 header.

# SD9Tool
This script lets you extract audio from / import audio into SD9 files. 

This script also supports setting **section loops**, which tells the game once you reach a section in the track (loop end), go back to another section (loop start). This lets you set an intro to the loop that will only play once. These are measured in **audio samples**, so you will need to use a tool such as Audacity to find where these are.

**NOTE:** When importing custom audio into an SD9 file, it must first be in **Microsoft ADPCM format**. Tools like [Audacity](https://www.audacityteam.org/) or [FFmpeg](https://www.ffmpeg.org/download.html) can be used to convert your audio to this format.

## Features
* Export audio from SD9 file
* Import audio into SD9 file
* Transfer audio and parameters from one SD9 file to another
* Set audio volume
* Set section loops

## Requirements
* Python 3.6 or higher

## Options
To get the help dialogue, run `python sd9tool.py --help`. See below for argument details:

#### General Options
* `--sd9 <FILE>` - SD9 file you wish to modify
* `--clobber` - Overwrite file on save. For saving SD9 files, **not** providing this will save the data into "your_file.sd9_out" instead
* `--outfile` - Specify output SD9 file

#### SD9 Operations
* `--print` - Output SD9 header information
* `--modify` - Only modify SD9 header parameters (see "SD9 Parameters" section)
* `--import <WAV_FILE>` - Replace audio file with the one provided. *Note: File provided must already be saved in Microsoft ADPCM format*
* `--export <WAV_FILE>` - Export audio file in SD9
* `--transfer <SD9_FILE>` - Transfer audio data, volume and loop parameters from `SD9_FILE` into the loaded SD9 file

#### SD9 Parameters
If none of the options below are specified, whatever is in the file will be used.
* `--loop <0|1>` - Enable(1) / Disable(0) portion of the track to loop
* `--loop-start` - Sample number indicating the start of the loop
* `--loop-end` - Sample number indicating the end of the loop. *Note: this may be needed if your audio file is not looping smoothly*
* `--volume` - Set the volume of the audio track, range is 0 - 125 (loudest)

## Usage Examples
Import audio into SD9, set the volume to 95, enable looping section, and set the start and end sample for loop:
```bash
python sd9tool.py --sd9 8thstyle.sd9 --import ddr4m.wav --volume 95 --loop 1 --loop-start 0 --loop-end 1016063
```

Export audio from SD9 to a file:
```bash
python sd9tool.py --sd9 8thstyle.sd9 --export 8thstyle.wav
```

Modify SD9 volume
```bash
python sd9tool.py --sd9 8thstyle.sd9 --modify --volume 97
```

Transfer SD9 data from `source.sd9` to `destination.sd9` and overwrite destination file:
```bash
python sd9tool.py --sd9 destination.sd9 --transfer source.sd9 --clobber
```

# SSP2WAV
This script exports sound data found in SSP files in either SD9 or WAV format. It goes about this in a brute force manner scanning for SD9 headers byte for byte.

Audio extracted is placed in a directory titled `export_<SSP filename>` with each exported track numbered 0 to N.

## Features
* Extract WAV audio from SSP
* Extract SD9 data from SSP

## Requirements
* Python 3.6 or higher

## Options
* `--ssp` - SSP file to scan for data
* `--verbose` - Print more verbose output when SD9 data is found
* `--sd9` - Export data in SD9 format (WAV by default)

## Usage Examples
Export audio in WAV format:
```
python ssp2sd9.py -f lincle.ssp
```
Export audio in SD9 format:
```
python ssp2sd9.py -f seeweewus.ssp
```

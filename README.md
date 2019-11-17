# Overview

This repo contains two scripts for working with proprietary audio files:
* `sd9tool.py` - Extracts audio from / imports audio into SD9 files
* `ssp2wav.py` - Extracts all audio files from SSP files in WAV or SD9 format

Credit to **RHKirby** for posting an excellent breakdown of the SD9 header.

# SD9Tool
This script lets you extract audio from / import audio into SD9 files. 

Audio tracks exported from this script will be in Microsoft ADPCM format. When importing audio, be sure your audio track is also in this format. If not, you can convert it with [ffmpeg](https://www.ffmpeg.org/download.html).

This script supports setting **section loops**, which tells the game once you reach a section in the track (loop end), go back to another section (loop start). This lets you set an intro to the loop that will only play once. These are measured in **audio samples**, so you will need to use a tool such as Audacity to find where these are.

## Features
* Export audio from SD9 file
* Import audio into SD9 file
* Set audio volume
* Set section loops

## Requirements
* Python 3.6 or higher

## Options
To get the help dialogue, run `python sd9tool.py --help`. See below for argument details:

#### General Options
* `--sd9 <FILE>` - SD9 file you wish to modify
* `--clobber` - Overwrite file on save. For saving SD9 files, **not** providing this will save the data into "your_file.sd9_out" instead

#### SD9 Operations
* `--print` - Output SD9 header information
* `--modify` - Only modify SD9 header parameters (see below)
* `--import <FILE>` - Replace audio file with the one provided. *Note: File provided must already be saved in Microsoft ADPCM format*
* `--export <FILE>` - Export audio file in SD9

#### SD9 Parameters
If none of the options below are specified, whatever is in the file will be used.
* `--loop <True|False>` - Enable portion of the track to loop
* `--loop-start` - Sample number indicating the start of the loop
* `--loop-end` - Sample number indicating the end of the loop. *Note: this may be needed if your audio file is not looping smoothly*
* `--volume` - Set the volume of the audio track, range is 0 - 125 (loudest)

## Usage Examples
Import audio into SD9, set the volume to 95, and set the start and end sample:
```bash
python sd9tool.py --sd9 8thstyle.sd9 --import ddr4m.wav --volume 95 --loop true --loop-start 0 --loop-end 1016063
```

Export audio from SD9 to a file:
```bash
python sd9tool.py --sd9 8thstyle.sd9 --export 8thstyle.wav
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
./ssp2sd9.py -f lincle.ssp
```
Export audio in SD9 format:
```
./ssp2sd9.py -f seeweewus.ssp
```
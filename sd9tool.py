#!/usr/bin/env python3
import sys, os, argparse

'''
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
SD9Tool - written by Datus

Huge thanks to RHKirby for posting an excellent breakdown of the SD9 header on
the forums. 
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
'''

class SD9File(object):
    SD9_HEADER = b"\x53\x44\x39\x00"

    def __init__(self, filename=None, clobber=False):
        # Set SD9 file defaults, overriden with file
        self.header     = self.SD9_HEADER           # SD9 header ID
        self.headerSize = b"\x20\x00\x00\x00"       # Should never change
        self.audioSize  = b"\x00\x00\x00\x00"       # Byte length of wav file
        self.fluff1     = b"\x31\x32\x01\x00"       # Should be replaced with whatever is in the existing file
        self.fluff2     = b"\x40\x00"               # Is always 0x40 0x00, changing it breaks
        self.volume     = b"\x00"                   # Scale is reverse where 0 is loudest
        self.fluff3     = b"\x00"                   # Possibly related to volume
        self.loopStart  = b"\x00\x00\x00\x00"       # Control where the loop cycle starts in # of samples
        self.loopEnd    = b"\x00\x00\x00\x00"       # Control where the loop cycle ends in # of samples
        self.loop       = b"\x00"                   # Loop enabled, 0=off 1=on
        self.fluff4     = b"\x00"                   # Loop end flag?
        self.index      = b"\x00\x00"               # Unique sound index, must be same as file replacing
        self.audio      = b""                       # Audio file in Microsoft ADPCM format

        self.fileLoaded = False
        self.clobber    = clobber

        if filename:
            self.fileLoaded = self.sd9_load(filename)

    def sd9_load(self, filename):
        '''
        Function : sd9_load
        Purpose  : Load SD9 header and audio data from a file
        '''
        if self.clobber:
            self.filename = filename
        else:
            self.filename = filename + "_out"

        try:
            sd9 = open(filename, "rb")
            self.header     = sd9.read(4)
            self.headerSize = sd9.read(4)
            self.audioSize  = sd9.read(4)
            self.fluff1     = sd9.read(4)
            self.fluff2     = sd9.read(2)
            self.volume     = sd9.read(1)
            self.fluff3     = sd9.read(1)
            self.loopStart  = sd9.read(4)
            self.loopEnd    = sd9.read(4)
            self.loop       = sd9.read(1)
            self.fluff4     = sd9.read(1)
            self.index      = sd9.read(2)
            self.audio      = sd9.read(int.from_bytes(self.audioSize, byteorder='little'))
            sd9.close()

            if self.header != self.SD9_HEADER:
                print("ERROR: SD9 file provided is invalid")
                return False
            
            return True

        except Exception as err:
            print(f"ERROR: Could not load SD9: {err}")
            sd9.close()
            return False

    def sd9_save(self):
        '''
        Function : sd9_save
        Purpose  : Save SD9 contents to a file
        '''
        try:
            outfile = open(self.filename, 'wb')
            outfile.write(self.header)
            outfile.write(self.headerSize)
            outfile.write(self.audioSize)
            outfile.write(self.fluff1)
            outfile.write(self.fluff2)
            outfile.write(self.volume)
            outfile.write(self.fluff3)
            outfile.write(self.loopStart)
            outfile.write(self.loopEnd)
            outfile.write(self.loop)
            outfile.write(self.fluff4)
            outfile.write(self.index)
            outfile.write(self.audio)
            return True
        except Exception as err:
            print(f"ERROR: Could not save SD9 file: {err}")
            return False

    def sd9_set_param(self, volume=None, loop=None, loopStart=None, loopEnd=None):
        '''
        Function : sd9_set_param
        Purpose  : Set volume and audio section loop parameters to SD9 file
        '''
        if volume is not None:
            if volume > 125:
               print("WARNING: Ignoring volume above 125")
            else:
                volume = 125 - volume
                self.volume = volume.to_bytes(1, byteorder="little", signed=False)
        if loop:
            self.loop = loop.to_bytes(1, byteorder='little', signed=False)
        if loopStart is not None:
            loopStart *= 4
            self.loopStart = loopStart.to_bytes(4, byteorder='little', signed=False)
        if loopEnd is not None:
            loopEnd *= 4
            self.loopEnd = loopEnd.to_bytes(4, byteorder='little', signed=False)


    def audio_import(self, filename):
        '''
        Function : audio_import
        Purpose  : Import audio file (in Microsoft ADPCM format) to SD9 audio data section
        '''
        try:
            infile = open(filename, "rb")
            self.audio = infile.read()
            self.audioSize = len(self.audio).to_bytes(4, byteorder="little", signed=False)
        except Exception as err:
            print(f"ERROR: Could not import audio track: {err}")
            return False

        saved = self.sd9_save()
        if saved:
            print(f"SUCCESS: Audio imported into SD9: {self.filename}")
        return saved

    def audio_export(self, export_name):
        '''
        Function : audio_export
        Purpose  : Dump the audio data portion of an SD9 file to a file
        '''
        if os.path.exists(export_name) and not self.clobber:
            print("ERROR: Output audio exists: " + export_name)
            return False

        try:
            outfile = open(export_name, "wb")
            outfile.write(self.audio)
            outfile.close()
            print(f"SUCCESS: Audio exported from SD9: {export_name}")
            return True
        except Exception as err:
            print(f"ERROR: Could not export audio track {err}")
            return False

    def __str__(self):
        '''
        Function : __str__
        Purpose  : Represent SD9 header as string
        '''
        index           = int.from_bytes(self.index, byteorder='little')
        audioSize       = int.from_bytes(self.audioSize, byteorder='little')
        audioVolume     = 125 - int.from_bytes(self.volume, byteorder='little')
        audioLoop       = bool(int.from_bytes(self.loop, byteorder='little'))
        audioLoopStart  = int(int.from_bytes(self.loopStart, byteorder='little') / 4)
        audioLoopEnd    = int(int.from_bytes(self.loopEnd, byteorder='little') / 4)

        s  = f'[{self.filename}]\n'
        s += f'Index                 : {[hex(x) for x in self.index]} ({index})\n'
        s += f'Audio Size            : {[hex(x) for x in self.audioSize]} ({audioSize} B)\n'
        s += f'Audio Volume          : {[hex(x) for x in self.volume]} ({audioVolume}%)\n'
        s += f'Section Loop Enabled  : {[hex(x) for x in self.loop]} ({audioLoop})\n'
        s += f'Section Loop Start    : {[hex(x) for x in self.loopStart]} ({audioLoopStart})\n'
        s += f'Section Loop End      : {[hex(x) for x in self.loopEnd]} ({audioLoopEnd})'

        return s

def main(argv):
    parser = argparse.ArgumentParser(
        prog="SD9Tool", 
        description="SD9 import, export, and modification tool"
    )

    # General arguments
    parser.add_argument(
        '-f', '--sd9',
        help='SD9 file to use as base',
        required=True
    )
    parser.add_argument(
        '-c', '--clobber',
        help='Overwrite output files',
        action='store_true'
    )

    # SD9 file operations
    fileAction = parser.add_argument_group(title="File Operations")
    fileActionExclusive = fileAction.add_mutually_exclusive_group(required=True)
    fileActionExclusive.add_argument(
        "-p", "--print",
        help='Print SD9 header hex data',
        action='store_true'
    )
    fileActionExclusive.add_argument(
        "-m", "--modify",
        help='Only modify SD9 options',
        action='store_true',
        dest='sd9_modify'
    )
    fileActionExclusive.add_argument(
        '-i', '--import',
        help='Audio file to import into SD9 file',
        dest='audio_import'
    )
    fileActionExclusive.add_argument(
        '-e', '--export',
        help='Audio file to export from SD9 file',
        dest='audio_export'
    )

    # SD9 parameters, by default it will use whatever is in the file
    trackOptions = parser.add_argument_group(title="Audio Track Options")
    trackOptions.add_argument(
        '-v', '--volume',
        type=int
    )
    trackOptions.add_argument(
        '-l', '--loop',
        type=bool
    )
    trackOptions.add_argument(
        '-ls', '--loop-start',
        type=int
    )
    trackOptions.add_argument(
        '-le', '--loop-end',
        type=int
    )

    args = parser.parse_args()

    # Load SD9 file
    sd9 = SD9File(filename=args.sd9, clobber=args.clobber)

    # Do not proceed without SD9 file loaded
    if not sd9.fileLoaded:
        return False

    # Set SD9 header parameters: volume and section loop settings
    sd9.sd9_set_param(args.volume, args.loop, args.loop_start, args.loop_end)

    #
    # Process SD9 file
    #

    # Print SD9 file information and quit
    if args.print:
        print(sd9)

    # Import audio, update size in header, and save SD9 file
    elif args.audio_import:
        ret_import  = sd9.audio_import(args.audio_import)
        if not ret_import:
            return 1

    # Export audio to file
    elif args.audio_export:
        ret_export  = sd9.audio_export(export_name=args.audio_export)
        if not ret_export:
            return 1

    # Save modified SD9 header 
    elif args.sd9_modify:
        ret_save    = sd9.sd9_save()
        if not ret_save:
            return 1

    return 0

exit(main(sys.argv))

#!/usr/bin/env python3
import sys, os, io, argparse

SD9_HEADER = b"\x53\x44\x39\x00"

def sspScan(ssp_file, export_sd9, clobber, verbose):
    header_buffer = b''
    sd9_counter   = 0
    byte_counter  = 0

    outdir = f'export_{ssp_file}'

    if not os.path.exists(outdir):
        try:
            os.mkdir(outdir)
        except Exception as err:
            print(f"ERROR: Could not create directory: {outdir}: {err}")
            return False
    
    print(f"Scanning {ssp_file}")
    try:
        ssp  = open(ssp_file, 'rb')

        # Keep a rolling buffer of 32 bytes and look for the SD9 header ID
        # Once found, get extract the audio data and export it to file
        while True:
            byte = ssp.read(1)

            if byte == b'':
                break
            elif len(header_buffer) == 32:
                header_buffer = header_buffer[1:]

            header_buffer += byte

            # SD9 file found!
            if header_buffer[0:4] == SD9_HEADER:
                audioSize = int.from_bytes(header_buffer[8:12], byteorder='little')
                audioData = ssp.read(audioSize)

                if verbose:
                    print(f"Found SD9: offset={hex(byte_counter)} size={audioSize}")
                else:
                    print("♪", end="", flush=True)

                # Export WAV or SD9 file
                export_name = f"{outdir}/{ssp_file}_{sd9_counter}"
                if export_sd9:
                    export_name += ".sd9"
                else:
                    export_name += ".wav"

                with open(export_name, "wb") as outfile:
                    if export_sd9:
                        outfile.write(header_buffer)
                    outfile.write(audioData)

                sd9_counter += 1

            byte_counter += 1
        ssp.close()
    except Exception as err:
        print(err)
        ssp.close()

    print(f"\nFound {sd9_counter} file(s) in {ssp_file}")

def main(argv):
    parser = argparse.ArgumentParser(
        prog="SSP2SD9", 
        description="SSP export tool"
    )

    # General arguments
    parser.add_argument(
        '-f', '--ssp',
        help='SSP file to use as base',
        required=True
    )
    parser.add_argument(
        '-c', '--clobber',
        help='Overwrite output files',
        action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Increase script verbosity',
        action='store_true'
    )

    parser.add_argument(
        '--sd9',
        help='Export all sounds in SSP to SD9 format (default: WAV)',
        dest='export_sd9',
        action='store_true'
    )

    args = parser.parse_args()
    sspScan(args.ssp, args.export_sd9, args.clobber, args.verbose)

exit(main(sys.argv))
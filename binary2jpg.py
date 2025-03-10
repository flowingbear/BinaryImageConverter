#!/usr/bin/env python3
import argparse
import sys
from converter import BinaryImageConverter
from utils import validate_file, show_progress

def main():
    parser = argparse.ArgumentParser(
        description='Convert binary files to JPG images and vice versa'
    )
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument(
        '--mode',
        choices=['bin2jpg', 'jpg2bin'],
        required=True,
        help='Conversion mode: bin2jpg (binary to JPG) or jpg2bin (JPG to binary)'
    )

    args = parser.parse_args()

    try:
        # Validate input file
        if not validate_file(args.input_file):
            sys.exit(1)

        converter = BinaryImageConverter()

        if args.mode == 'bin2jpg':
            print(f"Converting binary file '{args.input_file}' to JPG image '{args.output_file}'")
            converter.binary_to_image(args.input_file, args.output_file, progress_callback=show_progress)
            print("\nConversion completed successfully!")
            
        else:  # jpg2bin
            print(f"Converting JPG image '{args.input_file}' to binary file '{args.output_file}'")
            converter.image_to_binary(args.input_file, args.output_file, progress_callback=show_progress)
            print("\nConversion completed successfully!")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

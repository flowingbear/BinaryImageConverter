import numpy as np
from PIL import Image
import math
import os

class BinaryImageConverter:
    def __init__(self):
        self.HEADER_SIZE = 24  # bytes to store original file size and name
        self.CHUNK_SIZE = 1024 * 1024  # 1MB chunks for processing
        self.MAGIC_BYTES = b'B2J'  # Magic bytes to identify our converted images

    def binary_to_image(self, input_file, output_file, progress_callback=None):
        """Convert a binary file to a JPG image."""
        # Read binary file
        with open(input_file, 'rb') as f:
            binary_data = f.read()

        # Prepare header with magic bytes, original file size and name
        file_size = len(binary_data)
        file_name = os.path.basename(input_file).encode('utf-8')
        if len(file_name) > 16:
            file_name = file_name[:16]

        # New header format: MAGIC_BYTES + name_length(1) + name(16) + size(7)
        header = self.MAGIC_BYTES + len(file_name).to_bytes(1, 'big') + file_name + file_size.to_bytes(7, 'big')

        # Combine header and data
        full_data = header + binary_data

        # Calculate image dimensions
        data_len = len(full_data)
        width = int(math.sqrt(data_len / 3) + 1)
        height = width

        # Create numpy array and pad with zeros
        pixels = np.zeros((height, width, 3), dtype=np.uint8)
        pixels_flat = pixels.reshape(-1, 3)

        # Convert binary data to RGB values
        for i, byte_idx in enumerate(range(0, len(full_data), 3)):
            if progress_callback:
                progress_callback(byte_idx, len(full_data))

            chunk = full_data[byte_idx:byte_idx + 3]
            if len(chunk) < 3:
                chunk = chunk + b'\x00' * (3 - len(chunk))
            pixels_flat[i] = list(chunk)

        # Create and save image
        image = Image.fromarray(pixels)
        image.save(output_file, 'JPEG', quality=100)

    def image_to_binary(self, input_file, output_file, progress_callback=None):
        """Convert a JPG image back to the original binary file."""
        # Load image
        image = Image.open(input_file)
        pixels = np.array(image)

        # Extract binary data
        binary_data = pixels.reshape(-1, 3).tobytes()

        # Check for magic bytes
        if len(binary_data) < len(self.MAGIC_BYTES) or binary_data[:len(self.MAGIC_BYTES)] != self.MAGIC_BYTES:
            raise ValueError("This image was not created by this converter. Please only use images created with the bin2jpg mode.")

        # Extract header information (after magic bytes)
        header_start = len(self.MAGIC_BYTES)
        name_length = binary_data[header_start]
        original_name = binary_data[header_start + 1:header_start + name_length + 1]
        file_size = int.from_bytes(binary_data[header_start + 17:header_start + 24], 'big')

        # Calculate new header size including magic bytes
        total_header_size = self.HEADER_SIZE + len(self.MAGIC_BYTES)

        # Extract and validate file content
        file_content = binary_data[total_header_size:total_header_size + file_size]

        if len(file_content) < file_size:
            raise ValueError("Corrupted image: Unable to recover original file data")

        # Write binary data
        with open(output_file, 'wb') as f:
            bytes_written = 0
            chunk_size = self.CHUNK_SIZE

            while bytes_written < file_size:
                if progress_callback:
                    progress_callback(bytes_written, file_size)

                chunk = file_content[bytes_written:bytes_written + chunk_size]
                f.write(chunk)
                bytes_written += len(chunk)
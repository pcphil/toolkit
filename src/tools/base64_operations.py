import base64

class Base64Operations:

    @staticmethod
    def encode_to_base64(input,output_path='output/encoded_string.txt'):
        """Encodes a string to Base64 format. for file or string"""
        if isinstance(input, str):
            input_bytes = input.encode('utf-8')
        else:
            input_bytes = input.read() if hasattr(input, 'read') else bytes(input)
        encoded_bytes = base64.b64encode(input_bytes)
        encoded_string = encoded_bytes.decode('utf-8')
        with open(output_path, 'w') as f:
            f.write(encoded_string)
        return encoded_string

    @staticmethod
    def decode_from_base64(input, output_path='output/decoded_string.txt'):
        """Decodes a Base64 encoded string."""
        if isinstance(input, str):
            input_bytes = input.encode('utf-8')
        else:
            input_bytes = input.read() if hasattr(input, 'read') else bytes(input)
        decoded_bytes = base64.b64decode(input_bytes)
        decoded_string = decoded_bytes.decode('utf-8')
        with open(output_path, 'w') as f:
            f.write(decoded_string)
        return decoded_string
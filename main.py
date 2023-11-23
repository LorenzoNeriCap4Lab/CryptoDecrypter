from Crypto.Cipher import AES
import base64
import yaml
import shutil
import sys

def decrypt_and_reencrypt(original_key, new_key, text_to_decrypt):
    iv = original_key  # Use the same key as the IV

    # Create an AES cipher object for decryption
    decrypt_cipher = AES.new(original_key, AES.MODE_CBC, iv)

    # Decode and decrypt the ciphertext
    decoded_ciphertext = base64.b64decode(text_to_decrypt)
    decrypted_text = decrypt_cipher.decrypt(decoded_ciphertext)

    # Remove PKCS7 padding (if any)
    padding_length = decrypted_text[-1]
    decrypted_text = decrypted_text[:-padding_length]

    # Convert the decrypted bytes to a string
    plaintext = decrypted_text.decode('utf-8')

    # Define the new IV for re-encryption (you may generate a new IV or use an existing one)
    new_iv = new_key  # Replace with your new IV

    # Create a new AES cipher object for re-encryption
    reencrypt_cipher = AES.new(new_key, AES.MODE_CBC, new_iv)

    # Pad the plaintext to a multiple of 16 bytes using PKCS7 padding
    pad_length = 16 - (len(plaintext) % 16)
    plaintext_padded = plaintext.encode('utf-8') + bytes([pad_length] * pad_length)

    # Encrypt the padded plaintext with the new key and IV
    reencrypted_text = reencrypt_cipher.encrypt(plaintext_padded)

    # Encode the re-encrypted text in base64
    encoded_reencrypted_text = base64.b64encode(reencrypted_text).decode('utf-8')

    return encoded_reencrypted_text

def read_yaml_fields(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

        return yaml_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

def replace_field_values(yaml_data):
    if isinstance(yaml_data, dict):
        for key, value in yaml_data.items():
            if isinstance(value, str) and "![" in value:
                yaml_data[key] = "![" + decrypt_and_reencrypt(original_key, new_key, value) + "]"
            elif isinstance(value, (dict, list)):
                replace_field_values(value)  # Recursively handle nested structures
    elif isinstance(yaml_data, list):
        for index, item in enumerate(yaml_data):
            if isinstance(item, str) and "![" in item:
                yaml_data[key] = "![" + decrypt_and_reencrypt(original_key, new_key, value) + "]"
            elif isinstance(item, (dict, list)):
                replace_field_values(item)  # Recursively handle nested structures

    return yaml_data

def write_yaml_fields(file_path, yaml_data):
    try:
        with open(file_path, 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file,  default_flow_style=False)
    except Exception as e:
        print(f"Error writing YAML: {e}")

def replace_single_quotes_with_double_quotes(input_file):
    # Create a temporary file
    temp_file = input_file + ".tmp"

    try:
        with open(input_file, 'r') as infile, open(temp_file, 'w') as outfile:
            for line in infile:
                # Replace single quotes with double quotes in each line
                modified_line = line.replace("'", '"')
                outfile.write(modified_line)

        # Replace the original file with the temporary file
        shutil.move(temp_file, input_file)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")




if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python main.py input_file_path output_file_path original_key new_key")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    original_key = sys.argv[3].encode('utf-8')
    new_key = sys.argv[4].encode('utf-8')

    yaml_data = read_yaml_fields(input_file_path)

    if yaml_data:
        modified_yaml_data = replace_field_values(yaml_data)
        write_yaml_fields(output_file_path, modified_yaml_data)
        replace_single_quotes_with_double_quotes(output_file_path)
        print(f"Modified YAML written to {output_file_path}")


# README

## Overview

This Python script is designed to decrypt and reencrypt sensitive fields in a YAML file using the AES encryption algorithm. The decryption and reencryption process involves replacing specific placeholders in the YAML file with their decrypted counterparts.

## Dependencies

The script relies on the following Python libraries:

- `Crypto.Cipher` from the `pycryptodome` package for AES encryption
- `base64` for base64 encoding and decoding
- `yaml` for YAML file processing
- `shutil` for file manipulation
- `sys` for handling command-line arguments

## Installation Guide

1. **Install Python**: Ensure that you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

2. **Install Dependencies**: Install the required dependencies using the following command:

   ```bash
   pip install -r requirements.txt

3. **Clone or Download the Repository**:  Clone this repository or download the script (main.py) to your local machine.:

   ```bash
   git clone https://github.com/LorenzoNeriCap4Lab/CryptoDecrypter.git

4. **Navigate to the Script Directory**: Move to the directory where the script is located.

   ```bash
   cd path/to/script/directory

## Usage

To use the script, run it from the command line with the following arguments:

    
    python main.py input_file_path output_file_path original_key new_key

- input_file_path: Path to the input YAML file that contains sensitive fields.
- output_file_path: Path to the output YAML file where the modified data will be saved.
- original_key: 16-byte original key used for decryption (provided as a command-line argument).
- new_key: 16-byte new key used for re-encryption (provided as a command-line argument).

## Example

    python main.py test_input.yaml test_output.yaml 0123456789abcdef fedcba9876543210

This command will read the YAML data from secure.prod.yaml, replace sensitive fields, and write the modified YAML to secure.loc_prod.yaml. The provided original and new keys are used for decryption and re-encryption, respectively.

## Notes

- Ensure that the script is executed in a secure environment, as it deals with sensitive information.
- Keep the original and new keys secure and do not share them openly.
- Backup your YAML files before running the script to avoid data loss.
- For any issues or inquiries, feel free to create ticket on the GitHub repository
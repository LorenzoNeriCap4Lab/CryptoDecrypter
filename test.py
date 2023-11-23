from Crypto.Cipher import AES
import base64

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

# Example usage
original_key = b'0123456789abcdef'  # 8-byte key
new_key = b'fedcba9876543210'  # Replace with your new key
# Hello_There! is the content
ciphertext = 'I9rZ2qt900x3P1iszTTAxA=='

new_encrypted_text = decrypt_and_reencrypt(original_key, new_key, ciphertext)
print("New Encrypted Text:", new_encrypted_text)
original_encrypted_text=decrypt_and_reencrypt(new_key, original_key, new_encrypted_text)
print("Original Encrypted Text:", original_encrypted_text)
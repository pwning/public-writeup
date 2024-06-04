def reverse_custom_operation(encrypted_text):
    original_text = []
    c3 = 0
    for i in range(len(encrypted_text)):
        char_at = encrypted_text[i]
        original_text.append(chr((ord(char_at) - c3 + 256) % 256))  # Adjust with modulo 256 to handle wrap-around
        c3 += 1
    return ''.join(original_text)

def reverse_xor_operation(encrypted_text, key):
    length = len(encrypted_text)
    key_length = len(key)
    repeated_key = (key * (length // key_length)) + key[:length % key_length]

    original_text = []
    for i in range(length):
        original_text.append(chr(ord(encrypted_text[i]) ^ ord(repeated_key[i])))

    return ''.join(original_text)

def decrypt(encrypted_text, key):
    # Step 1: Reverse customOperation
    after_custom_operation = reverse_custom_operation(encrypted_text)

    # Step 2: Reverse xorOperation
    return reverse_xor_operation(after_custom_operation, key)

def main():
    encrypted_flag_hex = "0f010a0c0c121e1166656763236c68636c69676a6e6a20247524797679717675752b7b7b787b7b7c327d7fc288c2863e"
    
    # Decode hex to bytes
    encrypted_flag_bytes = bytes.fromhex(encrypted_flag_hex)
    
    # Decode bytes to string using utf-8
    encrypted_flag = encrypted_flag_bytes.decode('utf-8', errors='ignore')  # Decode as utf-8
    print(encrypted_flag)

    key = "lol"
    decrypted_flag = decrypt(encrypted_flag, key)
    print("Decrypted Flag: " + decrypted_flag)

if __name__ == "__main__":
    main()


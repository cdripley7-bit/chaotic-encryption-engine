import os
import json
import argparse
import matplotlib.pyplot as plt
from chaos_engine import find_encryption_key
from cryptographer import encrypt_image, decrypt_image

def save_key(key, filename):
    """Saves the 6-parameter key to a local file."""
    with open(filename, 'w') as f:
        json.dump(key, f)
    print(f"[*] Secret key securely saved to {filename}")

def load_key(filename):
    """Loads the key from the local file."""
    if not os.path.exists(filename):
        print(f"[!] Error: Could not find key file '{filename}'.")
        return None
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Hyperchaotic Image Encryptor: Secure your images using 3D strange attractors."
    )
    
    # Define the flags the user can pass in the terminal
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', type=str, metavar='FILE', help="Path to the image you want to encrypt")
    group.add_argument('-d', '--decrypt', type=str, metavar='FILE', help="Path to the image you want to decrypt")
    
    # Optional flag to specify a custom key name
    parser.add_argument('-k', '--key', type=str, default="master.key", metavar='KEY_FILE', 
                        help="Path to the key file (defaults to master.key)")

    # Parse the arguments
    args = parser.parse_args()

    # --- ENCRYPTION LOGIC ---
    if args.encrypt:
        if not os.path.exists(args.encrypt):
            print(f"[!] Error: Target file '{args.encrypt}' not found.")
            return

        print(f"[*] Mining new chaotic key for {args.encrypt}...")
        secret_key = find_encryption_key()
        
        save_key(secret_key, args.key)
        
        encrypted_img, _, _ = encrypt_image(args.encrypt, secret_key)
        output_name = "ENCRYPTED_" + os.path.basename(args.encrypt)
        
        plt.imsave(output_name, encrypted_img)
        print(f"[*] Success! Encrypted image saved as: {output_name}")

    # --- DECRYPTION LOGIC ---
    elif args.decrypt:
        if not os.path.exists(args.decrypt):
            print(f"[!] Error: Target file '{args.decrypt}' not found.")
            return

        print(f"[*] Loading cryptographic key from {args.key}...")
        secret_key = load_key(args.key)
        if secret_key is None:
            return

        decrypted_img = decrypt_image(args.decrypt, secret_key)
        
        # Clean up the output name (remove 'ENCRYPTED_' if it exists)
        base_name = os.path.basename(args.decrypt)
        clean_name = base_name.replace("ENCRYPTED_", "")
        output_name = "DECRYPTED_" + clean_name
        
        plt.imsave(output_name, decrypted_img)
        print(f"[*] Success! Image restored and saved as: {output_name}")

if __name__ == "__main__":
    main()
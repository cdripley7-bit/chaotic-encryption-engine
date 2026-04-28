from chaos_engine import find_encryption_key
from cryptographer import encrypt_image, decrypt_image

if __name__ == "__main__":
    print("--- HYPERCHAOTIC IMAGE ENCRYPTION ---")
    
    # 1. Mine the key
    secret_key = find_encryption_key()
    
    # 2. Encrypt the image (replace with your test image name)
    encrypted_img, _, _ = encrypt_image('test-image.png', secret_key)
    
    # 3. Decrypt the image to prove it works
    decrypted_img = decrypt_image(encrypted_img, secret_key)
    
    print("\nProcess finished successfully!")
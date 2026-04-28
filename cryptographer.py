import matplotlib.pyplot as plt
import numpy as np
from chaos_engine import generate_3d_map 

def encrypt_image(image_path, secret_key):
    print("Loading image...")
    # Load the image and convert to standard 8-bit integers (0-255)
    img = plt.imread(image_path)
    if img.dtype == np.float32:
        img = (img * 255).astype(np.uint8)
        
    # Get the dimensions: Height, Width, Color Channels (RGB)
    h, w, channels = img.shape
    total_values = h * w * channels
    
    print(f"Image size: {h}x{w}. Generating {total_values} chaotic numbers...")
    
    # Run the map for the exact number of pixels in the image (times 3 for RGB channels)
    x, y, z = generate_3d_map(secret_key, iterations=total_values)
    
    # Flatten the 3D image matrix into a 1D list of values
    flat_img = img.flatten()
    
    print("Applying Confusion (Shuffling)...")
    # np.argsort looks at the chaotic X array and returns the indices that would sort it.
    # uses this list of indices that would sort the chaotic X values, which is effectively a random shuffle
    shuffle_indices = np.argsort(x)
    scrambled_img = flat_img[shuffle_indices]
    
    print("Applying Diffusion (Color XORing)...")
    # Take the Y coordinates, multiply to extract the random decimal noise, 
    # and convert to numbers between 0 and 255
    y_integers = ((np.abs(y) * 1000000).astype(np.int64) % 256).astype(np.uint8)
    
    # The magical XOR operation. This destroys the color data securely.
    encrypted_flat = scrambled_img ^ y_integers
    
    # Fold the 1D list back into the original 2D image shape
    encrypted_img = encrypted_flat.reshape(h, w, channels)
    
    # Display the results side by side
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(img)
    ax[0].set_title("Original Image")
    ax[0].axis('off')
    
    ax[1].imshow(encrypted_img)
    ax[1].set_title("Encrypted Ciphertext")
    ax[1].axis('off')
    
    plt.show()
    
    return encrypted_img, shuffle_indices, y_integers

def decrypt_image(encrypted_img, secret_key):
    print("Loading encrypted image...")
    h, w, channels = encrypted_img.shape
    total_values = h * w * channels
    
    print("Regenerating the exact same chaotic key sequence...")
    x, y, z = generate_3d_map(secret_key, iterations=total_values)
    
    # Flatten the encrypted image
    encrypted_flat = encrypted_img.flatten()
    
    print("Reversing Diffusion (Undoing the XOR)...")
    y_integers = ((np.abs(y) * 1000000).astype(np.int64) % 256).astype(np.uint8)
    
    # XORing again restores the scrambled colors
    scrambled_flat = encrypted_flat ^ y_integers
    
    print("Reversing Confusion (Un-shuffling the pixels)...")
    # Get the exact same shuffled order we used to encrypt
    shuffle_indices = np.argsort(x)
    
    # Sorting the sorted indices gives us the reverse key
    unshuffle_indices = np.argsort(shuffle_indices)
    
    # Apply the reverse map to put the pixels back in their original spots
    decrypted_flat = scrambled_flat[unshuffle_indices]
    
    # Fold it back into a 2D image
    decrypted_img = decrypted_flat.reshape(h, w, channels)
    
    # Display restored image next to the encrypted version
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(encrypted_img)
    ax[0].set_title("Encrypted Static")
    ax[0].axis('off')
    
    ax[1].imshow(decrypted_img)
    ax[1].set_title("Successfully Decrypted Image")
    ax[1].axis('off')
    
    plt.show()
    
    return decrypted_img
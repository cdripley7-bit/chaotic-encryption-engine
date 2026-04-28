import numpy as np
from numba import njit
import random

@njit
def generate_3d_map(params, iterations=100000):
    a, b, c, d, e, f = params
    
    # Pre-allocate arrays
    x = np.zeros(iterations)
    y = np.zeros(iterations)
    z = np.zeros(iterations)
    
    # Set starting position
    x[0], y[0], z[0] = 0.1, 0.1, 0.1
    
    # The Iterated Map: Calculate the next point based purely on the last point
    # 3d version of the equation pioneered by Procktor and others in the 80s
    for i in range(1, iterations):
        x[i] = np.sin(a * y[i-1]) + c * np.cos(a * x[i-1]) + np.sin(e * z[i-1])
        y[i] = np.sin(b * x[i-1]) + d * np.cos(b * y[i-1]) + np.cos(f * z[i-1])
        z[i] = np.sin(c * x[i-1]) + e * np.cos(d * y[i-1]) + np.sin(a * z[i-1])
        
    return x, y, z

#Calculates the Lyapunov Exponent to measure how chaotic a system is.
#positive LLE means chaos, negative means stable, zero means borderline
@njit
def calculate_lyapunov(params, iterations=10000):
    a, b, c, d, e, f = params
    
    # Start the main point
    x, y, z = 0.1, 0.1, 0.1
    
    # Start the shadow point slightly offset from the main point
    d0 = 1e-8
    xs, ys, zs = x + d0, y, z
    
    lyapunov_sum = 0.0
    
    # Let the system run for 1000 steps without measuring 
    # this period allows th points to shift from the intial random starting point to the actual 
    # attractor shape, which gives us a more accurate LLE measurement
    for _ in range(1000):
        x_new = np.sin(a * y) + c * np.cos(a * x) + np.sin(e * z)
        y_new = np.sin(b * x) + d * np.cos(b * y) + np.cos(f * z)
        z_new = np.sin(c * x) + e * np.cos(d * y) + np.sin(a * z)
        x, y, z = x_new, y_new, z_new
        
    # Reset shadow point to be exactly d0 away after the intial "settling" period 
    # This ensures we are measuring the divergence from the attractor, not just from the random starting point
    xs, ys, zs = x + d0, y, z 
    
    # RUN & MEASURE
    for _ in range(iterations):
        # Step main point forward
        x_next = np.sin(a * y) + c * np.cos(a * x) + np.sin(e * z)
        y_next = np.sin(b * x) + d * np.cos(b * y) + np.cos(f * z)
        z_next = np.sin(c * x) + e * np.cos(d * y) + np.sin(a * z)
        
        # Step shadow point forward
        xs_next = np.sin(a * ys) + c * np.cos(a * xs) + np.sin(e * zs)
        ys_next = np.sin(b * xs) + d * np.cos(b * ys) + np.cos(f * zs)
        zs_next = np.sin(c * xs) + e * np.cos(d * ys) + np.sin(a * zs)
        
        # Calculate new distance between them (d1)
        dx = xs_next - x_next
        dy = ys_next - y_next
        dz = zs_next - z_next
        d1 = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # if they perfectly collide, prevent a divide-by-zero math error
        if d1 == 0:
            d1 = 1e-16
            
        # Add the exponential growth to our running score
        lyapunov_sum += np.log(d1 / d0)
        
        # RENORMALIZE: Pull the shadow point back so it is exactly d0 away again
        xs = x_next + (dx / d1) * d0
        ys = y_next + (dy / d1) * d0
        zs = z_next + (dz / d1) * d0
        
        # Update main points for the next loop
        x, y, z = x_next, y_next, z_next
        
    # Return the average growth per step (The Lyapunov Exponent)
    return lyapunov_sum / iterations

# The Automated Miner: Loops forever until it finds a cryptographic key
def find_encryption_key():
    print("Starting automated chaos miner...")
    attempts = 0
    
    while True:
        attempts += 1
        # Pick random parameters for the system
        params = [random.uniform(-2.5, 2.5) for _ in range(6)]
        
        # Evaluate them by calculating the Lyapunov Exponent
        lle = calculate_lyapunov(tuple(params))
        
        # If LLE is > 0.1, we have a strong chaotic system that could be used for encryption
        if lle > 0.1:
            print(f"\nJACKPOT Found a strong chaotic system after {attempts} attempts.")
            print(f"Lyapunov Exponent: {lle:.4f}")
            print(f"Secret Encryption Key (Parameters): {np.round(params, 4)}")
            return params
        
        # Print progress every 100 attempts so you know it's working
        if attempts % 100 == 0:
            print(f"Searched {attempts} systems... no strong chaos yet.")
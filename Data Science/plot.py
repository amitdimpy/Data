import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

a = np.linspace(0, 2 * np.pi, 100)
plt.figure(figsize=(10, 6))
b = np.sin(a)
c = np.cos(a)
# Plot the sine wave (blue line)
plt.plot(a, b, label='Sine Wave', color='blue', linestyle='-', linewidth=5)
# Plot the cosine wave (red dashed line)
plt.plot(a, c, label='Cosine Wave', color='red', linestyle='--', linewidth=5)
# 3. Customize the Plot (Optional but Recommended)
plt.title('Sine and Cosine Waves')
plt.xlabel('Angle (Radians)')
plt.ylabel('Amplitude')
plt.legend() # Show the legend with our labels
plt.grid(True,color='b') # Add a grid for readability

# Set limits for better viewing (optional)
plt.xlim(0, 2 * np.pi)
plt.ylim(-1.2, 1.2)
plt.show()
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Load the image
img = plt.imread("a.jpg")

width = img.shape[0]
height = img.shape[1]

print(f"Original image shape: {img.shape}")

# Reshape the image to a 2D array of pixels
img = img.reshape(width * height, 3)

# Perform KMeans clustering
kmeans = KMeans(n_clusters=3, n_init=10).fit(img)

# Predict the cluster labels of each pixel
labels = kmeans.predict(img)

# Get the cluster centers (dominant colors)
clusters = kmeans.cluster_centers_

print(f"Labels: {labels}")
print(f"Cluster centers (dominant colors): {clusters}")

# Create an empty image array
img2 = np.zeros((width, height, 3), dtype=np.uint8)

# Rebuild the quantized image
index = 0
for i in range(width):
    for j in range(height):
        label_of_pixel = labels[index]
        img2[i][j] = clusters[label_of_pixel].astype(np.uint8)  # Ensure the values are integers
        index += 1

# Display the quantized image
plt.imshow(img2)
plt.show()

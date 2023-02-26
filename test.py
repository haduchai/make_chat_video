from PIL import Image
import cv2
import numpy as np
# Front Image
filename = "asset/5 di'.png"

# Back Image
filename1 = 'asset/background2.jpg'

frontImage = Image.open(filename)
r, g, b, a = frontImage.split()
# Modify the values of the red channel

# Merge the color channels back into a single image
frontImage = Image.merge('RGBA', (b, g, r, a))

# Open Background Image
background = cv2.imread(filename1)
img_pil = Image.fromarray(background)
background = img_pil

# Calculate width to be at the center
width = (background.width - frontImage.width) // 2

# Calculate height to be at the center
height = (background.height - frontImage.height) // 2

# Paste the frontImage at (width, height)
background.paste(frontImage, (width, height), frontImage)

# convert to numpy array
background = np.array(background)

# Save this image
cv2.imwrite('result.jpg', background)


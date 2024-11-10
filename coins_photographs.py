import numpy as np
import cv2
import matplotlib.pyplot as plt

def av_pix(img, circles, size):
    av_value = []
    for coords in circles[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size, coords[0]-size:coords[0]+size])
        av_value.append(col)
    return av_value   

def get_radius(circles):
    radius = []
    for coords in circles[0,:]:
        radius.append(coords[2])    
    return radius
PATH=r"C:\Users\Mohamed\Downloads\19.1 capstone_coins.png"
# Load the image in grayscale and in color
img = cv2.imread(PATH, cv2.IMREAD_GRAYSCALE)
original_image = cv2.imread(PATH, 1)

# Check if images are loaded successfully
if img is None or original_image is None:
    print("Error: Image not found or cannot be loaded.")
else:
    # Apply Gaussian blur
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Detect circles in the image
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 120, param1=50, param2=27, minRadius=60, maxRadius=120)
    print(circles)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        count = 1
        for i in circles[0, :]:
            # Draw the outer circle
            cv2.circle(original_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(original_image, (i[0], i[1]), 2, (0, 0, 255), 3)
            count += 1

        # Calculate radii and brightness values
        radii = get_radius(circles)
        print(radii)
        bright_values = av_pix(img, circles, 20)
        print(bright_values)

        # Determine coin values based on brightness and radius
        values = []
        for a, b in zip(bright_values, radii):
            if a > 150 and b > 110:
                values.append(10)
            elif a > 150 and b <= 110:
                values.append(5)
            elif a < 150 and b > 110:
                values.append(2)
            elif a < 150 and b < 110:
                values.append(1)
        print(values)

        # Annotate the image with coin values and total
        count_2 = 0
        for i in circles[0, :]:
            cv2.putText(original_image, str(values[count_2]) + 'p', (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
            count_2 += 1
        cv2.putText(original_image, 'ESTIMATED TOTAL VALUE: ' + str(sum(values)) + 'p', (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255))

        # Use matplotlib to display the image
        plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
    else:
        print("No circles were detected.")

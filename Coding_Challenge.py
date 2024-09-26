import cv2
import numpy as np


# Load the image
image = cv2.imread('red.png')

# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range of red color in HSV
lower_red = np.array([0, 160, 160])
upper_red = np.array([10, 255, 255])

# Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lower_red, upper_red)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(image, image, mask=mask)

# Convert the image to grayscale
gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform Canny edge detection
edges = cv2.Canny(blur, 50, 150)

# Find contours in the edge image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on area or shape to retain only relevant ones
min_area_threshold = 50
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold]

# # Draw bounding boxes around the filtered contours
# for cnt in filtered_contours:
#     x, y, w, h = cv2.boundingRect(cnt)
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


# Fit lines to the detected cone contours
left_cones = []
right_cones = []

# Assuming the vehicle is driving along the center of the image,
# we can split the image into left and right halves
height, width = gray.shape
center_x = width // 2

for contour in filtered_contours:
    M = cv2.moments(contour)
    if M['m00'] == 0:
        continue
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    if cx < center_x:
        left_cones.append((cx, cy))
    else:
        right_cones.append((cx, cy))

# Fit a line to the left and right cone points
left_points = np.array(left_cones, dtype=np.int32)
right_points = np.array(right_cones, dtype=np.int32)

if len(left_points) > 1:
    [vx, vy, x, y] = cv2.fitLine(left_points, cv2.DIST_L2, 0, 0.01, 0.01)
    left_slope = vy / vx
    left_intercept = y - (left_slope * x)
else:
    left_slope = 0
    left_intercept = 0

if len(right_points) > 1:
    [vx, vy, x, y] = cv2.fitLine(right_points, cv2.DIST_L2, 0, 0.01, 0.01)
    right_slope = vy / vx
    right_intercept = y - (right_slope * x)
else:
    right_slope = 0
    right_intercept = 0

# Draw the lines on the image
for y in range(height):
    if left_slope != 0:
        left_x = int((y - left_intercept) / left_slope)
        if 0 <= left_x < width:
            cv2.circle(image, (left_x, y), 1, (0, 0, 255), -1)
    if right_slope != 0:
        right_x = int((y - right_intercept) / right_slope)
        if 0 <= right_x < width:
            cv2.circle(image, (right_x, y), 1, (0, 0, 255), -1)

# Save the resulting image
cv2.imwrite('answer.png', image)
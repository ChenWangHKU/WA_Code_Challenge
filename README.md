## Red Cone Detection and Lane Boundary Estimation

This Python script uses OpenCV to detect red cones in an image and estimate the boundaries of a lane based on the positions of these cones. Below is a summary of the methodology implemented in the code snippet:

1. **Image Preprocessing:**

   - Load the input image 'red.png'.
   - Convert the image from BGR to HSV color space.
   - Define the lower and upper HSV thresholds for detecting red color.
   - Threshold the HSV image to extract only the red areas.

   <img src="red.png" alt="Input" width="400"/>

2. **Edge Detection and Contour Extraction:**

   - Convert the resulting image to grayscale.
   - Apply Gaussian blur to reduce noise.
   - Perform Canny edge detection to identify edges.
   - Find contours in the edge-detected image.

3. **Filtering Contours and Cone Detection:**

   - Filter the detected contours based on area or shape to keep relevant ones.
   - Split the image into left and right halves assuming the vehicle is driving along the center.

4. **Fit Lines to Detected Cone Points:**

   - Fit lines to the points representing left and right cones.
   - Calculate the slope and intercept of the fitted lines.

5. **Draw Lane Boundaries:**

   - Using the calculated slopes and intercepts, draw lines representing the left and right boundaries of the lane.

6. **Save Resulting Image:**

   - Save the image with the detected red cones and estimated lane boundaries as 'answer.png'.

<img src="answer.png" alt="Output" width="400"/>

The script visualizes the estimated lane boundaries using circles along the vertical axis of the image, indicating the left and right boundaries. These boundaries are generated based on the positions of the red cones detected in the image.
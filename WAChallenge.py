import cv2 as cv
import numpy as np

# OpenCV by default reads in images in BGR format, but we need it in HSV format for better color distinction
read_image_bgr = cv.imread("red.png")

# Convert to HSV color space for better color filtering
img_hsv = cv.cvtColor(read_image_bgr, cv.COLOR_BGR2HSV)

# Threshold for low and high ranges of HSV red
lower_red_1 = np.array([0, 135, 135])
upper_red_1 = np.array([15, 255, 255])
lower_red_2 = np.array([159, 135, 135])
upper_red_2 = np.array([179, 255, 255])

mask_low = cv.inRange(img_hsv, lower_red_1, upper_red_1)
mask_high = cv.inRange(img_hsv, lower_red_2, upper_red_2)

# Combine the two masks
mask = cv.bitwise_or(mask_low, mask_high)

# Find the contours by smoothing out the image
mask = cv.erode(mask, None, iterations=1)
mask = cv.dilate(mask, None, iterations=1)
mask = cv.GaussianBlur(mask, (3,3), 0)

contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

cone_center_coords = []

for contour in contours:
    # Check if the contour shape resembles a cone
    epsilon = 0.04 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    if len(approx) >= 3 and len(approx) <= 10:
        # Get the center of the contour and draw a black dot
        M = cv.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cone_center_coords.append((cX, cY))

            cv.circle(read_image_bgr, (cX, cY), 3, (0, 0, 0), -1)


# Calculate average x-coordinate
avg_x = sum([x for x, y in cone_center_coords]) / len(cone_center_coords)

# Get image height, filter to only have points below half the image (which is where the cones are)
height, _, _ = read_image_bgr.shape
height = (height // 2) - (height // 4)

# Separate cone centers based on their x-coordinate
left_line = [point for point in cone_center_coords if point[0] < avg_x and point[1] > height]
right_line = [point for point in cone_center_coords if point[0] >= avg_x and point[1] > height]

# Function to compute line of best fit for the left line and right line of cones
def fit_line(points):
    n = len(points)
    sum_x = sum(p[0] for p in points)
    sum_y = sum(p[1] for p in points)
    sum_xx = sum(p[0]*p[0] for p in points)
    sum_xy = sum(p[0]*p[1] for p in points)

    m = (n*sum_xy - sum_x*sum_y) / (n*sum_xx - sum_x*sum_x)
    c = (sum_y - m*sum_x) / n

    return m, c

# Calculate lines of best fit
m_left, c_left = fit_line(left_line)
m_right, c_right = fit_line(right_line)

# Determine endpoints for lines
y1, y2 = 0, read_image_bgr.shape[0]  # Top to bottom of the image
x1_left = int((y1 - c_left) / m_left)
x2_left = int((y2 - c_left) / m_left)

x1_right = int((y1 - c_right) / m_right)
x2_right = int((y2 - c_right) / m_right)

# Draw lines on the image
cv.line(read_image_bgr, (x1_left, y1), (x2_left, y2), (0, 0, 255), 2)   # Draw left line in red
cv.line(read_image_bgr, (x1_right, y1), (x2_right, y2), (0, 0, 255), 2) # Draw right line in red

cv.imshow("Detected Cones", read_image_bgr)
cv.imwrite('answer.png', read_image_bgr)
cv.waitKey(0)
cv.destroyAllWindows()


# Previous Attempts
# -----------------------------------------------------------------------------------------------------------------
# gray_image = cv.cvtColor(read_image_bgr, cv.COLOR_BGR2GRAY)

# # We create a threshold image, and discard the type of threshold we use
# # This function takes any pixel that doesn't match our threshold of 110 (not less than/equal to) and turns it black
# _, threshold_image = cv.threshold(gray_image, 110, 225, cv.THRESH_BINARY)

# # Getting a list of all the contours (outlines) and relationships between contours
# # CHAIN_APPROX_SIMPLE makes it so only necessary points of the contour are stored, whereas
# # CHAIN_APPROX_NONE makes it so every point of the contour is stored; SIMPLE saves a lot of memory
# contours, hierarchy = cv.findContours(threshold_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# # Iterate through each contour
# for i, contour in enumerate(contours):
#     if i == 0:
#         continue # detection program considers entire image a shape, want to skip past this

#     epsilon = 0.01 * cv.arcLength(contour, True)
#     approx = cv.approxPolyDP(contour, epsilon, True)

#     cv.drawContours(read_image_bgr, contour, 0, (0, 0, 0), 4)

#     x, y, w, h = cv.boundingRect(approx)
#     x_mid = int(x + w/2)
#     y_mid = int(y + h/2)

#     if len(approx) == 3:
#         print("Triangle")


# cv.imshow("test2", read_image_bgr)


# cv.imshow("test1", threshold_image)
# cv.imshow("test", gray_image)


# cv.waitKey(0)
# cv.destroyAllWindows()

#-------------------------------------------------


# read_image_rgb = cv.cvtColor(read_image_bgr, cv.COLOR_BGR2RGB)

# # Define the RGB range [lower bounds, upper bounds]
# lower_bound = (205, 25, 25)
# upper_bound = (230, 50, 50)

# # Extract the dimensions
# height, width, _ = read_image_rgb.shape

# # Create an array to store coordinates within the RGB range
# coordinates_in_range = []

# for y in range(height):
#     for x in range(width):
#         # Fetch the RGB values
#         r, g, b = read_image_rgb[y, x]
        
#         # Check if the RGB values are within the defined range
#         if lower_bound[0] <= r <= upper_bound[0] and \
#            lower_bound[1] <= g <= upper_bound[1] and \
#            lower_bound[2] <= b <= upper_bound[2]:
#             coordinates_in_range.append((x, y))

# #print(coordinates_in_range)


# # Set a color and radius for the dots
# dot_color = (255, 255, 0)  # Green color
# dot_radius = 5  # Adjust as needed

# # Draw dots at the coordinates
# for (x, y) in coordinates_in_range:
#     cv.circle(read_image_rgb, (x, y), dot_radius, dot_color, -1)  # -1 means the circle will be filled

# # Display the image
# cv.imshow('Image with Dots', read_image_rgb)
# cv.waitKey(0)
# cv.destroyAllWindows()


# cv.imshow("Input_Image", read_image_bgr)
# print(read_image_bgr)
# cv.waitKey(0)
# cv.destroyAllWindows()
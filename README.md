# Wisconsin-Autonomous-Coding-Challenge-Sid-Ganesh
The public Git repository for my Wisconsin Autonomous Coding Challenge Fall 2023

## First Thoughts:
I am new to OpenCV, so my first initial thought in solving this problem was converting the image to a 2D array of RGB values, and then selecting the ones that represent red. This would technically give me the (x,y) values of the red cones within the image, which I could then use to draw the lines.
I opened up Adobe Photoshop and analyzed the RGB values of each of the cones. I found out that:
  - The Red Intensity Values range from 165-250
  - The Green Intensity Values range from 0-50
  - The Blue Intensity Values range from 10-60


<img src="https://github.com/SidGanesh41053/Wisconsin-Autonomous-Coding-Challenge-Sid-Ganesh/assets/131557045/a2c7e529-37f8-42ed-9f56-d9bca9eae78a" width="250" height="250">

<img src="https://github.com/SidGanesh41053/Wisconsin-Autonomous-Coding-Challenge-Sid-Ganesh/assets/131557045/709b844e-b8c3-4d14-a098-3736015f56e5" width="300" height="250">

However, when I created my array of coordinate tuples within the range of the RGB values, I had 12266 coordinates. Deciding that this was too much, I narrowed the range of the RGB values:  
  - The Red Intensity Values range from 205-230
  - The Green Intensity Values range from 25-50
  - The Blue Intensity Values range from 25-50

This narrowed down the number of coordinates to 3548.

When I plotted these points onto the image so that they would be on top of the cones, this is the image that was produced:

<img src="https://github.com/SidGanesh41053/Wisconsin-Autonomous-Coding-Challenge-Sid-Ganesh/assets/131557045/da486512-809c-4476-9fec-e1f69c933144" width="300" height="400">

I realized at this point that I would have to resort to clustering these points together so that I could draw my line, but this is a machine learning method I am unfamiliar with, so with the interest of completing the challenge in mind, I put off learning about the technique and decided to switch gears and use a different CV approach: shape detection and contours.

## Second Approach
I figured that if I could identify each of the cones as triangles, I could calculate the centroid of the triangle and plot the point coordinate, and then draw a line through the points.
### Resources Used
  - https://www.educba.com/opencv-inrange/
  - https://www.youtube.com/watch?v=Wl11eloYVm8
  - https://www.youtube.com/watch?v=Y7SkyY58aUw
  - https://docs.opencv.org/3.4/d0/d49/tutorial_moments.html
  - https://learnopencv.com/tag/cv2-moments/

This approach proved to be a lot more efficient. Once I had all of the centroids of the cones (used the help of ChatGPT to write this section of the code), I tried drawing lines connecting all the points, but didn't realize that it would end up doing this:
<img src=https://github.com/SidGanesh41053/Wisconsin-Autonomous-Coding-Challenge-Sid-Ganesh/assets/131557045/81865ff5-93d4-4e4b-888e-4ca6ca5de272 width="300" height="400">


I did end up using ChatGPT to write my line of best fit function after I separated the coordinates into the left and right lines of cones. Furthermore, it seems that the detection algorithm also drew centroids on many other detected triangles that were not cones in the picture, so I filtered out many of the coordinates that were below a certain y-coordinate threshold to have the best possible lines of best fit. 

<img src=https://github.com/SidGanesh41053/Wisconsin-Autonomous-Coding-Challenge-Sid-Ganesh/assets/131557045/0c92f72a-13a8-4c6c-8952-a13f57af4af1 width="300" height="400">

This was the result.
In the end, I used OpenCV and NumPy.

## Drawbacks of My Code
I believe that the main drawback of my code is that it is not generalized for any and every image that contains cones. This is because my work on this challenge was somewhat rushed. This code will really only work for the red.png input image given to us (though, it contains everything I believe is necessary to develop a successful general algorithm). However, it is definitely something to work on in the future, as it's generally accepted practice to have your code run anywhere.

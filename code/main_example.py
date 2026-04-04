# ChatGPT wwas used to help during coding, modification and trouble shooting.
#  OpenAI. (2026). ChatGPT (GPT-5 mini) [Large language model]. [https://openai.com/chatgpt](https://openai.com/chatgpt)


'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

from termcolor import colored #import all the tools
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import timeit


# Load the images you want to analyze

filenames = [
    "/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010017.jpg", #defining the path to the images
    "/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010018.jpg",
    "/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010019.jpg",
    "/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010021.jpg",
    "/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010022.jpg",
    "/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010023.jpg",
    "/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_SK658 Slobe ch010130.jpg",
]

# Enter the depth of each image (in the same order that the images are listed above; you can find these in the .csv file provided to you which is tilted: "Filenames and Depths for Students")

depths = [ #defining the depths
    15,
    200,
    1000,
    3000,
    5300,
    7000,
    9900
]

# Make the lists that will be used

images = [] #Initializing the storage for the data
white_counts = []
black_counts = []
white_percents = []

# Build the list of all the images you are analyzing

for filename in filenames: #load the photos 
    img = cv2.imread(filename, 0)
    images.append(img)

# For each image (until the end of the list of images), calculate the number of black and white pixels and make a list that contains this information for each filename.

for x in range(len(filenames)): #convert to binary
    _, binary = cv2.threshold(images[x], 127, 255, cv2.THRESH_BINARY)

    white = np.sum(binary == 255)
    black = np.sum(binary == 0)

    white_counts.append(white) #count pixels
    black_counts.append(black)

# Print the number of white and black pixels in each image.

print(colored("Counts of pixel by color in each image", "yellow"))
for x in range(len(filenames)):
    print(colored(f"White pixels in image {x}: {white_counts[x]}", "white")) #print counts
    print(colored(f"Black pixels in image {x}: {black_counts[x]}", "black"))
    print()

# Calculate the percentage of pixels in each image that are white and make a list that contains these percentages for each filename

for x in range(len(filenames)):
    white_percent = (
        100 * (white_counts[x] / (black_counts[x] + white_counts[x]))) #compute the white pixel percentage
    white_percents.append(white_percent)

# Print the filename (on one line in red font), and below that line print the percent white pixels and depth into the lung where the image was obtained

print(colored("Percent white px:", "yellow"))
for x in range(len(filenames)):
    print(colored(f'{filenames[x]}:', "red"))
    print(f'{white_percents[x]}% White | Depth: {depths[x]} microns') #print the percents with depths
    print()

'''Write your data to a .csv file'''

# Create a DataFrame that includes the filenames, depths, and percentage of white pixels
df = pd.DataFrame({ #save into the csv
    'Filenames': filenames,
    'Depths': depths,
    'White percents': white_percents
})

# Write that DataFrame to a .csv file

df.to_csv('Percent_White_Pixels.csv', index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")

'''the .csv writing subroutine ends here'''



################
# LECTURE 2: UNCOMMENT BELOW

# # Interpolate a point: given a depth, find the corresponding white pixel percentage

interpolate_depth = float(input(colored(
     "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

x = depths
y = white_percents

# # You can also use 'quadratic', 'cubic', etc.
# Linear interpolation
i_linear = interp1d(x, y, kind='linear')
y_linear = i_linear(interpolate_depth)

# Quadratic interpolation
i_quad = interp1d(x, y, kind='quadratic')
y_quad = i_quad(interpolate_depth)

# Point for code compatibility
interpolate_point = y_linear


print(colored(f'Linear interpolation: {y_linear}', "green"))
print(colored(f'Quadratic interpolation: {y_quad}', "cyan"))

depths_i = depths[:]
depths_i.append(interpolate_depth)
white_percents_i = white_percents[:]
white_percents_i.append(interpolate_point)


# # make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
fig, axs = plt.subplots(2, 1, figsize=(8, 10))


# Original data 

axs[0].scatter(depths, white_percents, marker='o', color='blue', label='Data')
axs[0].plot(depths, white_percents, color='blue', linestyle='-')  # optional line
axs[0].set_title('Depth vs % White Pixels (Original Data)')
axs[0].set_xlabel('Depth (microns)')
axs[0].set_ylabel('% White Pixels')
axs[0].grid(True)
axs[0].legend()


# Data + interpolated points

axs[1].scatter(depths, white_percents, marker='o', color='blue', label='Data')
axs[1].plot(depths, white_percents, color='blue', linestyle='-')  # optional line

# Linear interpolated point
axs[1].scatter(interpolate_depth, y_linear, color='red', s=100, label=f'Linear ({y_linear:.2f})')

# Quadratic interpolated point
axs[1].scatter(interpolate_depth, y_quad, color='green', s=100, label=f'Quadratic ({y_quad:.2f})')

axs[1].set_title('Depth vs % White Pixels with Interpolated Points')
axs[1].set_xlabel('Depth (microns)')
axs[1].set_ylabel('% White Pixels')
axs[1].grid(True)
axs[1].legend()


# # Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

from termcolor import colored
import cv2
import numpy as np
import pandas as pd

filenames = [
    r"/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010017.jpg", #defining the path to the images
    r"/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010018.jpg",
    r"/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010019.jpg",
    r"/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010021.jpg",
    r"/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010022.jpg",
    r"/Users/zain/Documents/GitHub/Module-3-Fibrosis_Luke_Zain/images/MASK_Sk658 Llobe ch010023.jpg",
]

depths = [15, 1000, 3000, 5300, 7000, 9900]

white_percents = []

print(colored("Counts of pixel by color in each image", "yellow"))

for i, (file, depth) in enumerate(zip(filenames, depths)):
    img = cv2.imread(file, 0)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    white = np.sum(binary == 255)
    black = np.sum(binary == 0)

    percent = 100 * white / (white + black)
    white_percents.append(percent)

    print(colored(f"White pixels in image {i}: {white}", "white"))
    print(colored(f"Black pixels in image {i}: {black}", "black"))
    print()
    print(colored(f"{file}:", "red"))
    print(f"{percent}% White | Depth: {depth} microns\n")

# Save to CSV
df = pd.DataFrame({
    'Filenames': filenames,
    'Depths': depths,
    'White percents': white_percents
})

df.to_csv('Percent_White_Pixels.csv', index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")

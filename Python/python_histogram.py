import cv2
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
from alive_progress import alive_bar
from fileinput import filename
from tkinter.filedialog import askopenfilename

def rgb_histogram(image, filename):
    r, g, b = image[:,:,0], image[:,:,1], image[:,:,2]

    r_hist, bins = np.histogram(r, bins=256, range=(0,256))
    g_hist, bins = np.histogram(g, bins=256, range=(0,256))
    b_hist, bins = np.histogram(b, bins=256, range=(0,256))

    bright = np.zeros(256)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            brightnes = sum(image[i,j,:])//3
            bright[brightnes] += 1

    bright_values = np.arange(0,256, dtype=int)
    df = pd.DataFrame({'brightness':bright_values, 'brightness_count':bright, 'red_count':r_hist, 'green_count':g_hist, 'blue_count':b_hist})

    data_preproc = pd.melt(df, id_vars=['brightness'], value_vars=['brightness_count', 'red_count', 'green_count', 'blue_count'], var_name='color', value_name='count')

    sns.set_style("darkgrid")
    sns.set(rc={"figure.figsize":(15, 6)})
    fig, ax = plt.subplots()

    sns.lineplot(x='brightness', y='count', hue='color', data=data_preproc, palette={'brightness_count': 'tab:gray', 'red_count': 'tab:red', 'green_count': 'tab:green', 'blue_count': 'tab:blue'}, linewidth=3, alpha=0)

    ax.fill_between(bright_values, r_hist, color='r', alpha=0.7)
    ax.fill_between(bright_values, g_hist, color='g', alpha=0.7)
    ax.fill_between(bright_values, b_hist, color='b', alpha=0.7)
    ax.fill_between(bright_values, bright, color='#c7c7c7')
    ax.set_xlabel('Brightness')
    ax.set_ylabel('Count')
    ax.set_title('RGB Histogram')
    red_lg = mpatches.Patch(color='red', label='Red')
    blue_lg = mpatches.Patch(color='blue', label='Blue')
    green_lg = mpatches.Patch(color='green', label='Green')
    gray_lg = mpatches.Patch(color='gray', label='Brightness')
    ax.legend(handles=[red_lg, blue_lg, green_lg, gray_lg])

    plt.savefig('histogram.png', dpi=300)
    print("Histogram saved as 'histogram.png'")

filename = askopenfilename(title='Select an image file', filetypes=[('Image files', '*.jpg *.jpeg *.png *.bmp *.tiff *.JPG')])
image = cv2.imread(filename)
height, width, _ = image.shape
total_pixels = height * width
with alive_bar(total_pixels) as bar:
    for i in range(height):
        for j in range(width):
            bar()
bar(height * width)
rgb_histogram(image, filename)

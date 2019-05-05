import os, sys
from skimage import io
import numpy as np
import webcolors
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def getOpaquePixels(image):
    # can be replaced with a single statement
    shape = image.shape
    pixelArray = []
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            pixel = image[x, y]
            if (pixel[3] == 255):
                pixelArray.append((pixel[0], pixel[1], pixel[2]))
    
    return pixelArray

def getStats(pixelArray):
    mean = tuple(map(np.mean, zip(*pixelArray)))
    median = tuple(map(np.median, zip(*pixelArray)))

    return median

def getClosestColor(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def getColorName(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = getClosestColor(requested_colour)
        actual_name = None
    return closest_name

def showColorFigures(colorA, colorB, colorNameA, colorNameB):
    fig, ax = plt.subplots()

    ax.set_xlim([-1, 2.5])
    ax.set_ylim([-1.25, 1.25])

    ax.add_artist(plt.Circle((0, 0), 0.7, color=np.array(colorA) / 255))
    ax.add_artist(plt.Circle((1.5, 0), 0.7, color=np.array(colorB) / 255))

    ax.add_artist(plt.text(x = 0, y = 0, horizontalalignment='center', verticalalignment='center', s=colorNameA, color='white', size='large'))
    ax.add_artist(plt.text(x = 1.5, y = 0, horizontalalignment='center', verticalalignment='center', s=colorNameB, color='white', size='large'))

    plt.show()

primaryImage = io.imread('primary.png')
primaryMedian = getStats(getOpaquePixels(primaryImage))
primaryColor = getColorName(primaryMedian)

secondaryImage = io.imread('secondary.png')
secondaryMedian = getStats(getOpaquePixels(secondaryImage))
secondaryColor = getColorName(secondaryMedian)

print("Primary Color: ")
print(primaryMedian)

print("Secondary Color: ")
print(secondaryMedian)

print("")
print("The colors are: ")
print(primaryColor + " and " + secondaryColor)

showColorFigures(primaryMedian, secondaryMedian, primaryColor, secondaryColor)

#exit()
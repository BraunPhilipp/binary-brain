# bInArI
import random
import numpy
import time
import requests
import re
from scipy import misc
import numpy as np
import itertools
import matplotlib.pyplot as plt

# Brain

HEIGHT = 8
WIDTH = 8
LENGTH = 8

ACT_WIDTH = WIDTH + (2 * HEIGHT) # adds diagonal spacing
ACT_LENGTH = LENGTH + (2 * HEIGHT)
ACT_HEIGHT = HEIGHT

def visualize(arr):
    for i in range(ACT_HEIGHT):
        for j in range(ACT_LENGTH):
            for k in range(ACT_WIDTH):
                #alpha = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                #letter = alpha[int((arr[i][j][k] * 35) / 255)]
                print(arr[i][j][k], end=' ')
            print(' ')
        print(' ')

def brain_activate(brain, inp):
    for x in range(WIDTH):
        for y in range(LENGTH):
            brain[0][x+HEIGHT][y+HEIGHT] = inp[x][y]
    return brain

def brain_propagate(brain):
    for x,y,z,i,j,k in itertools.product(range(HEIGHT),range(ACT_LENGTH),range(ACT_WIDTH),[-1,1],[-1,1],[-1,1]):
        if (HEIGHT>x+i>0 and ACT_LENGTH>y+j>0 and ACT_WIDTH>z+k>0):
            brain[x+i][y+j][z+k] += int (brain[x][y][z] / 26)
    return brain

def brain_fade(brain, rate):
    return brain / rate

def build_circuit(brain, circuit):
    for x,y,z in itertools.product(range(1, ACT_HEIGHT),range(1, ACT_LENGTH),range(1, ACT_WIDTH)):
        if (brain[x][y][z] > 25):
            circuit[x][y][z] = 1
    return circuit

def follow_circuit(brain, circuit):
    for x,y,z,i,j,k in itertools.product(range(ACT_HEIGHT),range(ACT_LENGTH),range(ACT_WIDTH),[-1,1],[-1,1],[-1,1]):
        if (ACT_HEIGHT>x+i>0 and ACT_LENGTH>y+j>0 and ACT_WIDTH>z+k>0):
            if (circuit[x+i][y+j][z+k] != 0 and brain[x][y][z] != 0):
                brain[x+i][y+j][z+k] = brain[x][y][z]
    return brain

def circuit_coord(circuit):
    coord = []
    for x,y,z in itertools.product(range(ACT_HEIGHT),range(ACT_LENGTH),range(ACT_WIDTH)):
        if (circuit[x][y][z] != 0):
            coord.append([x,y,z])

    x = [x[0] for x in coord]
    y = [x[1] for x in coord]
    z = [x[2] for x in coord]

    return [x,y,z]

# Get Data

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def download_image(url):
    with open("image.png", "wb") as file:
        response = requests.get(url)
        file.write(response.content)

def google_images(query):
    match = []
    for i in range(1,5):
        resp = requests.get("https://www.google.de/search?q="+str(query)+"&sa=X&biw=1159&bih=393&tbm=isch&ijn=4&start="+str(i*10)+"&tbs=itp:photo")
        pattern = re.compile(r"""data-src="(.*?)" """, re.IGNORECASE)
        match += pattern.findall(str(resp.content))
    return match

# Main Routine

brain = [[[0 for x in range(ACT_WIDTH)] for x in range(ACT_LENGTH)] for x in range(ACT_HEIGHT)]
circuit = [[[0 for x in range(ACT_WIDTH)] for x in range(ACT_LENGTH)] for x in range(ACT_HEIGHT)]

for image in google_images("polar+bear"):

    download_image(image)
    data = misc.imread("image.png").astype(np.float32)

    min_len = min(data.shape[:2])

    grey = []

    for row in data[:min_len]:
        grey.append(np.dot(row[:min_len], [0.299, 0.587, 0.114]))

    grey = misc.imresize(grey, (WIDTH,HEIGHT), interp='bilinear')

    brain = brain_activate(brain, grey)
    brain = follow_circuit(brain, circuit)
    brain = brain_propagate(brain)
    circuit = build_circuit(brain, circuit)

    #visualize(brain)
    visualize(circuit)

    # Reset Brain
    brain = [[[0 for x in range(ACT_WIDTH)] for x in range(ACT_LENGTH)] for x in range(ACT_HEIGHT)]

    # print(circuit_coord(circuit))

    #plt.plot(x2,fx2,'ro',markersize=1)
    # brain = brain_fade(brain, 2)
    # misc.imsave("image.png", grey)

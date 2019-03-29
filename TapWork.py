import math
from PIL import Image, ImageChops
import networkx as nx
import matplotlib
# matplotlib.use('TkAgg')
matplotlib.use('agg')
import matplotlib.pyplot as plt
import itertools
import cv2
import copy
import numpy as np
from tqdm import tqdm

def get_taps_demand(taps,houses):
    tap_demand = []
    houses_tap = []
    for tap in taps:
        tap_demand.append(0)

    for house in houses:
        lowest_distance = 99999999999999999
        house_tap = 0
        housex = house[1][0]
        housey = house[1][1]
        for tap in taps:
            tapx = tap[0]
            tapy = tap[1]
            tap_dist = math.sqrt((tapx-housex)**2+(tapy-housey)**2)
            if tap_dist < lowest_distance:
                lowest_distance = tap_dist
                house_tap = taps.index(tap)
        houses_tap.append((house_tap,work_done(lowest_distance)*house[0]))

    for tap in houses_tap:
        tap_demand[tap[0]]+=tap[1]
    return tap_demand

def work_done(distance):
    return distance**2

def total_differnces(tap_demands):
    total = 0
    index = 0
    for tap in tap_demands:
        index+=1
        for othertap in tap_demands[index:]:
            total += (othertap-tap)%1
    return total

def total_demand(tap_demands):
    total = 0
    for tap in tap_demands:
        total+=tap
    return total

def draw_network(houses,taps,image, display = True):
    pos = {}
    names = {}
    g = nx.Graph()
    for i in range(len(houses)):
        g.add_node(i)
        pos[i]=(houses[i][1][0],houses[i][1][1])
        names[i]=str(round(houses[i][0]))

    nx.draw_networkx(g, pos=pos, labels=names, node_color='r',node_size = 15,font_size=10)

    pos = {}
    names = {}
    g = nx.Graph()
    for i in range(len(houses)):
        g.add_node(i)
        pos[i]=(taps[i][0],taps[i][1])
        names[i]= str(i + 1)

    nx.draw_networkx(g, pos=pos, names=names, node_color='b',node_size=90,fontsize=8, font_color='w')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    fig1 = plt.gcf()
    plt.axis('off')
    plt.imshow(image)
#    plt.show()

    fig1.tight_layout(pad=0)
    fig1.canvas.draw()
    img = np.frombuffer(fig1.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig1.canvas.get_width_height()[::-1] + (3,))
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    crop_img = img[5:455, 94:544]
    # cv2.imwrite("figureTaps.png",crop_img)
    return crop_img

def total(demands):
    totalval = 0
    for demand in demands:
        totalval += demand
    return totalval

def greedy_brute(houses,amount_of_taps,grid_size):
    total_tick = amount_of_taps*grid_size[0]*grid_size[1]
    happy_taps = []
    stored_taps = []
    possible_coords = []

    for x in range(grid_size[0] + 1):
        for y in range(grid_size[1] + 1):
            possible_coords.append((x, y))

    with tqdm(total=total_tick) as t:
        for tap_placed in range(amount_of_taps):
            min_total_differnces = 999999999999999
            happy_taps = [0]
            for possible_coord in possible_coords:
                t.update(1)
                taps = list(copy.copy(stored_taps))
                taps.append(possible_coord)

                tap_demand = get_taps_demand(taps, houses)
                total_differnce = total_demand(tap_demand)

                if total_differnce == min_total_differnces:
                    happy_taps[0] = possible_coord

                if total_differnce < min_total_differnces:
                    happy_taps[0] = possible_coord

                    min_total_differnces = total_differnce
            stored_taps.append(happy_taps[-1])
    return stored_taps
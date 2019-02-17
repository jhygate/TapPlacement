import math
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import cv2



taps = [(29,29),(10,10)]
houses = [[4,(10,10)],[7,(29,29)],[8,(18,6)],[15,(12,16)],[6,[23,20]],[7,[6,19]]]





def get_taps_demand(taps,houses):
    tap_demand = []
    houses_tap = []
    for tap in taps:
        tap_demand.append(0)

    for house in houses:
        # print(house)
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

    # print(houses_tap)
    # print(tap_demand)
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

# taps_d = get_taps_demand(taps,houses)
# print(total_differnces(taps_d))
#


# tick = 0
# for x1 in range(15):
#     print(tick/810000)
#     for y1 in (range(30)):
#         for x2 in (range(30)):
#             for y2 in (range(30)):
#                 # print(x1,y1,x2,y2)
#                 tick += 1
#                 taps = [[x1, y1], [x2, y2]]
#                 tap_demand = get_taps_demand(taps, houses)
#                 total_differnce = total_demand(tap_demand)
#                 if total_differnce < min_total_differnces:
#                     happy_taps = []
#                     happy_taps.append(taps)
#                     min_total_differnces = total_differnce
#                 if total_differnce == min_total_differnces:
#                     happy_taps.append(taps)


# print(happy_taps)
# print(min_total_differnces)

taps = [[18,16],[29,29]]

def draw_network(houses,taps,image = "null"):
    pos = {}
    names = []
    edges = []
    for i in range(len(houses)):
        pos[str(houses[i][0])]=(houses[i][1][0],houses[i][1][1])
        edges.append((str(houses[i][0]),str(houses[i][0])))
    print(pos)
    print(edges)

    G = nx.Graph()
    G.add_edges_from(edges)

    nx.draw_networkx(G, pos=pos, node_color='r',node_size = 15,font_size=10)

    pos = {}
    edges = []
    for i in range(len(taps)):
        pos[(i+1)]=(taps[i][0],taps[i][1])
        print(pos)
        edges.append((i+1,i+1))
    print(pos)
    print(edges)

    G = nx.Graph()
    G.add_edges_from(edges)

    nx.draw_networkx(G, pos=pos, node_color='b',node_size=30,fontsize=50)
    # G.add_edges_from([(1, 1), (2, 2)])
    # pos = {1: (taps[0][0], taps[0][1]), 2: (taps[1][0], taps[1][1])}
    # #
    # nx.draw_networkx(G, pos=pos, node_color='b')
    print(image)
    if image != "null":
        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
    plt.show()


import copy

taps = [(10, 16), (18, 6), (19, 19)]
demands = get_taps_demand(taps,houses)
print(demands)

print(total_demand(demands))

taps = [(10, 16), (10,10), (19, 19)]
demands = get_taps_demand(taps,houses)
print(demands)

print(total_demand(demands))

def total(demands):
    totalval = 0
    for demand in demands:
        totalval += demand
    return totalval

def greedy_brute(houses,amount_of_taps,grid_size,image="null"):
    tick = 0
    total_tick = amount_of_taps*grid_size[0]*grid_size[1]
    happy_taps = []
    stored_taps = []
    possible_coords = []

    for x in range(grid_size[0] + 1):
        for y in range(grid_size[1] + 1):
            possible_coords.append((x, y))

    for tap_placed in range(amount_of_taps):
        min_total_differnces = 999999999999999
        happy_taps = []
        for possible_coord in possible_coords:
            tick += 1
            if tick % (int(total_tick/1000)) == 0:
                print(tick*100/total_tick)
            taps = list(stored_taps)
            taps.append(possible_coord)

            tap_demand = get_taps_demand(taps, houses)
            total_differnce = total_demand(tap_demand)

            if total_differnce == min_total_differnces:
                happy_taps.append(taps)

            if total_differnce < min_total_differnces:
                happy_taps = []
                happy_taps.append(possible_coord)
                min_total_differnces = total_differnce

        stored_taps.append(happy_taps[-1])
    draw_network(houses, stored_taps,image)




def brute_tap_position(houses,amount_of_taps,grid_size,image="null"):


    min_total_differnces = 999999999999999
    happy_taps = []
    possible_coords = []

    for x in range(grid_size[0]+1):
        for y in range(grid_size[1]+1):
            possible_coords.append((x, y))





    pairs = list(itertools.combinations_with_replacement(possible_coords,amount_of_taps))
    print(pairs[-1])
    total_ticks = (len(list(copy.copy(pairs))))
    #total_ticks = (grid_size[0]**(2*amount_of_taps))
    print(total_ticks)
    tick = 0

    for pair in pairs:

        tick += 1
        if tick % (int(total_ticks/1000)) == 0:
            print((tick / total_ticks)*100)
        taps = pair
        tap_demand = get_taps_demand(taps, houses)
        total_differnce = total_demand(tap_demand)


        if total_differnce == min_total_differnces:
            happy_taps.append(taps)


        if total_differnce < min_total_differnces:
            happy_taps = []
            happy_taps.append(taps)
            min_total_differnces = total_differnce

    print(happy_taps)

    for gtaps in happy_taps:
        draw_network(houses, gtaps,image=image)



#brute_tap_position(houses,3,(20,20))






import pygame, random
import numpy as np

    
def Solve(part_map, en_map, now, size_x, size_y):
    now_coord = [int(now[0]/2), int(now[1]/2)]
    correct_path = []
    new_path = []
    before = now_coord
    is_searched = 0
    #for x in range(1, self.size_x+1):
        #for y in range(1, self.size_y+1):
    answer_path = route(part_map, (size_x - 1, size_y - 1)) # 도착점 - 시작점
    now_path = route(part_map, now_coord) # 현재위치 - 시작점

    for x in answer_path:
        for y in now_path:
            if (x[0] == y[0]) and (x[1] == y[1]):
                cross_point = x
                is_searched = 1
                break
        if is_searched:
            break

    for x in answer_path:
        if (x[0] == cross_point[0]) and (x[1] == cross_point[1]):
            break
        else:
            correct_path.append(x)
    
    for x in now_path:
        new_path.append(x)
        if (x[0] == cross_point[0]) and (x[1] == cross_point[1]):
            break
    correct_path.reverse()
    final_path = new_path + correct_path

    for now in final_path:
        #print(now[0]*2 + 1, now[1] * 2 + 1)
        #print(now[0] + before[0] + 1, now[1] + before[1] + 1)
        en_map[now[0]*2 + 1, now[1]*2 + 1] = 2
        en_map[now[0] + before[0] + 1, now[1] + before[1] + 1] = 2
        before = now

    return en_map

def route(part_map, now):
    now_coord = now
    is_startpoint = 1
    tem_route = []
    while is_startpoint: # 시작지점부터 출구까지 경로
        tem_route.append(now_coord)

        before_coord = part_map[now_coord[0], now_coord[1]]

        #en_map[now_coord[0]*2 + 1, now_coord[1]*2 + 1] = 2
        #en_map[before_coord[0] + now_coord[0] + 1, before_coord[1] + now_coord[1] + 1] = 2

        if now_coord[0] == 0 and now_coord[1] == 0:
            is_startpoint = 0

        now_coord = before_coord
    
    return tem_route

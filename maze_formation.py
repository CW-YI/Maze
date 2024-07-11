import numpy as np
import pygame, random
import time
from datetime import date
from maze_solve import Solve

BLACK =      (  0,   0,   0)
WHITE =      (255, 255, 255)
GOLD =       (255, 191,   0)
BRIGHTGOLD = (255, 220, 115)
DARKGOLD =   (166, 124,   0)
BEIGE =      (248, 233, 200)
GREYBLUE =   (152, 175, 183)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

size_x = 40
size_y = 40

WINDOWWIDTH = size_x*25
WINDOWHEIGHT = size_y*20 + 10


class Maze(object):
    def __init__(self, level):
        self.level = level
        if self.level == 'easy': # easy → 지나온 길 표시
            self.color = BRIGHTGOLD
        else: # 나머지 → 지나온 길 표시X
            self.color = WHITE

        self.map = np.ndarray([size_x, size_y, 2], np.int64) # 기본 미로 방배열
        self.map[::] = -1 
        self.visited = [] # 방문 배열
        self.location = [0, 0] # 현재 위치 - 미로 형성

        self.start_time = time.time()
        self.Gameoff = 0 # 미로 클리어 판단 여부
        self.is_solved = 0 # solve 버튼 클릭 판단 여부
        
        while True:
            self.map[0, 0] = 0 
            self.location = self.go_next(self.location, self.map, self.visited) # 미로 생성
            if self.location == None: # 현재 위치가 없을 때까지
                break
        

    def maze_start(self):
        final_map = self.plus_wall(self.draw_map(self.map)) # 화면에 출력할 미로 생성
        DISPLAYSURF.fill(GREYBLUE)
        self.print_map(final_map) # 화면에 미로 출력
        self.maze_menu()
        return final_map, 1

    def random_pick(self, select):
        return select[random.randint(0, len(select) - 1)]

    def check_next(self, loc, map):
        next = []
        w = map.shape[0] 
        h = map.shape[1]
        if loc[0] > 0 and map[loc[0] - 1, loc[1]][0] < 0 : next.append([loc[0] - 1, loc[1]]) # 왼쪽 방향
        if loc[0] < h - 1 and map[loc[0] + 1, loc[1]][0] < 0 : next.append([loc[0] + 1, loc[1]]) # 오른쪽 방향
        if loc[1] > 0 and map[loc[0], loc[1] - 1][0] < 0 : next.append([loc[0], loc[1] - 1]) # 위쪽 방향
        if loc[1] < w - 1 and map[loc[0], loc[1] + 1][0] < 0 : next.append([loc[0], loc[1] + 1]) # 아래쪽 방향
        return next
        

    def go_next(self, loc, map, vit):
        nexts = self.check_next(loc, map) # 다음에 갈 수 있는 칸 탐색
        if len(nexts) > 0: # 다음에 갈 수 있는 칸이 있다면
            vit.append(loc) # 방문배열에 현재 위치 추가
            next = self.random_pick(nexts) # 다음에 갈 수 있는 칸 중 하나를 랜덤으로 픽
            map[next[0], next[1]] = loc # 미로의 다음 칸에 현재의 위치를 입력
            return next
        else: # 다음에 갈 수 있는 칸이 없다면
            if loc in vit:
                vit.remove(loc) # 방문배열에서 현재 위치 삭제
            if len(vit) == 0: # 방문배열의 길이가 0 = 더 이상 갈 곳이 없으면 None 반환
                return None
            return self.random_pick(vit) # 방문배열에서 랜덤으로 현재위치를 선택
        
    def draw_map(self, map):
        h = map.shape[0] * 2 + 1
        w = map.shape[1] * 2 + 1
        draw = np.ndarray([w, h], np.int64)
        draw[::] = 0

        for x in range(map.shape[0]):
            for y in range(map.shape[1]):
                pos = map[x, y]
                print(f'{pos} pos위치')
                draw[x * 2, y * 2] = 1 # 현재칸
                draw[pos[0] * 2, pos[1] * 2] = 1 # 이전칸
                draw[x + pos[0], y + pos[1]] = 1 # 사이칸
                #print(draw)

        draw[0, 1] = 1
        draw[len(draw)-2, len(draw)-3] = 1 # 출구 = 1
        return draw


    def print_map(self, draw):
        for x in range(len(draw) - 1):
            for y in range(len(draw) -1):
                if draw[x, y] == 0: # 벽 → 검은색
                    pygame.draw.rect(DISPLAYSURF, BLACK, (x*10, y*10, 10, 10))

                elif draw[x, y] == 1 and self.level == 'hard': # 하드모드
                    pygame.draw.rect(DISPLAYSURF, BLACK, (x*10, y*10, 10, 10)) # 전부 검은색으로 칠한 후
                    if now_coord[0]-10 <= x <= now_coord[0]+10:
                        if now_coord[1]-10 <= y <= now_coord[1]+10:
                            pygame.draw.rect(DISPLAYSURF, WHITE, (x*10, y*10, 10, 10)) # 현재위치에서 +- 10칸씩만 길 표시

                elif draw[x, y] == 1: # 길 → 하얀색
                    pygame.draw.rect(DISPLAYSURF, WHITE, (x*10, y*10, 10, 10))

                elif draw[x, y] ==2 and self.level == 'hard': # 하드모드
                    pygame.draw.rect(DISPLAYSURF, BLACK, (x*10, y*10, 10, 10))
                    if now_coord[0]-10 <= x <= now_coord[0]+10:
                        if now_coord[1]-10 <= y <= now_coord[1]+10:
                            pygame.draw.rect(DISPLAYSURF, GREYBLUE, (x*10, y*10, 10, 10))

                elif draw[x, y] ==2: # solve route → 파란색
                    pygame.draw.rect(DISPLAYSURF, GREYBLUE, (x*10, y*10, 10, 10))                        

    
        pygame.draw.rect(DISPLAYSURF, GOLD, (now_coord[0]*10, now_coord[1]*10, 10, 10)) # 플레이어
        pygame.draw.rect(DISPLAYSURF, GOLD, (((len(draw)-2)*10, (len(draw)-3)*10, 10, 10))) # 종료지점

        pygame.display.update()
        

    def plus_wall(self, map):
        self.tem_map = np.ndarray([len(map) + 1, len(map) + 1 ], np.int64)
        self.tem_map[::] = 0
        for x in range(len(map)):
            for y in range(len(map)):
                self.tem_map[x+1, y+1] = map[x, y] # 테두리에 벽을 추가하기 위함

        return self.tem_map
     

    def move_player(self, map, key, now):
        next_coord = (now[0], now[1])

        if key == pygame.K_UP: # 위로
            if map[now[0], now[1]-1] == 1 or map[now[0], now[1]-1] == 2:
                next_coord = (now[0], now[1]-1)
        if key == pygame.K_DOWN: # 아래로
            if map[now[0], now[1]+1] == 1 or map[now[0], now[1]+1] == 2:
                next_coord = (now[0], now[1]+1)
        if key == pygame.K_LEFT: # 왼쪽
            if map[now[0]-1, now[1]] == 1 or map[now[0]-1, now[1]] == 2:
                next_coord = (now[0]-1, now[1])
        if key == pygame.K_RIGHT: # 오른쪽
            if map[now[0]+1, now[1]] == 1 or map[now[0]+1, now[1]] == 2:
                next_coord = (now[0]+1, now[1])
        
        pygame.draw.rect(DISPLAYSURF, self.color, (now[0]*10, now[1]*10, 10, 10))
        pygame.draw.rect(DISPLAYSURF, GOLD, ((next_coord[0]*10, next_coord[1]*10, 10, 10)))

        if next_coord == (len(map)-2, len(map)-3): # 출구에 도착했을때
            self.maze_clear() 
            self.Gameoff = 1 # 게임 종료 판단
            self.is_solved = 1 # solve 버튼 입력X

        return next_coord, self.Gameoff

    def maze_clear(self):
        self.end_time = time.time()
        text('Clear!', BLACK, None, WINDOWWIDTH - 100, 100, 50)
        time_record = round(self.end_time-self.start_time, 2) # 시간 기록
        text(f'{time_record}', BLACK, None, WINDOWWIDTH - 100, 200, 50)

        if self.is_solved: # solve를 사용했다면 기록 저장X
            text('with solve button', BLACK, None, WINDOWWIDTH - 100, 250 , 20)
        else: # 날짜, 난이도, 시간기록 순으로 메모장에 저장
            save = open("C:/Users/cwyi6/OneDrive/문서/python/maze/time_record.txt", "a")
            save.write(f'{date.today()}, {self.level}, {time_record}\n')
            save.close()

        pygame.display.update()

        
    def maze_menu(self):
        self.home = text('home', BLACK, None, WINDOWWIDTH - 100, WINDOWHEIGHT - 100, 40)
        self.solve = text('solve', BLACK, None, WINDOWWIDTH - 100, WINDOWHEIGHT - 200, 40)

    def maze_check_rect(self, pos):
        if self.home.collidepoint(pos): # 메인 화면으로
            return 1
        if self.solve.collidepoint(pos):
            if self.is_solved == 1: # solve는 한 번만 누를 수 있도록
                pass
            else:
                self.solve_maze()
                return 3

    def solve_maze(self):
        self.is_solved = 1
        self.solve_map = Solve(self.map, self.tem_map, now_coord, size_x, size_y) # 현재지점 - 도착지점 경로 찾기
        self.print_map(self.solve_map)


    def change_map(self):
        return self.solve_map # 경로(2)가 저장된 미로 배열로 바꾸기

class Title(object):
    def __init__(self):
        self.level = None
        DISPLAYSURF.fill(GREYBLUE)

        self.make_menu()

    def make_menu(self):
        text('MAZE', BLACK, None, WINDOWWIDTH/2, WINDOWHEIGHT/4, 220)
        self.start_game = text('Game Start', BLACK, None, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 - 10, 50)
        self.record = text('Record', BLACK, None, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 + 50, 50)
        self.exit = text('Exit', BLACK, None, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 + 110, 50)
        self.level_easy = text('Easy', BLACK, None, WINDOWWIDTH/2 - 100, (WINDOWHEIGHT/3)*2 - 60, 30)
        self.level_normal = text('Normal', BLACK, None, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 - 60, 30)
        self.level_hard = text('Hard', BLACK, None, WINDOWWIDTH/2 + 100, (WINDOWHEIGHT/3)*2 - 60, 30)

    def check_level(self):
        return self.level

    def main_check_rect(self, pos): # 메인화면 체크
        if self.start_game.collidepoint(pos): # 게임 시작
            return 1
        elif self.record.collidepoint(pos): # 기록 화면으로
            self.menu_record()
            return 2

        elif self.exit.collidepoint(pos):
            pygame.quit() # 게임 종료

        elif self.level_easy.collidepoint(pos): # 레벨 선택에 따른 색 변화
            self.level = 'easy'
            text('Easy', WHITE, BLACK, WINDOWWIDTH/2 - 100, (WINDOWHEIGHT/3)*2 - 60, 30)
            text('Normal', BLACK, GREYBLUE, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 - 60, 30)
            text('Hard', BLACK, GREYBLUE, WINDOWWIDTH/2 + 100, (WINDOWHEIGHT/3)*2 - 60, 30)
        
        elif self.level_normal.collidepoint(pos):
            self.level = 'normal'
            text('Easy', BLACK, GREYBLUE, WINDOWWIDTH/2 - 100, (WINDOWHEIGHT/3)*2 - 60, 30)
            text('Normal', WHITE, BLACK, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 - 60, 30)
            text('Hard', BLACK, GREYBLUE, WINDOWWIDTH/2 + 100, (WINDOWHEIGHT/3)*2 - 60, 30)

        elif self.level_hard.collidepoint(pos):
            self.level = 'hard'
            text('Easy', BLACK, GREYBLUE, WINDOWWIDTH/2 - 100, (WINDOWHEIGHT/3)*2 - 60, 30)
            text('Normal', BLACK, GREYBLUE, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 - 60, 30)
            text('Hard', WHITE, BLACK, WINDOWWIDTH/2 + 100, (WINDOWHEIGHT/3)*2 - 60, 30)

    def menu_record(self):
        self.save_file = []
        DISPLAYSURF.fill(GREYBLUE)
        text('Record', BLACK, None, WINDOWWIDTH/2, WINDOWHEIGHT/8, 100)
        self.menu_home = text('home', BLACK, None, WINDOWWIDTH - 100, 100, 40)

        with open('C:/Users/cwyi6/OneDrive/문서/python/maze/time_record.txt', encoding='utf8') as file: # 기록 불러오기
            for line in file:
                line = line.rstrip('\n') # 엔터로 끊기
                self.save_file.append(line) # 한줄씩 가져오기
            self.save_file.reverse() # 저장한 파일 뒤집기 → 가장 최근 기록이 앞에 오도록

            if len(self.save_file) <= 20: # 파일에 저장된 기록이 20보다 작다면 파일의 길이로 loop을 지정
                loop = len(self.save_file)
            else:
                loop = 20

            for x in range(loop):
                h = WINDOWHEIGHT/3 - 60
                if x<=9:
                    w = WINDOWWIDTH/4
                    num = x
                else:
                    w = WINDOWWIDTH/4 * 3
                    num = x-10
                text(f'{self.save_file[x]}', BLACK, None, w, h + (60*num), 30) # 최근기록 20개 화면에 출력
    
    def record_check_rect(self, pos): # 기록화면 체크
        if self.menu_home.collidepoint(pos): # 메인 화면으로
            return 1

def text(text, color, bgcolor, x, y, size):
        font = pygame.font.Font('Maze.ttf', size)
        surf = font.render(text, True, color, bgcolor)
        rect = surf.get_rect()
        rect.center = (x, y)
        DISPLAYSURF.blit(surf, rect)

        return rect

def main():
    while True:
        global FPSCLOCK, DISPLAYSURF, now_coord

        # on off (0,0) -> 메인화면 / (1,0) -> 게임 중 / (0,1) -> 게임화면, 게임중X
        is_start = 0 # 게임 시작 여부
        check = 0 # [1 → 메인화면, 3 → solve]
        screen = 0 # 현재 스크린 [0 → 메인화면, 1 → 게임화면, 2 → 기록화면]
        Gameoff = 0 # 게임 종류 여부 확인
        title = Title()


        while True:
            for event in pygame.event.get():
                
                if is_start == 1: # 게임 시작 - 미로 생성
                    Gamelevel = title.check_level()
                    if Gamelevel != None:
                        maze = Maze(Gamelevel)
                        now_coord = (0, 1) # 현재 위치 - 플레이어 움직임
                        #79, 78
                        final_map, screen = maze.maze_start() # 생성된 맵 저장, screen = 1 지정(게임 화면)
                        is_start = 0
                    else:
                        text(' Select A Level ', WHITE, None, WINDOWWIDTH/2, (WINDOWHEIGHT/3)*2 - 90, 25) # 레벨 선택X 
                        is_start = 0

                if event.type==pygame.QUIT:
                        pygame.quit() # 게임 종료

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if screen == 0: # 게임 시작X 메인화면 클릭
                         is_start = title.main_check_rect(event.pos) # 메뉴 클릭 [1 → 게임시작, 2 → 기록확인]
                         if is_start == 2:
                             screen = 2
                    if screen == 1: # 게임 화면 클릭
                        check = maze.maze_check_rect(event.pos)
                        if check == 1: # 메인화면으로
                            break
                    if screen == 2: # 기록 확인
                        check = title.record_check_rect(event.pos)
                        if check == 1: # 메인화면으로
                            break      

                
                if screen == 1 and Gameoff == 0 and event.type == pygame.KEYDOWN: 
                    if check == 3: # solve → final_map을 경로가 표시된 맵으로 교체
                        final_map = maze.change_map()

                    now_coord, Gameoff = maze.move_player(final_map, event.key, now_coord) # 플레이어 좌표

                    if Gamelevel == 'hard' or check == 3: # hard나 solve 선택 시 주기적으로 화면 출력
                        maze.print_map(final_map)
                
            if check == 1:
                break

            pygame.display.flip()

pygame.init()
pygame.key.set_repeat(100)

print('Game start')

FPSCLOCK = pygame.time.Clock() 
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
pygame.display.set_caption('MAZE GAME') 

main()
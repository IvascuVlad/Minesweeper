import pygame
import time
from random import randrange

window_width = 400
window_height = 500
number_of_blocks = 9
number_of_bombs = 2
game_over_flag = False
desired_time_in_seconds = 64
start_time_in_seconds = 0
start_counting_flag = False
lose_flag = False

input_number_of_blocks_text = "blocks"
input_number_of_blocks_flag = False
input_number_of_minutes_text = "minutes"
input_number_of_minutes_flag = False
input_number_of_bombs_text = "bombs"
input_number_of_bombs_flag = False
input_number_of_seconds_text = "seconds"
input_number_of_seconds_flag = False

hidden_matrix = []
visible_matrix = []

def generate_matrix():
    for i in range(number_of_blocks):
        aux_for_hidden = []
        aux_for_visible = []
        for j in range(number_of_blocks):
            # if i == 1 and j == 1 or i == 1 and j == 2 or i == 3 and j == 3 or  i == 1 and j == 4 or i == 5 and j == 3 or i == 8 and j == 8 or i == 5 and j == 6:
            #     aux_for_hidden.append("B")
            # else:
            aux_for_hidden.append(0)
            aux_for_visible.append(None)
        hidden_matrix.append(aux_for_hidden)
        visible_matrix.append(aux_for_visible)

def generate_matrix_game():
    aux_for_number_of_bombs = 0
    while aux_for_number_of_bombs < number_of_bombs:
        x = randrange(0, number_of_blocks)
        y = randrange(0, number_of_blocks)
        if hidden_matrix[x][y] == 0:
            hidden_matrix[x][y] = "B"
            aux_for_number_of_bombs += 1
    for i in range(number_of_blocks):
        for j in range(number_of_blocks):
            if hidden_matrix[i][j] != "B":
                if i - 1 > -1:
                    if j - 1 > -1:
                        if hidden_matrix[i - 1][j - 1] == "B":
                            hidden_matrix[i][j] += 1
                    if j + 1 < number_of_blocks:
                        if hidden_matrix[i - 1][j + 1] == "B":
                            hidden_matrix[i][j] += 1
                    if hidden_matrix[i - 1][j] == "B":
                        hidden_matrix[i][j] += 1
                #if pentru linia de deasupra
                if i + 1 < number_of_blocks:
                    if j - 1 > -1:
                        if hidden_matrix[i + 1][j - 1] == "B":
                            hidden_matrix[i][j] += 1
                    if j + 1 < number_of_blocks:
                        if hidden_matrix[i + 1][j + 1] == "B":
                            hidden_matrix[i][j] += 1
                    if hidden_matrix[i + 1][j] == "B":
                        hidden_matrix[i][j] += 1
                #if pentru linia de dedesubt
                if j - 1 > -1:
                    if hidden_matrix[i][j - 1] == "B":
                        hidden_matrix[i][j] += 1
                if j + 1 < number_of_blocks:
                    if hidden_matrix[i][j + 1] == "B":
                        hidden_matrix[i][j] += 1
                #if pentru linia curenta

pygame.init()

window = pygame.display.set_mode((window_width,window_height))

pygame.display.set_caption("Minesweeper")
icon  = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
full_square = pygame.image.load("REALE/t.png")
empty_square = pygame.image.load("empty_square.png")
empty_square = pygame.transform.scale(empty_square, (17,17))
one = pygame.image.load("REALE/1.png")
two = pygame.image.load("REALE/2.png")
three = pygame.image.load("REALE/3.png")
four = pygame.image.load("REALE/4.png")
five = pygame.image.load("REALE/5.png")
bomb = pygame.image.load("bomb.png")
flag = pygame.image.load("flag.png")
question_mark = pygame.image.load("question.png")
smiley_face = pygame.image.load("win_and_happy.png")
sad_face = pygame.image.load("sad.png")
happy_face = pygame.image.load("happy.png")

def drawGrid():
    top_left = (10, (window_height - window_width) + 10)
    top_right = (window_width - 10, (window_height - window_width) + 10)
    blockSize = int((top_right[0] - top_left[0]) / number_of_blocks)
    number_one = pygame.transform.scale(one, (blockSize,blockSize))
    number_two = pygame.transform.scale(two, (blockSize,blockSize))
    number_three = pygame.transform.scale(three, (blockSize,blockSize))
    number_four = pygame.transform.scale(four, (blockSize, blockSize))
    number_five = pygame.transform.scale(five, (blockSize, blockSize))
    bomb_trap = pygame.transform.scale(bomb, (blockSize,blockSize))
    for x in range(number_of_blocks):
        for y in range(number_of_blocks):
            rect = pygame.Rect(y*blockSize + top_left[0], x*blockSize + top_left[1],blockSize, blockSize)
            if hidden_matrix[x][y] == "B":
                pygame.draw.rect(window, (255, 0, 0), rect)
            else:
                pygame.draw.rect(window, (117,117,117), rect, 2)
            if isinstance(hidden_matrix[x][y],int):
                if hidden_matrix[x][y] == 1:
                    window.blit(number_one, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 2:
                    window.blit(number_two, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 3:
                    window.blit(number_three, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 4:
                    window.blit(number_four, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 5:
                    window.blit(number_five, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
            if hidden_matrix[x][y] == "B":
                window.blit(bomb_trap, (y * blockSize + top_left[0], x * blockSize + top_left[1]))

def draw_delimiters():
    top_left = (10, (window_height - window_width) + 10)
    top_right = (window_width - 10, (window_height - window_width) + 10)
    bottom_left = (10, window_height - 10)
    bottom_right = (window_width - 10, window_height - 10)
    black = pygame.Color(0,0,0)
    right_space_error = (top_right[0] - top_left[0]) - int((top_right[0] - top_left[0]) / number_of_blocks) * number_of_blocks + 1 #restul impartirii pentru dreapta
    bottom_space_error = (bottom_right[1] - top_right[1]) - int((bottom_right[1] - top_right[1]) / number_of_blocks) * number_of_blocks + 1 # restul impartirii pentru jos
    top_right = (top_right[0] - right_space_error,top_right[1])
    bottom_right = (bottom_right[0] - right_space_error,bottom_right[1] - bottom_space_error)
    bottom_left = (bottom_left[0], bottom_left[1] - bottom_space_error)
    pygame.draw.line(window, black, (bottom_left[0], bottom_left[1]), (bottom_right[0], bottom_right[1])) #linie jos
    pygame.draw.line(window, black, (top_left[0], top_left[1]), (top_right[0], top_right[1])) #linie sus
    pygame.draw.line(window, black, (top_left[0], top_left[1]), (bottom_left[0], bottom_left[1])) #linie stanga
    pygame.draw.line(window, black, (top_right[0], top_right[1]), (bottom_right[0], bottom_right[1])) #linie dreapta

    pygame.draw.line(window, black, (10, 10), (window_width - 10, 10))  # linie sus control
    pygame.draw.line(window, black, (10, (window_height - window_width) - 10), (window_width - 10, (window_height - window_width) - 10))  # linie jos control
    pygame.draw.line(window, black, (10, 10), (10, (window_height - window_width) - 10))  # linie stanga control
    pygame.draw.line(window, black, (window_width - 10, 10), (window_width - 10, (window_height - window_width) - 10))  # linie sus control

def drawBoxesInit():
    top_left = (10, (window_height - window_width) + 10)
    top_right = (window_width - 10, (window_height - window_width) + 10)
    blockSize = int((top_right[0] - top_left[0]) / number_of_blocks)
    block = pygame.transform.scale(full_square, (blockSize,blockSize))
    flag_for_bomb = pygame.transform.scale(flag, (blockSize,blockSize))
    question_for_bomb = pygame.transform.scale(question_mark, (blockSize,blockSize))
    for x in range(number_of_blocks):
        for y in range(number_of_blocks):
            if visible_matrix[x][y] == "F":
                window.blit(block, (y*blockSize + top_left[0], x*blockSize + top_left[1]))
                window.blit(flag_for_bomb, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
            elif visible_matrix[x][y] == "?":
                window.blit(block, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
                window.blit(question_for_bomb, (y * blockSize + top_left[0], x * blockSize + top_left[1]))
            elif visible_matrix[x][y] != "D":
                window.blit(block, (y * blockSize + top_left[0], x * blockSize + top_left[1]))

def process_click(event):
    global game_over_flag
    global start_counting_flag
    global start_time_in_seconds
    global input_number_of_blocks_flag
    global input_number_of_bombs_flag
    global input_number_of_minutes_flag
    global input_number_of_seconds_flag
    global input_number_of_blocks_text
    global input_number_of_bombs_text
    global input_number_of_minutes_text
    global input_number_of_seconds_text
    global lose_flag
    top_left = (10, (window_height - window_width) + 10)
    top_right = (window_width - 10, (window_height - window_width) + 10)
    bottom_right = (window_width - 10, window_height - 10)
    blockSize = int((top_right[0] - top_left[0]) / number_of_blocks)
    y_position = int((event.pos[0] - top_left[0]) / blockSize)
    x_position = int((event.pos[1] - top_left[1]) / blockSize)
    if not game_over_flag:
        if top_left[0] <= event.pos[0] and event.pos[0] <= bottom_right[0] and top_left[1] <= event.pos[1] and event.pos[1] <= bottom_right[1]:
            if visible_matrix[x_position][y_position] == None and event.button == 1:
                if hidden_matrix[x_position][y_position] != "B":
                    if hidden_matrix[x_position][y_position] == 0:
                        find_empty_neighbours(x_position, y_position)
                    visible_matrix[x_position][y_position] = "D"
                    if not start_counting_flag:
                        start_time_in_seconds = int(pygame.time.get_ticks() / 1000)
                    start_counting_flag = True
                else:
                    print("AI PIERDUT")
                    lose_flag = True
                    game_over_flag = True
            if event.button == 3:
                if visible_matrix[x_position][y_position] == None:
                    if not start_counting_flag:
                        start_time_in_seconds = int(pygame.time.get_ticks() / 1000)
                    start_counting_flag = True
                    visible_matrix[x_position][y_position] = "F"
                elif visible_matrix[x_position][y_position] == "F":
                    visible_matrix[x_position][y_position] = "?"
                elif visible_matrix[x_position][y_position] == "?":
                    visible_matrix[x_position][y_position] = None
    control_panel_x_coordinate = (10, window_width - 10)
    control_panel_y_coordinate = (10, window_height - window_width - 10)
    game_reset_x_coordinate = (control_panel_x_coordinate[1] - control_panel_x_coordinate[0]) / 2 - 10
    game_reset_y_coordinate = (control_panel_y_coordinate[1] - control_panel_y_coordinate[0]) / 2 - 10
    if event.button == 1 and game_reset_x_coordinate < event.pos[0] and event.pos[0] < game_reset_x_coordinate + 40 and game_reset_y_coordinate < event.pos[1] and event.pos[1] < game_reset_y_coordinate + 40:
        reset_game()
    input_number_of_blocks_coord = (10 + control_panel_x_coordinate[0], 10 + control_panel_y_coordinate[0],
                                    10 + control_panel_x_coordinate[0] + game_reset_x_coordinate / 2 - 25,
                                    10 + control_panel_y_coordinate[0] + game_reset_y_coordinate - 5)
    if event.button == 1 and input_number_of_blocks_coord[0] <= event.pos[0] and event.pos[0] <= \
            input_number_of_blocks_coord[2] and input_number_of_blocks_coord[1] <= event.pos[1] and event.pos[1] <= \
            input_number_of_blocks_coord[3]:
        print("input_number_of_blocks")
        input_number_of_blocks_text = ""
        input_number_of_blocks_flag = True
        input_number_of_bombs_flag = False
        input_number_of_minutes_flag = False
        input_number_of_seconds_flag = False

    input_number_of_bombs_coord = (control_panel_x_coordinate[0] + game_reset_x_coordinate / 2 - 5, 10 + control_panel_y_coordinate[0],control_panel_x_coordinate[0] + game_reset_x_coordinate - 30, 10 + control_panel_y_coordinate[0] + game_reset_y_coordinate - 5)
    if event.button == 1 and input_number_of_bombs_coord[0] <= event.pos[0] and event.pos[0] <= \
            input_number_of_bombs_coord[2] and input_number_of_bombs_coord[1] <= event.pos[1] and event.pos[1] <= \
            input_number_of_bombs_coord[3]:
        print("input_number_of_bombs")
        input_number_of_bombs_text = ""
        input_number_of_blocks_flag = False
        input_number_of_bombs_flag = True
        input_number_of_minutes_flag = False
        input_number_of_seconds_flag = False

    input_number_of_minutes_coord = (10 + control_panel_x_coordinate[0], 10 + control_panel_y_coordinate[0] + game_reset_y_coordinate + 5 ,10 + control_panel_x_coordinate[0] + game_reset_x_coordinate / 2 - 25,10 + control_panel_y_coordinate[0] + 2 * game_reset_y_coordinate)
    if event.button == 1 and input_number_of_minutes_coord[0] <= event.pos[0] and event.pos[0] <= \
            input_number_of_minutes_coord[2] and input_number_of_minutes_coord[1] <= event.pos[1] and event.pos[1] <= \
            input_number_of_minutes_coord[3]:
        print("input_number_of_minutes")
        input_number_of_minutes_text = ""
        input_number_of_blocks_flag = False
        input_number_of_bombs_flag = False
        input_number_of_minutes_flag = True
        input_number_of_seconds_flag = False

    input_number_of_seconds_coord = (control_panel_x_coordinate[0] + game_reset_x_coordinate / 2 - 5,10 + control_panel_y_coordinate[0] + game_reset_y_coordinate + 5, control_panel_x_coordinate[0] + game_reset_x_coordinate -30 , 10 + control_panel_y_coordinate[0] + 2 * game_reset_y_coordinate)
    if event.button == 1 and input_number_of_seconds_coord[0] <= event.pos[0] and event.pos[0] <= \
            input_number_of_seconds_coord[2] and input_number_of_seconds_coord[1] <= event.pos[1] and event.pos[1] <= \
            input_number_of_seconds_coord[3]:
        print("input_number_of_seconds")
        input_number_of_seconds_text = ""
        input_number_of_blocks_flag = False
        input_number_of_bombs_flag = False
        input_number_of_minutes_flag = False
        input_number_of_seconds_flag = True

def process_key(event):
    global input_number_of_blocks_text
    global input_number_of_blocks_flag
    global input_number_of_bombs_text
    global input_number_of_bombs_flag
    global input_number_of_minutes_text
    global input_number_of_minutes_flag
    global input_number_of_seconds_text
    global input_number_of_seconds_flag
    global number_of_blocks
    global number_of_bombs
    global desired_time_in_seconds
    if input_number_of_blocks_flag:
        if event.key == pygame.K_RETURN:
            print(input_number_of_blocks_text)
        elif event.key == pygame.K_BACKSPACE:
            input_number_of_blocks_text = input_number_of_blocks_text[:-1]
        else:
            input_number_of_blocks_text += event.unicode

    if input_number_of_bombs_flag:
        if event.key == pygame.K_RETURN:
            print(input_number_of_bombs_text)
        elif event.key == pygame.K_BACKSPACE:
            input_number_of_bombs_text = input_number_of_bombs_text[:-1]
        else:
            input_number_of_bombs_text += event.unicode

    if input_number_of_minutes_flag:
        if event.key == pygame.K_RETURN:
            print(input_number_of_minutes_text)
        elif event.key == pygame.K_BACKSPACE:
            input_number_of_minutes_text = input_number_of_minutes_text[:-1]
        else:
            input_number_of_minutes_text += event.unicode

    if input_number_of_seconds_flag:
        if event.key == pygame.K_RETURN:
            print(input_number_of_seconds_text)
        elif event.key == pygame.K_BACKSPACE:
            input_number_of_seconds_text = input_number_of_seconds_text[:-1]
        else:
            input_number_of_seconds_text += event.unicode

def find_empty_neighbours(x, y):
    nextx = [-1, -1, -1, 0, 0, 1, 1, 1]
    nexty = [-1, 0, 1, -1, 1, -1, 0, 1]
    if x >= 0 and x < number_of_blocks and y >= 0 and y < number_of_blocks and hidden_matrix[x][y] == 0 and visible_matrix[x][y] == None:
        visible_matrix[x][y] = "D"
        for i in range(8):
            if x + nextx[i] >= 0 and x + nextx[i] < number_of_blocks and y + nexty[i] >= 0 and y + nexty[i] < number_of_blocks:
                if isinstance(hidden_matrix[x + nextx[i]][y + nexty[i]],int) and hidden_matrix[x + nextx[i]][y + nexty[i]] > 0 and hidden_matrix[x + nextx[i]][y + nexty[i]] < 6:
                    visible_matrix[x + nextx[i]][y + nexty[i]] = "D"
            find_empty_neighbours(x + nextx[i], y + nexty[i])

def game_over():
    global game_over_flag
    global start_counting_flag
    if game_over_flag:
        reveal_all_bombs()
        start_counting_flag = False
        return True
    number_of_correct_flags = 0
    for i in range(number_of_blocks):
        for j in range(number_of_blocks):
            if hidden_matrix[i][j] != "B" and visible_matrix[i][j] == "D":
                number_of_correct_flags += 1
    if number_of_correct_flags == number_of_blocks*number_of_blocks - number_of_bombs:
        game_over_flag = True
        start_counting_flag = False
        print("AI CASTIGAT")
        return True
    else:
        return False

def reveal_all_bombs():
    for i in range(number_of_blocks):
        for j in range(number_of_blocks):
            if hidden_matrix[i][j] == "B":
                visible_matrix[i][j] = "D"

def draw_control_panel():
    global input_number_of_blocks_text
    global input_number_of_bombs_text
    global input_number_of_minutes_text
    global input_number_of_seconds_text
    global lose_flag
    global game_over_flag
    control_panel_x_coordinate = (10, window_width - 10)
    control_panel_y_coordinate = (10, window_height - window_width - 10)
    game_reset = pygame.transform.scale(smiley_face, (40, 40))
    if lose_flag:
        game_reset = pygame.transform.scale(sad_face, (40, 40))
    if game_over_flag and not lose_flag:
        game_reset = pygame.transform.scale(happy_face, (40, 40))
    game_reset_x_coordinate = (control_panel_x_coordinate[1] - control_panel_x_coordinate[0]) / 2 - 10
    game_reset_y_coordinate = (control_panel_y_coordinate[1] - control_panel_y_coordinate[0]) / 2 - 10
    window.blit(game_reset,(game_reset_x_coordinate,game_reset_y_coordinate))

    input_number_of_blocks = pygame.Rect(10 + control_panel_x_coordinate[0], 10 + control_panel_y_coordinate[0], game_reset_x_coordinate / 2 - 25, game_reset_y_coordinate - 5)
    font = pygame.font.SysFont('Consolas', int(game_reset_y_coordinate - 15))
    txt_surface_blocks = font.render(input_number_of_blocks_text, True, (0,0,0))
    window.blit(txt_surface_blocks, (input_number_of_blocks.x + 5, input_number_of_blocks.y + 5))
    pygame.draw.rect(window, (0,0,0), input_number_of_blocks, 2)

    input_number_of_minutes = pygame.Rect(10 + control_panel_x_coordinate[0], 10 + control_panel_y_coordinate[0] + game_reset_y_coordinate + 5 ,game_reset_x_coordinate / 2 - 25, game_reset_y_coordinate - 5)
    txt_surface_minutes = font.render(input_number_of_minutes_text, True, (0, 0, 0))
    window.blit(txt_surface_minutes, (input_number_of_minutes.x + 5, input_number_of_minutes.y + 5))
    pygame.draw.rect(window, (0, 0, 0), input_number_of_minutes, 2)

    input_number_of_bombs = pygame.Rect(control_panel_x_coordinate[0] + game_reset_x_coordinate / 2 - 5, 10 + control_panel_y_coordinate[0],game_reset_x_coordinate / 2 - 25, game_reset_y_coordinate - 5)
    txt_surface_bombs = font.render(input_number_of_bombs_text, True, (0, 0, 0))
    window.blit(txt_surface_bombs, (input_number_of_bombs.x + 5, input_number_of_bombs.y + 5))
    pygame.draw.rect(window, (0, 0, 0), input_number_of_bombs, 2)

    input_number_of_seconds = pygame.Rect(control_panel_x_coordinate[0] + game_reset_x_coordinate / 2 - 5,10 + control_panel_y_coordinate[0] + game_reset_y_coordinate + 5,game_reset_x_coordinate / 2 - 25, game_reset_y_coordinate - 5)
    txt_surface_seconds = font.render(input_number_of_seconds_text, True, (0, 0, 0))
    window.blit(txt_surface_seconds, (input_number_of_seconds.x + 5, input_number_of_seconds.y + 5))
    pygame.draw.rect(window, (0, 0, 0), input_number_of_seconds, 2)

def draw_time():
    global start_time_in_seconds
    global desired_time_in_seconds
    control_panel_x_coordinate = (10, window_width - 10)
    control_panel_y_coordinate = (10, window_height - window_width - 10)
    game_reset_x_coordinate = (control_panel_x_coordinate[1] - control_panel_x_coordinate[0]) / 2
    game_reset_y_coordinate = (control_panel_y_coordinate[1] - control_panel_y_coordinate[0]) / 2
    font = pygame.font.SysFont('Consolas', 50)
    text = ""
    if start_counting_flag:
        aux_for_seconds = desired_time_in_seconds - (int(pygame.time.get_ticks() / 1000) - start_time_in_seconds)
        aux_for_minutes = int(aux_for_seconds / 60)
        aux_for_seconds = int(aux_for_seconds % 60)
        if aux_for_seconds == -1:
            aux_for_seconds = 60
            aux_for_minutes -= 1
        if aux_for_minutes < 10:
            aux_for_minutes = " " + str(aux_for_minutes)
        else:
            aux_for_minutes = str(aux_for_minutes)
        if aux_for_seconds < 10:
            aux_for_seconds = "0" + str(aux_for_seconds)
        else:
            aux_for_seconds = str(aux_for_seconds)
        text = aux_for_minutes + ":" + aux_for_seconds
    window.blit(font.render(text, True, (0, 0, 0)), (game_reset_x_coordinate + 50, game_reset_y_coordinate - 10))

def reset_game():
    global hidden_matrix
    global visible_matrix
    global number_of_blocks
    global number_of_bombs
    global desired_time_in_seconds
    global game_over_flag
    global start_time_in_seconds
    global start_counting_flag
    global input_number_of_blocks_text
    global input_number_of_blocks_flag
    global input_number_of_minutes_text
    global input_number_of_minutes_flag
    global input_number_of_bombs_text
    global input_number_of_bombs_flag
    global input_number_of_seconds_text
    global input_number_of_seconds_flag
    global lose_flag
    if input_number_of_bombs_text != "bombs":
        number_of_bombs = int(input_number_of_bombs_text)
    if input_number_of_blocks_text != "blocks":
        number_of_blocks = int(input_number_of_blocks_text)
    if input_number_of_seconds_text != "seconds" or input_number_of_minutes_text != "minutes":
        desired_time_in_seconds = 0
        if input_number_of_seconds_text != "seconds":
            desired_time_in_seconds += int(input_number_of_seconds_text)
        if input_number_of_minutes_text != "minutes":
            desired_time_in_seconds += int(input_number_of_minutes_text) * 60
    hidden_matrix = []
    visible_matrix = []
    generate_matrix()
    generate_matrix_game()
    game_over_flag = False
    start_time_in_seconds = 0
    start_counting_flag = False
    #input_number_of_blocks_text = "blocks"
    input_number_of_blocks_flag = False
    #input_number_of_minutes_text = "minutes"
    input_number_of_minutes_flag = False
    #input_number_of_bombs_text = "bombs"
    input_number_of_bombs_flag = False
    #input_number_of_seconds_text = "seconds"
    input_number_of_seconds_flag = False
    lose_flag = False

running = True

generate_matrix()

generate_matrix_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            process_click(event)
        elif event.type == pygame.KEYDOWN:
            process_key(event)

    window.fill((192,192,192))
    draw_delimiters()
    drawGrid()
    drawBoxesInit()
    draw_control_panel()
    draw_time()
    game_over()
    pygame.display.update()
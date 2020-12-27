import pygame

window_width = 400
window_height = 500
number_of_blocks = 9

hidden_matrix = []
visible_matrix = []
matrix_for_visited = []

def generate_matrix_game():
    for i in range(number_of_blocks):
        aux = []
        aux_for_hidden = []
        for j in range(number_of_blocks):
            if i == 1 and j == 1 or i == 1 and j == 2 or i == 3 and j == 3 or  i == 1 and j == 4 or i == 5 and j == 3 or i == 8 and j == 8 or i == 5 and j == 6:
                aux.append("B")
            else:
                aux.append(0)
            aux_for_hidden.append(None)
            matrix_for_visited.append(None)
        hidden_matrix.append(aux)
        visible_matrix.append(aux_for_hidden)
    for i in range(number_of_blocks):
        for j in range(number_of_blocks):
            if hidden_matrix[i][j] != "B":
                if i - 1 > 0:
                    if j - 1 > 0:
                        if hidden_matrix[i - 1][j - 1] == "B":
                            hidden_matrix[i][j] += 1
                    if j + 1 < number_of_blocks:
                        if hidden_matrix[i - 1][j + 1] == "B":
                            hidden_matrix[i][j] += 1
                    if hidden_matrix[i - 1][j] == "B":
                        hidden_matrix[i][j] += 1
                #if pentru linia de deasupra
                if i + 1 < number_of_blocks:
                    if j - 1 > 0:
                        if hidden_matrix[i + 1][j - 1] == "B":
                            hidden_matrix[i][j] += 1
                    if j + 1 < number_of_blocks:
                        if hidden_matrix[i + 1][j + 1] == "B":
                            hidden_matrix[i][j] += 1
                    if hidden_matrix[i + 1][j] == "B":
                        hidden_matrix[i][j] += 1
                #if pentru linia de dedesubt
                if j - 1 > 0:
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
            rect = pygame.Rect(x*blockSize + top_left[0], y*blockSize + top_left[1],
                               blockSize, blockSize)
            pygame.draw.rect(window, (117,117,117), rect, 2)
            if isinstance(hidden_matrix[x][y],int):
                if hidden_matrix[x][y] == 1:
                    window.blit(number_one, (x * blockSize + top_left[0], y * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 2:
                    window.blit(number_two, (x * blockSize + top_left[0], y * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 3:
                    window.blit(number_three, (x * blockSize + top_left[0], y * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 4:
                    window.blit(number_four, (x * blockSize + top_left[0], y * blockSize + top_left[1]))
                elif hidden_matrix[x][y] == 5:
                    window.blit(number_five, (x * blockSize + top_left[0], y * blockSize + top_left[1]))
            if hidden_matrix[x][y] == "B":
                window.blit(bomb_trap, (x * blockSize + top_left[0], y * blockSize + top_left[1]))

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
    for x in range(number_of_blocks):
        for y in range(number_of_blocks):
            if visible_matrix[x][y] == None:
                window.blit(block, (x*blockSize + top_left[0], y*blockSize + top_left[1]))

def process_click(position, button):
    top_left = (10, (window_height - window_width) + 10)
    top_right = (window_width - 10, (window_height - window_width) + 10)
    blockSize = int((top_right[0] - top_left[0]) / number_of_blocks)
    x_position = int((position[0] - top_left[0]) / blockSize)
    y_position = int((position[1] - top_left[1]) / blockSize)
    if visible_matrix[x_position][y_position] == None and button == 1:
        if hidden_matrix[x_position][y_position] != "B":
            if hidden_matrix[x_position][y_position] == 0:
                find_empty_neighbours(x_position, y_position)
            visible_matrix[x_position][y_position] = "D"
        else:
            print("AI PIERDUT")

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

running = True

generate_matrix_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # MOUSEBUTTONDOWN events have a pos and a button attribute
            # which you can use as well. This will be printed once per
            # event / mouse click.
            print('In the event loop:', event.pos, event.button)
            process_click(event.pos, event.button)

    window.fill((192,192,192))
    draw_delimiters()
    drawGrid()
    drawBoxesInit()
    pygame.display.update()
import pygame
import numpy as np

def draw_snake(screen, position, case_dim, facing):
    pos = pygame.Vector2(position[0] * case_dim + (case_dim//2), position[1] * case_dim + (case_dim//2))
    pygame.draw.circle(screen, "white", pos, case_dim - (case_dim//10))

    if facing=="left":
        right_eye_position = (pos.x - case_dim//2, pos.y - case_dim//2)
        left_eye_position = (pos.x - case_dim//2, pos.y + case_dim//2)
    elif facing=="right":
        right_eye_position = (pos.x + case_dim//2, pos.y + case_dim//2)
        left_eye_position = (pos.x + case_dim//2, pos.y - case_dim//2)
    elif facing=="up":
        right_eye_position = (pos.x + case_dim//2, pos.y - case_dim//2)
        left_eye_position = (pos.x - case_dim//2, pos.y - case_dim//2)
    elif facing=="down":
        right_eye_position = (pos.x - case_dim//2, pos.y + case_dim//2)
        left_eye_position = (pos.x + case_dim//2, pos.y + case_dim//2)
    
    pygame.draw.circle(screen, "black", right_eye_position, case_dim//10)
    pygame.draw.circle(screen, "black", left_eye_position, case_dim//10)

def draw_body(screen, body, case_dim):
    for position in body:
        pos = pygame.Vector2(position[0] * case_dim + (case_dim//2), position[1] * case_dim + (case_dim//2))
        pygame.draw.circle(screen, "white", pos, case_dim - (case_dim//10))

def draw_point(screen, position, case_dim):
    pos = pygame.Vector2(position[0] * case_dim + (case_dim//2), position[1] * case_dim + (case_dim//2))
    pygame.draw.circle(screen, "red", pos, (case_dim//2))

def update_position(position, facing, DIMS):
    x,y = position
    
    if facing=="left":
        x = (x-1)%DIMS[0]
    elif facing=="right":
        x = (x+1)%DIMS[0]
    elif facing=="up":
        y = (y-1)%DIMS[1]
    elif facing=="down":
        y = (y+1)%DIMS[1]

    return (x,y)

def update_movement(facing, last_move):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and last_move != "down":
        return "up"
    if keys[pygame.K_s] and last_move != "up":
        return "down"
    if keys[pygame.K_a] and last_move != "right":
        return "left"
    if keys[pygame.K_d] and last_move != "left":
        return "right"
    return facing

def spawn(position, body, DIMENSIONS):
    #define spawnpoint
    satisfied = False
    while not satisfied:
        x = np.random.randint(DIMENSIONS[0])
        y = np.random.randint(DIMENSIONS[1])
        satisfied = check_integrity((x,y), position, body)
    spawnpoint = (x,y)
    return spawnpoint

def check_integrity(pos1, pos_snake, body):
    for pos in body:
        if not (pos1[0]!=pos[0] or pos1[1]!=pos[1]):
            return False
    return (pos1[0]!=pos_snake[0] or pos1[1]!=pos_snake[1])
    
def check_no_bite(pos_snake, body):
    for pos in body:
        if pos_snake[0] == pos[0] and pos_snake[1] == pos[1]:
            return False
    return True


DIMENSIONS = (50,30)
COTE_CASE = 25

# pygame setup
pygame.init()
pygame.display.set_caption('SNAKE')
screen = pygame.display.set_mode((DIMENSIONS[0]*COTE_CASE, DIMENSIONS[1]*COTE_CASE))
clock = pygame.time.Clock()
game_going = False
running = True

font = pygame.font.Font('freesansbold.ttf', 32)
text_ng = font.render("New Game", True, "white")
ng_rect = text_ng.get_rect()
text_ex = font.render("Exit", True, "white")
ex_rect = text_ex.get_rect()

natural_color = (100, 100, 100)
hover_color = (130, 130, 130)

ng_btn_color = natural_color
ex_btn_color = natural_color




score = 0

while running:

    while game_going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_going = False
        
        screen.fill("black")
        
        if do_spawn:
            point_coords = spawn(position, body, DIMENSIONS)
            do_spawn = False
        
        draw_point(screen, point_coords, COTE_CASE)
        
        draw_body(screen, body, COTE_CASE)
        draw_snake(screen, position, COTE_CASE, facing)

        facing = update_movement(facing, last_move)

        if move_in == 0:
            last_position = position
            position = update_position(position, facing, DIMENSIONS)
            move_in = freeze_duration
            last_move = facing

            body.append(last_position)
            body.remove(body[0])

            if(position[0]==point_coords[0] and position[1]==point_coords[1]):
                #eats
                do_spawn = True
                body.append(position)
                score+=1
            else:
                keep = check_no_bite(position, body)
                if not keep:
                    game_going = False

            
        else :
            move_in-=1

        text_score = font.render(str(score), True, "red")
        score_rect = text_score.get_rect()
        score_rect.center = (score_rect.width//2 + 5 , score_rect.height//2 + 5)
        screen.blit(text_score, score_rect)

        #update scene and dt
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # code for lose screen
    screen.fill("black")
    w = screen.get_width()
    h = screen.get_height()

    btn_w = w//4
    btn_h = h//16
    pygame.draw.rect(screen, ng_btn_color, ((w-btn_w)//2, (h-btn_h)//2, btn_w, btn_h))
    ng_rect.center = (((w-btn_w)//2 + btn_w//2) , ((h-btn_h)//2 + btn_h//2))
    screen.blit(text_ng, ng_rect)

    pygame.draw.rect(screen, ex_btn_color, ((w-btn_w)//2, (h-btn_h)//2 + btn_h + 10, btn_w, btn_h))
    ex_rect.center = (((w-btn_w)//2 + btn_w//2) , ((h-btn_h)//2 + btn_h//2) + btn_h + 10)
    screen.blit(text_ex, ex_rect)

    if score>0:
        text_score = font.render("Score : "+str(score), True, "red")
        score_rect = text_score.get_rect()
        score_rect.center = (((w-btn_w)//2 + btn_w//2) , h//8)
        screen.blit(text_score, score_rect)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0]:
        if (w-btn_w)//2 <= mouse[0] <= (w-btn_w)//2 + btn_w:
            if (h-btn_h)//2 <= mouse[1] <= (h-btn_h)//2 + btn_h:
                #new game
                facing = "up"
                position = (DIMENSIONS[0]//2, DIMENSIONS[1]//2)
                freeze_duration = 10
                move_in = freeze_duration
                last_move = facing
                dt = 0
                do_spawn = True
                body = []
                score = 0

                game_going = True

            elif (h-btn_h)//2 + btn_h + 10 <= mouse[1] <= (h-btn_h)//2 + btn_h + 10 + btn_h:
                running = False
    else :
        if (w-btn_w)//2 <= mouse[0] <= (w-btn_w)//2 + btn_w:
            if (h-btn_h)//2 <= mouse[1] <= (h-btn_h)//2 + btn_h:
                ng_btn_color = hover_color
                ex_btn_color = natural_color
            elif (h-btn_h)//2 + btn_h + 10 <= mouse[1] <= (h-btn_h)//2 + btn_h + 10 + btn_h:
                ex_btn_color = hover_color
                ng_btn_color = natural_color
            else:
                ex_btn_color = natural_color
                ng_btn_color = natural_color
        else:
            ex_btn_color = natural_color
            ng_btn_color = natural_color

    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()
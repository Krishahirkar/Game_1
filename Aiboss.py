
import pygame
from random import randint

# Functions 
def display_score():
    current_time = pygame.time.get_ticks() - initial_time
    current_time = int(current_time/1000)
    score_surface = text_font.render(f'Score:{current_time}', False, (64,63,63))
    score_rect = score_surface.get_rect(center=(420,100))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 565:
                screen.blit(enemy_surface, obstacle_rect)
            else:
                screen.blit(enemy2_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 565:
        player_index += 0.1
        if player_index >= len(player_jump_list):
            player_index = 0
        player_surface = player_jump_list[int(player_index)]
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

#start
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Can you defeat them?")
clock = pygame.time.Clock()

score = 0
obstacle_rect_list = []
text_font = pygame.font.Font(None,50)   
initial_time = 0

# Backgrounds
sky_surface = pygame.image.load('game sky.jpg').convert()
sky_surface = pygame.transform.scale(sky_surface,(800,200))
bg_surface = pygame.image.load('Game Background.jpg').convert()

# Player Animations
player_jump_1= pygame.image.load('player_jump1.png').convert_alpha()
player_jump_2 = pygame.image.load('player_jump2.png').convert_alpha()
player_jump_3 = pygame.image.load('player_jump3.png').convert_alpha()
player_jump_4 = pygame.image.load('player_jump4.png').convert_alpha()

player_jump_1 = pygame.transform.scale(player_jump_1,(39,55))
player_jump_2 = pygame.transform.scale(player_jump_2,(39,55))
player_jump_3 = pygame.transform.scale(player_jump_3,(39,55))
player_jump_4 = pygame.transform.scale(player_jump_4,(39,55))
player_jump_list = [player_jump_1,player_jump_2,player_jump_3,player_jump_4]
player_index = 0  

player_walk_1 = pygame.image.load('player_walk1.png').convert_alpha()
player_walk_2 = pygame.image.load('player_walk2.png').convert_alpha()
player_walk_3 = pygame.image.load('player_walk3.png').convert_alpha()

player_walk_1 = pygame.transform.scale(player_walk_1,(39,55))
player_walk_2 = pygame.transform.scale(player_walk_2,(39,55))
player_walk_3 = pygame.transform.scale(player_walk_3,(39,55))
player_walk = [player_walk_1,player_walk_2,player_walk_3]

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(70,565))

# Enemies
enemy_surface = pygame.image.load('Enemies.png').convert_alpha()
enemy2_surface = pygame.image.load('enemy2.png').convert_alpha()

# End screen
player_end = pygame.image.load('player_end.png').convert_alpha()
player_end_scaled = pygame.transform.scale(player_end,(800,600))
player_end_rect = player_end_scaled.get_rect(center=(400,300))

end_text1 = text_font.render("You have Perished",False,(152,251,152))
end_text1_rect = end_text1.get_rect(center=(400,159))
end_text2 = text_font.render("Press Space to Try again!!!",False,(119,196,169))
end_text2_rect = end_text2.get_rect(center=(400,300))
end_text3 = text_font.render("Try again!!!",False,(138,3,3))
end_text3_rect = end_text3.get_rect(center=(400,450)) 

# Timer
obstacles_timer = pygame.USEREVENT+1
pygame.time.set_timer(obstacles_timer,900)

#  Game states
game_active = True

# Player physics
player_gravity = 0
player_speed = 0
move_speed = 5
jumps_left = 2

# Dash system
is_dashing = False
dash_time = 0
dash_cooldown = 500  # ms
dash_speed = 20
last_dash = 0

# Main Game Loop
while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                # Jump & Double Jump
                if event.key == pygame.K_w and jumps_left > 0:
                    player_gravity = -20
                    jumps_left -= 1

                # Dash
                if event.key == pygame.K_LSHIFT and pygame.time.get_ticks() - last_dash > dash_cooldown:
                    is_dashing = True
                    dash_time = pygame.time.get_ticks()
                    last_dash = dash_time

            if event.type == obstacles_timer:
                if randint(0,2):
                    obstacle_rect_list.append(enemy_surface.get_rect(bottomright=(randint(900,1100),565)))
                else:
                    obstacle_rect_list.append(enemy2_surface.get_rect(bottomright=(randint(900,1100),400)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                initial_time = pygame.time.get_ticks()
                player_rect.midbottom = (70,565)
                jumps_left = 2

    # Game Active
    if game_active:
        screen.blit(bg_surface,(0,0))
        screen.blit(sky_surface,(0,0))
        score = display_score()

        # Animations
        player_animation()
        screen.blit(player_surface, player_rect)

        # Gravity
        if not is_dashing:
            player_gravity += 1
            player_rect.y += player_gravity

        # Movement left/right
        if not is_dashing:
            if keys[pygame.K_a]:
                player_rect.x -= move_speed
            if keys[pygame.K_d]:
                player_rect.x += move_speed

        # Dash movement
        if is_dashing:
            if keys[pygame.K_d]:
                player_rect.x += dash_speed
            elif keys[pygame.K_a]:
                player_rect.x -= dash_speed
            if pygame.time.get_ticks() - dash_time > 150: # dash lasts 150ms
                is_dashing = False

        # collision on floor 
        if player_rect.bottom >= 565:
            player_rect.bottom = 565
            player_gravity = 0
            jumps_left = 2
        
        # Keep player inside screen 
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > 800:   
             player_rect.right = 800
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > 565:  
         player_rect.bottom = 565
        
        # Obstacles movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

    # Game Over Screen
    else:
        screen.fill((94,129,112))
        screen.blit(player_end_scaled, player_end_rect)
        screen.blit(end_text1,end_text1_rect)
        obstacle_rect_list.clear()
        score_message = text_font.render(f'Your Score:{score}',False,(255,215,0))
        score_message_rect = score_message.get_rect(center=(400,300))
        if score == 0:
            screen.blit(end_text2,end_text2_rect)
        else:
            screen.blit(score_message,score_message_rect)
        screen.blit(end_text3,end_text3_rect)

    pygame.display.update()
    clock.tick(60)



    
   


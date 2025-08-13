import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("Can you defeat them?")
clock = pygame.time.Clock()

text_font = pygame.font.Font(None,50)   

sky_surface = pygame.image.load('game sky.jpg').convert()
sky_surface = pygame.transform.scale(sky_surface,(800,200))
bg_surface = pygame.image.load('Game Background.jpg').convert()
enemy_surface = pygame.image.load('Enemies.png').convert_alpha()
player_surface = pygame.image.load('Player.png')
player_surface = pygame.transform.scale(player_surface,(39,55))

score_surface = text_font.render('My game',50,(64,64,64))
score_rect = score_surface.get_rect(center = (400,50))

player_rect = player_surface.get_rect(midbottom =(30,565) )
enemy_rect = enemy_surface.get_rect(midbottom = (700,565))

game_active = True

player_gravity = -20

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active==True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 565:
                        player_gravity = -20
             
        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                enemy_rect.left  = 700


    if game_active == True:
        screen.blit(bg_surface,(0,0))
        screen.blit(sky_surface,(0,0))
        enemy_rect.x -=4
        if enemy_rect.right<=0:
            enemy_rect.left = 800
        


        screen.blit(enemy_surface,enemy_rect)
        screen.blit(player_surface,player_rect)
        screen.blit(score_surface,score_rect)
        player_gravity+=1
        player_rect.y+=player_gravity

        if player_rect.bottom >=565:
            player_rect.bottom = 565

        #collision
        if enemy_rect.colliderect(player_rect):
            game_active = False
        
    else:
        screen.fill('Yellow')
   

    pygame.display.update()
    clock.tick(60)




    
   

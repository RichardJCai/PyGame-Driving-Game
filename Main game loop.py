"""
Author: Richard Cai
Description: Getaway (summative game)
Date: 5/29/2015

       Versions:
       V1.0 - Moving car sprite
       
       v1.1 - Infinite road background
       
       v1.2 - Road block obstacles, moving at the same speed as the road
       
       v1.3 - Incoming cars
       
       v1.4 - Unit collision 
       
       v1.5 - ScoreKeeper
       
       v1.6 - Coins for points
       
       v1.7 - Powerups
       
       v1.8 - Sprites and Sounds
       
       v1.9 - Menu
       """

# I - Import and Initialize
import pygame,pySprites,random
pygame.init()
pygame.mixer.init()
    
def main():    
    """Mainline logic for Getaway"""
    # D - Display configuration
    screen = pygame.display.set_mode((558, 558))
    pygame.display.set_caption("Getaway!")

    # E - Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    
    #Sounds
    pygame.mixer.music.load("Sounds/bgm.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    crash = pygame.mixer.Sound("Sounds/crash.wav")
    crash.set_volume(0.3)
    
    coin = pygame.mixer.Sound("Sounds/coin.wav")
    coin.set_volume(0.3)
    
    power_up = pygame.mixer.Sound("Sounds/power_up.wav")
    power_up.set_volume(0.3)
    

    #Road Background
    road = pySprites.road(screen)

    #Scorekeeper
    Scorekeeper = pySprites.ScoreKeeper()

    #Car sprite
    car = pySprites.player_car()

    #Coingroup
    coin_group = pygame.sprite.Group()

    #Power ups
    speed_boost = pygame.sprite.Group()
    life_boost = pygame.sprite.Group()

    pick_up_group = pygame.sprite.Group()
    
    #Obstacles
    opposing_cars = pySprites.other_cars()
    road_block = pySprites.road_blocks()

    road_block_group = [road_block]

    obstacles = pygame.sprite.Group(opposing_cars,road_block_group)
    
    #allSprites Group
    allSprites = pygame.sprite.OrderedUpdates(road,car,opposing_cars,road_block_group,Scorekeeper)

    # A - Action
 
      # A - Assign values
    clock = pygame.time.Clock()
    keepGoing = True

    move_up = False
    move_down = False
    move_left = False
    move_right = False
    counter = 0 

    speedboost = False
    boostcounter = 0
    invincibility_flag = False
    inv_counter = 0

    # L - Loop
    while keepGoing:
 
    # T - Timer
        clock.tick(30)

        #Ingame clock counter
        counter += 1
        if counter == 30:
            Scorekeeper.increase_tracker()
            #Adds more  road blocks for every 15 seconds
            if Scorekeeper.get_tracker() != 0 and Scorekeeper.get_tracker() % 15 == 0:
                allSprites.clear(screen,background)
                road_block_group.append(pySprites.road_blocks())
        
            #Adds coins for every 3 and 5 seconds  
            if Scorekeeper.get_tracker() != 0 and Scorekeeper.get_tracker() % 3 ==0 or Scorekeeper.get_tracker() % 5 == 0:
                coin_group.add(pySprites.coin())
            
            #Random powerup every 20 seconds
            if Scorekeeper.get_tracker() != 0 and Scorekeeper.get_tracker() % 20 == 0:
                #50/50 chance of either boost
                rand_boost = random.randint(0,1)
                if rand_boost == 0:
                    speed_boost.add(pySprites.speed_boost())
                elif rand_boost == 1:
                    life_boost.add(pySprites.life_up())
            
            #Update sprite groups
            pick_up_group = pygame.sprite.Group(coin_group,speed_boost,life_boost)
            obstacles = pygame.sprite.Group(opposing_cars,road_block_group)
            allSprites = pygame.sprite.OrderedUpdates(road,car,opposing_cars,road_block_group,coin_group,speed_boost,life_boost,Scorekeeper)
                     
            #Speedboost tracker, keeps speedboost on for 5 seconds
            if speedboost:
                boostcounter += 1
                if boostcounter == 5:
                    speedboost = False
                    car.speed_colour(False)
                    boostcounter = 0
                
            counter = 0
 
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                
                pygame.mixer.music.fadeout(2000)
                high_score(Scorekeeper)
                keepGoing = False
            
            #Movement, if a key is pressed down, a movement will happen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if speedboost:
                        car.move_up(12)
                    else:
                        car.move_up(7)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if speedboost:
                        car.move_down(12)
                    else:
                        car.move_down(7)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if speedboost:
                        car.move_left(12)
                    else:
                        car.move_left(7)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if speedboost:
                        car.move_right(12)
                    else:
                        car.move_right(7)
        
            #Keyup sets movement value to 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    car.move_up(0)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    car.move_down(0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    car.move_left(0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    car.move_right(0)
                
            
        #Collision detection
        for obstacle in  pygame.sprite.spritecollide(car,obstacles,False):
            obstacle.reset()
            Scorekeeper.death()
            crash.play()

        for item in pygame.sprite.spritecollide(car,coin_group,True):
            Scorekeeper.increase_points(50)
            coin.play()
        
        for item in pygame.sprite.spritecollide(car,speed_boost,True):
            speedboost = True
            car.speed_colour(True)
            power_up.play()
            
        for item in pygame.sprite.spritecollide(car,life_boost,True):
            Scorekeeper.increase_lives()
            power_up.play()
    
        #Checks if the player runs out of lives
        if Scorekeeper.game_over():
            pygame.mixer.music.fadeout(2000)
            high_score(Scorekeeper)
            keepGoing = False    
        
    
        #Checks each item in the coin_group
        for item in pick_up_group:
            if item.rect.centery > screen.get_height():
                item.kill()
                
       
        # R - Refresh display
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    
    # Close the game window
    pygame.quit()
    
def high_score(Scorekeeper):
    """Checks to see if the current score is higher than the old high score, if so, it rewrites the file with the new score"""
    
    #Try to open file, if it does not exist, write high score in new file
    try:
        score_file_r = open("score.txt","r")
        highscore = int(score_file_r.readline())
        score_file_r.close()
                    
        #If current points is higher than high score, current points becomes high score
        if Scorekeeper.get_points() > highscore:
            score_file = open("score.txt","w")
            score_file.write(str(Scorekeeper.get_points()))
            score_file.close()
                            
    except IOError:
        score_file = open("score.txt","w")
        score_file.write(str(Scorekeeper.get_points()))
        score_file.close()
        
        
def menu():
    """Menu program for Getaway"""
    
    # D - Menu Display
    screen = pygame.display.set_mode((558, 558))
    pygame.display.set_caption("Getaway Menu!")
 
    # E - Entities
    
    #Display the menu background
    background = pygame.image.load("Images/menu.gif")
    background = background.convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    #A - Action
    #Assign
   
    keepGoing = True
 
    # L - Loop
    while keepGoing:
 
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            
            #Pressing space starts the game ( runs main )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False
                    main() 
                    
    pygame.quit()

#Run menu
menu()
import random
import pygame
import time 

pygame.init()
fps = 60
timer = pygame.time.Clock()

class Game:
    def __init__(self) -> None:
        self.played = False
        self.score = 0
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.lines = [0, self.WIDTH/4, 2*self.WIDTH/4, 3*self.WIDTH/4]
        self.game_speed = 6
        self.pause = True
        self.run = True
        self.started = False
        self.gravity = 0.4
        self.myPlayer = Player(self.HEIGHT)
        self.myObstacles = []   
        self.myRocket = Obstacle("rocket.png", self.game_speed, self.HEIGHT)
        self.myUttropstecken = "uttropstecken.png"

        #pygame.draw()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption('Jetpack joyride')
        
        self.titleFont = pygame.font.Font('freesansbold.ttf', 64)
        self.font = pygame.font.SysFont(None, 32)

        self.bg_color = (128, 128, 128)
        self.lines = [0, self.WIDTH/4, 2*self.WIDTH/4, 3*self.WIDTH/4]
        self.top = pygame.draw.rect(self.screen, 'gray', [0, 0, self.WIDTH, 50])
        self.bottom = pygame.draw.rect(self.screen, 'gray', [0, self.HEIGHT-50, self.WIDTH, 50])
        self.booster = False
        self.startTime = time.time()

    def showTitleScreen(self):
        if not self.started:
            self.drawBackGround()
            self.title = myGame.titleFont.render("Press Space to start", False, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.screen.blit(self.title, ((self.WIDTH/5), (self.HEIGHT/2)))
            if self.played == True:
                self.titleScore = myGame.titleFont.render("Score: " + str(int(self.score)), False, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                self.screen.blit(self.titleScore, (400, 400))


    def start(self):
        self.game_speed = 6
        self.pause = False
        self.started = True
        self.startTime = time.time()

    def end(self):
        
        self.started = False
        self.game_speed=0
        self.myObstacles[0].setSpeed(self.game_speed)
        self.myRocket.setSpeed(self.game_speed)
        self.myObstacles[0].obstacle_rect.x = -1000
        self.myRocket.obstacle_rect.x = -1000
    
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.pause and self.started:
                    self.booster = True
                if event.key == pygame.K_SPACE and not self.started:
                    self.played = True
                    self.start()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.booster = False

    def drawBackGround(self):
        self.screen.fill('black')
        pygame.draw.rect(self.surface, 
                         (self.bg_color[0], self.bg_color[2], self.bg_color[2], 50),
                         [0, 0, self.WIDTH, self.HEIGHT])
        self.screen.blit(self.surface, (0, 0))
        self.top = pygame.draw.rect(self.screen, 'gray', [0, 0, self.WIDTH, 50])
        self.bottom = pygame.draw.rect(self.screen, 'gray', [0, self.HEIGHT-50, self.WIDTH, 50])
        for i in range(len(self.lines)):
            pygame.draw.line(self.screen, 'black', (self.lines[i], 0), (self.lines[i], 50), 3)  #-#Svart linje på toppen
            pygame.draw.line(self.screen, 'black', (self.lines[i], self.HEIGHT-50), (self.lines[i], self.HEIGHT), 3) #-#Svart linje på botten
            if not self.pause:
                self.lines[i] -= self.game_speed
            if self.lines[i] < -3:
                self.lines[i] = self.WIDTH

    def drawPlayer(self):
        self.colliding=self.checkAreaCollision()
        self.myPlayer.Draw(self.screen, self.pause, self.gravity, self.colliding, self.booster)
    
    def drawLaser(self):
        if len(self.myObstacles)==0:
            self.myObstacles.append(Obstacle("hinder.png", self.game_speed, self.HEIGHT))
        for i in range(len(self.myObstacles)):
            self.myObstacles[i].spawnObstacle(self.HEIGHT, self.WIDTH)
            self.myObstacles[i].draw(self.screen)
            if self.myObstacles[i].checkCollision(self.myPlayer.getPlayer()):
                self.end()

    def drawRocket(self):
        self.myRocket.spawnObstacle(self.HEIGHT, self.WIDTH)
        self.myRocket.createUttropstecken(self.WIDTH)
        self.myRocket.draw(self.screen)
        self.myRocket.setSpeed(self.game_speed+4)
        if self.myRocket.checkCollision(self.myPlayer.getPlayer()):
            self.end()
        
    def checkAreaCollision(self):
        coll = [False, False]
        if self.myPlayer.getPlayer().colliderect(self.bottom):
            coll[0] = True
        elif self.myPlayer.getPlayer().colliderect(self.top):
            coll[1] = True
        return coll
    
    def getRunStatus(self):
        return self.run

    
    def titleScreen(self):
        self.game_speed = 0
        

    
class Player:
    def __init__(self, height) -> None:
        self.init_y = height - 130
        self.player_y = self.init_y
        self.counter = 0
        self.y_velocity = 0
        self.player = pygame.rect.Rect((120, self.player_y + 10), (25, 60))
    
    def getPlayer(self):
        return self.player
    
    def Draw(self, screen, pause, gravity, colliding, booster):
        if not pause:
            if booster:
                self.y_velocity -= gravity
            else:
                self.y_velocity += gravity

        if self.counter < 40:
            self.counter += 1
        else:
            self.counter = 0
    
        if (colliding[0] and self.y_velocity > 0) or (colliding[1] and self.y_velocity < 0):
            self.y_velocity = 0 
        self.player_y += self.y_velocity

        self.player = pygame.rect.Rect((120, self.player_y + 10), (25, 60))
        if self.player_y <= self.init_y or pause:
            if booster:
                pygame.draw.ellipse(screen, 'red', [100, self.player_y + 50, 20, 30])
                pygame.draw.ellipse(screen, 'orange', [105, self.player_y + 50, 10, 30])
                pygame.draw.ellipse(screen, 'yellow', [110, self.player_y + 50, 5, 30])
            pygame.draw.rect(screen, 'yellow', [128, self.player_y + 60, 10, 20], 0, 3)
            pygame.draw.rect(screen, 'orange', [130, self.player_y + 60, 10, 20], 0, 3)
        else:
            if self.counter < 10:
                pygame.draw.line(screen, 'yellow',
                                 (128, self.player_y + 60),
                                 (140, self.player_y + 80), 10)
                pygame.draw.line(screen, 'orange',
                                 (130, self.player_y + 60),
                                 (120, self.player_y + 80), 10)
                #-#draw pos1
            elif 10 <= self.counter < 20:
                pygame.draw.rect(screen, 'yellow',
                                 [128, self.player_y + 60, 10, 20], 0, 3)
                pygame.draw.rect(screen, 'orange',
                                 [130, self.player_y + 60, 10, 20], 0, 3)        
            elif 20 <= self.counter < 30:
                pygame.draw.line(screen, 'yellow',
                                 (128, self.player_y + 60), (120, self.player_y + 80), 10)
                pygame.draw.line(screen, 'orange',
                                 (130, self.player_y + 60), (140, self.player_y + 80), 10)        
            else:
                pygame.draw.rect(screen, 'yellow',
                                 [128, self.player_y + 60, 10, 20], 0, 3)
                pygame.draw.rect(screen, 'orange',
                                 [130, self.player_y + 60, 10, 20], 0, 3)
            
        #-#Jetpack, body, head
        pygame.draw.rect(screen, 'white', [100, self.player_y + 20, 20, 30], 0, 5)
        pygame.draw.ellipse(screen, 'orange', [120, self.player_y + 20, 20, 50])
        pygame.draw.circle(screen, 'orange', (135, self.player_y + 15), 10)
        pygame.draw.circle(screen, 'black', (138, self.player_y + 12), 3)
    
    
class Obstacle:
    def __init__(self, filename, speed, height) -> None:
        self.obstacle= pygame.image.load(filename)
        obstacle_size = self.obstacle.get_size()
        self.obstacle = pygame.transform.scale(self.obstacle, (int(obstacle_size[0]/2), int(obstacle_size[1]/2)))
        self.obstacle = pygame.transform.rotate(self.obstacle, 90) #random
        self.obstacle_rect = self.obstacle.get_rect()
        self.obstacle_rect.x = -1000
        self.obstacle_rect.y = height/2
        self.speed = speed
        self.myUttropstecken = None
    
    def spawnObstacle(self, height, width) -> None:
        if self.obstacle_rect.x < (random.randint(-1000,-500)):
            y_ccord = random.randint(50, (height-155))
            self.obstacle_rect.x = (width+500)
            self.obstacle_rect.y = y_ccord


    def createUttropstecken(self, width):
        self.myUttropstecken = pygame.image.load("uttropstecken.png")
        self.myUttropstecken_x = width-100
        self.myUttropstecken_y = self.obstacle_rect.y
    

    def setSpeed(self, speed):
        self.speed = speed 
    
    def getRect(self):
        return self.obstacle_rect
    
    def draw(self, screen):
        self.obstacle_rect.x-=self.speed
        #if self.speed != self.game_speed:
        #    screen.blit(self.myUttropstecken, (self.myUttropstecken_x, self.myUttropstecken_y))
        if self.myUttropstecken:
            screen.blit(self.myUttropstecken, (self.myUttropstecken_x, self.myUttropstecken_y))

        screen.blit(self.obstacle, (self.obstacle_rect.x,self.obstacle_rect.y))
    
    def checkCollision(self, player):
        if player.colliderect(self.obstacle_rect):
            
            return True
        return False

myGame = Game()

run = True


while myGame.getRunStatus(): 

    timer.tick(fps)

     
    #lines, top_plat, bottom_plat = draw_screen(lines)#, laser, laser_line = draw_screen(lines, laser)
    #player = myPlayer.Draw(booster)
    #print (f"player x,y: {player.x}{player.y}")
    #print (f"obastacle x,y: {obstacle1.getRect()}")
    #obstacle1.spawnObstacle()
    #obstacle1.draw()
    #obstacle_colliding = obstacle1.checkCollision(player)
    #colliding = check_colliding()

    #if obstacle_colliding:
    #    game_speed=0
    #    obstacle1.setSpeed(game_speed)
    if myGame.started:
        myGame.score = (time.time() - myGame.startTime)*(myGame.game_speed)
        
        textScore = myGame.font.render("score: " + str(int(myGame.score)), False, (255, 0, 0))
        

        if myGame.game_speed < 16:
            myGame.game_speed += 0.005
            for i in range (len(myGame.myObstacles)):
                myGame.myObstacles[i].setSpeed(myGame.game_speed)



        myGame.drawBackGround()
        myGame.drawPlayer()
        myGame.drawLaser()
        myGame.drawRocket()
        myGame.screen.blit(textScore, (10, 10))
    else:
        myGame.showTitleScreen()
    myGame.checkEvent()
    pygame.display.flip()
    pygame.display.update()
pygame.quit()




#-#how to make jetpack joyride in python! Full game tutorial - Creating and drawing the laser obstacles

#-#fixa laser positioner, class som bara ändrar x pos med - gamespeed. y samma och random.
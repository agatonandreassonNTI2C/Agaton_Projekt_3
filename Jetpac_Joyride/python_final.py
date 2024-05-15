import random  # Importera randommodulen för slumpmässiga operationer
import pygame  # Importera pygame-biblioteket för spelutveckling
import time  # Importera time-modulen för tidsrelaterade operationer

pygame.init()  # Initiera pygame-modulen
fps = 60  # Sätt antal frames per sekund för spelet
timer = pygame.time.Clock()  # Skapa en klocka för att hantera tiden i spelet

class Game:  # Skapa en klass för spelet
    def __init__(self) -> None:  # Konstruktor för Game-klassen
        # Initialiserar min Game klass variablar
        self.played = False  # Flagga för om spelet har startats
        self.score = 0  # Spelarens poäng i spelet
        self.WIDTH = 1000  # Bredden på spelfönstret
        self.HEIGHT = 600  # Höjden på spelfönstret
        self.lines = [0, self.WIDTH/4, 2*self.WIDTH/4, 3*self.WIDTH/4]  # Positioner för linjer i spelområdet
        self.game_speed = 6  # Hastighet för spelet
        self.pause = True  # Flagga för paus i spelet
        self.run = True  # Flagga för att köra spelet
        self.started = False  # Flagga för om spelet har börjat
        self.gravity = 0.4  # Gravitationskraften i spelet
        self.myPlayer = Player(self.HEIGHT)  # Skapa en instans av spelarobjektet
        self.myObstacles = []  # Lista för hinderobjekt
        self.myRocket = Obstacle("rocket.png", self.game_speed, self.HEIGHT)  # Skapa ett rakethinderobjekt
        self.myUttropstecken = "uttropstecken.png"  # Filnamnet för utropstecknet

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))  # Skapa spelområdet
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)  # Skapa en yta för alfastöd
        pygame.display.set_caption('Jetpack joyride')  # Sätt titeln på fönstret

        # Skapa fontar för text i spelet
        self.titleFont = pygame.font.Font('freesansbold.ttf', 64)
        self.font = pygame.font.SysFont(None, 32)

        self.bg_color = (128, 128, 128)  # Bakgrundsfärg för spelet
        self.lines = [0, self.WIDTH/4, 2*self.WIDTH/4, 3*self.WIDTH/4]  # Positioner för linjer i spelområdet
        self.top = pygame.draw.rect(self.screen, 'gray', [0, 0, self.WIDTH, 50])  # Övre plattform
        self.bottom = pygame.draw.rect(self.screen, 'gray', [0, self.HEIGHT-50, self.WIDTH, 50])  # Nedre plattform
        self.booster = False  # Flagga för jetpack-boost
        self.startTime = time.time()  # Starttid för spelet

    # Funktion för att visa titelskärmen
    def showTitleScreen(self):
        if not self.started:
            self.drawBackGround()  # Rita bakgrund
            # Skapa text för att starta spelet
            self.title = myGame.titleFont.render("Press Space to start", False, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.screen.blit(self.title, ((self.WIDTH/5), (self.HEIGHT/2)))  # Rita texten på skärmen
            if self.played == True: # Om det inte är första gången. Alltså om man har dött istället för att startat spelet.
                # Visa spelarens poäng på titelskärmen
                self.titleScore = myGame.titleFont.render("Score: " + str(int(self.score)), False, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                self.screen.blit(self.titleScore, (400, 400))  # Rita poängen på skärmen

    # Funktion för att starta spelet
    def start(self):
        self.game_speed = 6  # Återställ spelets hastighet
        self.pause = False  # Sluta pausa spelet
        self.started = True  # Sätt igång spelet
        self.startTime = time.time()  # Sätt starttiden för spelet

    # Funktion för att avsluta spelet
    def end(self):
        self.started = False  # Stoppa spelet
        self.game_speed = 0  # Stoppa spelets hastighet
        self.myObstacles[0].setSpeed(self.game_speed)  # Återställ hinderobjektets hastighet
        self.myRocket.setSpeed(self.game_speed)  # Återställ rakethinderobjektets hastighet
        self.myObstacles[0].obstacle_rect.x = -1000  # Återställ hinderobjektets position
        self.myRocket.obstacle_rect.x = -1000  # Återställ rakethinderobjektets position

    # Funktion för att kontrollera händelser i spelet
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False  # Avsluta spelet vid stängning av fönstret
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.pause and self.started:
                    self.booster = True  # Aktivera jetpack-boost
                if event.key == pygame.K_SPACE and not self.started:
                    self.played = True  # Spelet har startats
                    self.start()  # Starta spelet
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.booster = False  # Avaktivera jetpack-boost

    # Funktion för att rita bakgrunden
    def drawBackGround(self):
        self.screen.fill('black')  # Fyll skärmen med svart färg
        # Rita bakgrunden med alfastöd
        pygame.draw.rect(self.surface, 
                         (self.bg_color[0], self.bg_color[2], self.bg_color[2], 50),
                         [0, 0, self.WIDTH, self.HEIGHT])
        self.screen.blit(self.surface, (0, 0))  # Rita bakgrunden på skärmen
        self.top = pygame.draw.rect(self.screen, 'gray', [0, 0, self.WIDTH, 50])  # Rita övre plattformen
        self.bottom = pygame.draw.rect(self.screen, 'gray', [0, self.HEIGHT-50, self.WIDTH, 50])  # Rita nedre plattformen
        # Rita linjer i spelområdet
        for i in range(len(self.lines)):
            # Rita linjer på övre plattformen
            pygame.draw.line(self.screen, 'black', (self.lines[i], 0), (self.lines[i], 50), 3)
            # Rita linjer på nedre plattformen
            pygame.draw.line(self.screen, 'black', (self.lines[i], self.HEIGHT-50), (self.lines[i], self.HEIGHT), 3)
            if not self.pause:
                self.lines[i] -= self.game_speed  # Uppdatera linjernas position baserat på spelets hastighet
            if self.lines[i] < -3:
                self.lines[i] = self.WIDTH  # Återställ linjernas position när de når skärmens kant

    # Funktion för att rita spelaren
    def drawPlayer(self):
        self.colliding = self.checkAreaCollision()  # Kontrollera kollision med spelarens område
        # Rita spelaren på skärmen
        self.myPlayer.Draw(self.screen, self.pause, self.gravity, self.colliding, self.booster)
    
    # Funktion för att skapa laserhindren
    def drawLaser(self):
        if len(self.myObstacles) == 0:
            self.myObstacles.append(Obstacle("hinder.png", self.game_speed, self.HEIGHT))  # Skapa ett nytt hinderobjekt
        for i in range(len(self.myObstacles)):
            self.myObstacles[i].spawnObstacle(self.HEIGHT, self.WIDTH)  # Placera ut hindret i spelområdet
            self.myObstacles[i].draw(self.screen)  # Rita hindret på skärmen
            if self.myObstacles[i].checkCollision(self.myPlayer.getPlayer()):
                self.end()  # Avsluta spelet om spelaren kolliderar med hindret

    # Funktion för att skapa rakethindret
    def drawRocket(self):
        self.myRocket.spawnObstacle(self.HEIGHT, self.WIDTH)  # Placera ut rakethindret i spelområdet
        self.myRocket.createUttropstecken(self.WIDTH)  # Skapa utropstecken för rakethindret
        self.myRocket.draw(self.screen)  # Rita rakethindret på skärmen
        self.myRocket.setSpeed(self.game_speed + 3)  # Ställ in hastigheten för rakethindret
        if self.myRocket.checkCollision(self.myPlayer.getPlayer()):
            self.end()  # Avsluta spelet om spelaren kolliderar med rakethindret
        
    # Funktion för att kontrollera kollision med spelarens område
    def checkAreaCollision(self):
        coll = [False, False]
        if self.myPlayer.getPlayer().colliderect(self.bottom):
            coll[0] = True
        elif self.myPlayer.getPlayer().colliderect(self.top):
            coll[1] = True
        return coll
    
    # Funktion för att kontrollera om spelet ska fortsätta köras
    def getRunStatus(self):
        return self.run

    # Funktion för att visa titelskärmen
    def titleScreen(self):
        self.game_speed = 0  # Stoppa spelets hastighet
        
class Player:  # Klass för spelaren
    def __init__(self, height) -> None:  # Konstruktor för Player-klassen
        self.init_y = height - 130  # Initial y-position för spelaren
        self.player_y = self.init_y  # Aktuell y-position för spelaren
        self.counter = 0  # Räknare för animation av spelaren
        self.y_velocity = 0  # Y-hastighet för spelaren
        self.player = pygame.rect.Rect((120, self.player_y + 10), (25, 60))  # Spelarens rektangel

    # Funktion för att hämta spelarens rektangel
    def getPlayer(self):
        return self.player
    
    # Funktion för att rita spelaren på skärmen
    def Draw(self, screen, pause, gravity, colliding, booster):
        if not pause:
            if booster:
                self.y_velocity -= gravity  # Aktivera jetpack-boost
            else:
                self.y_velocity += gravity  # Applicera gravitationskraft

        if self.counter < 40:
            self.counter += 1
        else:
            self.counter = 0
    
        if (colliding[0] and self.y_velocity > 0) or (colliding[1] and self.y_velocity < 0):
            self.y_velocity = 0  # Stoppa vertikal rörelse vid kollision med plattformar
        self.player_y += self.y_velocity  # Uppdatera spelarens y-position baserat på hastighet

        self.player = pygame.rect.Rect((120, self.player_y + 10), (25, 60))  # Uppdatera spelarens rektangel

        # Rita spelaren och jetpacken beroende på dess status
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
            
        pygame.draw.rect(screen, 'white', [100, self.player_y + 20, 20, 30], 0, 5)
        pygame.draw.ellipse(screen, 'orange', [120, self.player_y + 20, 20, 50])
        pygame.draw.circle(screen, 'orange', (135, self.player_y + 15), 10)
        pygame.draw.circle(screen, 'black', (138, self.player_y + 12), 3)

class Obstacle:  # Klass för hinder
    def __init__(self, filename, speed, height) -> None:  # Konstruktor för Obstacle-klassen
        self.obstacle = pygame.image.load(filename)  # Läs in hinderbilden från filen
        obstacle_size = self.obstacle.get_size()  # Hämta storleken på hinderbilden
        # Skala hinderbilden till önskad storlek
        self.obstacle = pygame.transform.scale(self.obstacle, (int(obstacle_size[0]/2), int(obstacle_size[1]/2)))
        self.obstacle = pygame.transform.rotate(self.obstacle, 90)  # Rotera hinderbilden (valfritt)
        self.obstacle_rect = self.obstacle.get_rect()  # Skapa en rektangel för hindret
        self.obstacle_rect.x = -1000  # Startposition för hindret utanför vänsterkanten
        self.obstacle_rect.y = height/2  # Y-position för hindret (vertikalt centrerat)
        self.speed = speed  # Hastighet för hindret
        self.myUttropstecken = None  # Utropstecken för hindret

    # Funktion för att placera ut hindret i spelområdet
    def spawnObstacle(self, height, width) -> None:
        if self.obstacle_rect.x < (random.randint(-1000, -500)):
            # Slumpmässig y-position för hindret inom spelområdet
            y_ccord = random.randint(50, (height - 155))
            self.obstacle_rect.x = (width + 500)  # Återställ hindrets x-position utanför högerkanten
            self.obstacle_rect.y = y_ccord  # Uppdatera hindrets y-position

    # Funktion för att skapa utropstecken för hindret
    def createUttropstecken(self, width):
        self.myUttropstecken = pygame.image.load("uttropstecken.png")  # Läs in utropstecken från filen
        self.myUttropstecken_x = width - 100  # X-position för utropstecknet
        self.myUttropstecken_y = self.obstacle_rect.y  # Y-position för utropstecknet

    # Funktion för att ställa in hindrets hastighet
    def setSpeed(self, speed):
        self.speed = speed  # Uppdatera hindrets hastighet

    # Funktion för att hämta hindrets rektangel
    def getRect(self):
        return self.obstacle_rect  # Returnera hindrets rektangel

    # Funktion för att rita hindret på skärmen
    def draw(self, screen):
        self.obstacle_rect.x -= self.speed  # Uppdatera hindrets x-position baserat på spelets hastighet
        if self.myUttropstecken:
            screen.blit(self.myUttropstecken, (self.myUttropstecken_x, self.myUttropstecken_y))  # Rita utropstecknet
        screen.blit(self.obstacle, (self.obstacle_rect.x, self.obstacle_rect.y))  # Rita hindret på skärmen

    # Funktion för att kontrollera kollision med spelaren
    def checkCollision(self, player):
        if player.colliderect(self.obstacle_rect):
            return True  # Returnera True om kollision med spelaren
        return False  # Annars returnera False

myGame = Game()  # Skapa ett Game-objekt för spelet (Klassen Games funktioner kan användas i min huvudspel loop)
run = True  # Flagga för att köra spelet

while myGame.getRunStatus():  # Huvudspel loopen
    timer.tick(fps)  # Uppdatera klockan med aktuell framehastighet

    if myGame.started:  # Om spelet har startat
        myGame.score = (time.time() - myGame.startTime) * (myGame.game_speed)  # Uppdatera spelarens poäng

        textScore = myGame.font.render("score: " + str(int(myGame.score)), False, (255, 0, 0))  # Text för poängvisning

        if myGame.game_speed < 16:  # Öka spelets hastighet gradvis
            myGame.game_speed += 0.005
            for i in range(len(myGame.myObstacles)):
                myGame.myObstacles[i].setSpeed(myGame.game_speed)

        # Rita bakgrund, spelare, hinder och rakethinder på skärmen
        myGame.drawBackGround()
        myGame.drawPlayer()
        myGame.drawLaser()
        myGame.drawRocket()
        myGame.screen.blit(textScore, (10, 10))  # Rita poängtexten på skärmen
    else:
        myGame.showTitleScreen()  # Visa titelskärmen om spelet inte har startat ännu.

    myGame.checkEvent()  # Kontrollera händelser i spelet
    pygame.display.flip()  # Uppdatera skärmen
    pygame.display.update()  # Uppdatera skärmen

pygame.quit()  # Avsluta pygame-modulen när spelet är klart

# =====SAVE THE SCREEN GAME=====

#Code Contents:

#Libraries and Initialisations
#Class Definitions
#Subprogram Definitions
#Object Creation
#Group Assignment
#Game Loop (Event Blocks (Single Loop))
#Game Loop (Current Menu Blocks (Every Loop))

#Basic Code Layout Explanation:

#Libraries and Initialisation is just seting all global variables at the start of the program
#so that the game knows what they're supposed to be.

#Class Definitions Defines my Buttons, Windows, Text and Entity objects that the game uses the most.

#Subprogram Definitions covers many different subprograms for some screens and mainly for gameplay elements.

#Object Creation is my initialisation that can only take place after the classes are defined. Each object is
#defined specifically so that it is at a set size, location and colour as well as having other unique data.

#Group Assignment is how I seperate my objects so that only ones apart of a specific group can be displayed
#to the screen and interacted with by the player.

#The Game Loop is how the game runs every frame. Inside a while loop is all of my code that can be run multiple
#times each time the game is played. It is broken into 2 main chunks: 1 where the code is run once per call and
#1 where the code is run every frame (frame rate is controlled by line at the end of the while loop).

#The single-time run code is controlled by pygame events that are only sent to be read once (e.g. when a button
#is pressed). This is where all of my drawing to the screen happens and where the currentMenu variable is set.

#The contantly run code is controlled by that currentMenu variable and is for any checks that need to take place
#every frame like checking if a button has been pressed.

#In the case of the gameplay screen, this has 2 different currentMenu blocks due to the contantly run code only
#running every time an event happens wheras the other gameplay block is run every frame regardless. I need to
#seperate the 2 because things like player movement being tied to the event handler means that the game only 
#provides movement when a pygame event happens. If the player doest touch anything, then no events occur leading
#to a weird jittery movement error hence my inclusion of 2 currentMenu checks in the game loop.

#The game is defined in order of which screens appear in standard gameplay. This is as follows:
#TitleScreen, SaveSelect, MainMenu, AdventureMode, EndlessMode, Settings, Controls, Gameplay+Upgrades
#It follows this order for Initialisation, Class Definitions, Grouping and The Game Loop


# Imports =======================================================================================================================
import csv
import math
import sys
import random
import pygame
from pygame.locals import *
# Library Initialisation ========================================================================================================
pygame.init()
framePerSec = pygame.time.Clock()

smallFont = pygame.font.Font(None, 22)
standardFont = pygame.font.Font(None, 36)
titleFont = pygame.font.Font(None, 78)
#emojiFont = pygame.font.Font("seguiemj.ttf",24) Never used but could be in future

# Global Variables & Constants ==================================================================================================
FPS = 60
HEIGHT = 500
WIDTH = 900

timeSinceAbility1 = 0 
timeSinceAbility2 = 0 

shieldCount = 0
shieldActivated = False
shieldActivationLength = 0 

swordCount = 0
swordActivated = False
swordDamageCooldown = 0
swordActivationLength = 0
angleOfSword = 0

playerAttackInput = pygame.K_SPACE #These are the game's default controls if the player doesn't set any themself
playerAction1Input = 1 # This matches the pygame input for left mouse button
playerAction2Input = pygame.K_RETURN

canDash = True
canSaviour = False
saviourUsed = False
canRampage = False
canBurst = False
canPulse = False
canSuper = False

ability1Cooldown = 30
ability2Cooldown = 300

playerChosenUpgrades = []
playerDiscardedUpgrades = []
                                                                                                                              #Tier (Count)
masterUpgradeList = [["Sharpen", "Resist", "Fast", "Dextrous", "Extend"],                                                     #Common (5)
                     ["Honed", "Deft", "Broaden", "Boost", "Blacksmith", "Stoic", "Temper", "Inflate", "Exercise", "Unruly"], #Uncommon (10)
                     ["Toughen", "Speedier", "Embiggen", "Smite", "Fortify", "Rush", "Lash", "Bolster"],                      #Rare (8)
                     ["Dash", "Saviour", "Rampage", "Burst", "Pulse", "Super"]]                                               #Ability (6)

dungeon1Upgrades = [""]
dungeon2Upgrades = [""]
dungeon3Upgrades = [""]
dungeon4Upgrades = [""]
dungeon5Upgrades = [""]

loopsOfEndless = 0

preRampageDamage = 0
preBurstDspeed = 0
prePulseRange = 0
                                                                            #Numbers refer to upgrade tier where 0=Basic and 3=Ability
floorReward = [0,0,0,                                                       #Dungeon 1
               0,1,0,2,0,1,0,                                               #Dungeon 2
               0,1,0,2,0,1,3,0,2,0,1,0,2,0,0,                               #Dungeon 3
               0,1,0,2,0,1,3,0,2,0,1,0,2,0,0,                               #Dungeon 4
               0,1,0,2,0,1,0,2,0,1,0,2,3,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0] #Dungeon 5

currentDungeon = 0
currentFloor = 0
startingFloor = [0,3,10,25,40]
endingFloor = [3,10,25,40,70]

gameMode = ""

randomUpgrade1 = random.randint(0,4)
randomUpgrade2 = random.randint(0,4)
randomUpgrade3 = random.randint(0,4)
randomUpgrade4 = random.randint(0,4)

currentMenu = ""
previousMenu = ""
showQuitMenu = False
#choice = True   #Used in SaveSelect submenu should be renamed if re-used
continueWithGameplay = False 

saveFileSelectedButton = ""
controlsSelectedButton = ""

fileName1 = "" 
fileName2 = ""
fileName3 = ""

gameData = []
currentFile = ""
# Screen Event Assignment =======================================================================================================
NONE = pygame.event.custom_type()
TITLESCREEN = pygame.event.custom_type()
SAVESELECT = pygame.event.custom_type()
MAINMENU = pygame.event.custom_type()
ADMODESELECT = pygame.event.custom_type()
ENDMODESELECT = pygame.event.custom_type()
SETTINGS = pygame.event.custom_type()
CONTROLS = pygame.event.custom_type()
ACHIEVEMENTS = pygame.event.custom_type()
GAMEPLAY = pygame.event.custom_type()
UPGRADES = pygame.event.custom_type()
# Initial File Handling =========================================================================================================
#ORDER OF FILE INTERNALS: | Name Data | Endless Scores | Adventure Progress | Current Postion Data | Controls/Settings |


with open('GameFile1.csv', newline= '', encoding='utf-16') as csvFile :
    csvReader = csv.reader(csvFile)
    for row in csvReader :
        gameData.append(row)
#fileName1 = gameData[0][1] 

gameData = []

with open('GameFile2.csv', newline= '', encoding='utf-16') as csvFile :
    csvReader = csv.reader(csvFile)
    for row in csvReader :
        gameData.append(row)
   
#fileName2 = gameData[0][1]

gameData = []

with open('GameFile3.csv', newline= '', encoding='utf-16') as csvFile :
    csvReader = csv.reader(csvFile)
    for row in csvReader :
        gameData.append(row)

#fileName3 = gameData[0][1]

gameData = []
# Screen Creation ===============================================================================================================
displaySurface = pygame.display.set_mode((WIDTH,HEIGHT))
displaySurface.fill((255,255,255))
pygame.display.set_caption("SAVE THE SCREEN")

# Classes =======================================================================================================================

class gameObject(pygame.sprite.Sprite): #Base class all menu object inherit
    def __init__(self, x, y, width, height):
        super().__init__()
        self.pos = [x,y]
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
 
 
class Button(gameObject):
    def __init__(self, x, y, width, height, colour, clickEvent):
        super().__init__(x, y, width, height) # takes everything from gameObject
        
        self.surf.fill(colour)
        self.clickEvent = clickEvent #So I can direct where a button should take the player
        
    def clicked(self, pEvent):
        if (pEvent.type == pygame.MOUSEBUTTONDOWN) and (self.rect.collidepoint(int(pygame.mouse.get_pos()[0]),int(pygame.mouse.get_pos()[1]))):
            pygame.event.post(pygame.event.Event(self.clickEvent))
            return(True)
           

class TitleText(gameObject): #3 different text objects for different font sizes
    def __init__(self, x, y, text, colour):
        width = titleFont.size(text)[0]
        height = titleFont.size(text)[1]
        super().__init__(x, y, width, height)
        
        self.colour = colour
        self.text = text
        self.surf = titleFont.render(text, True, colour)
        
class StandardText(gameObject):
    def __init__(self, x, y, text, colour):
        width = standardFont.size(text)[0]
        height = standardFont.size(text)[1]
        super().__init__(x, y, width, height)
        
        self.colour = colour 
        self.text = text
        self.surf = standardFont.render(text, True, colour)
        
class SmallText(gameObject):
    def __init__(self, x, y, text, colour):
        width = smallFont.size(text)[0]
        height = smallFont.size(text)[1]
        super().__init__(x, y, width, height)
        
        self.colour = colour
        self.text = text
        self.surf = smallFont.render(text, True, colour)
        
class Window(gameObject):
    def __init__(self, x, y, width, height, colour):
        super().__init__(x, y, width, height)
        self.colour = colour
        self.surf.fill(colour)
        
class ImageButton(pygame.sprite.Sprite):
    def __init__(self, x, y, filePath, clickEvent):
        super().__init__()
        self.filePath = filePath
        self.pos = [x,y]
        self.surf = pygame.image.load(filePath)
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.clickEvent = clickEvent 
        
    def clicked(self, pEvent): #Same function as from Button class
        if (pEvent.type == pygame.MOUSEBUTTONDOWN) and (self.rect.collidepoint(int(pygame.mouse.get_pos()[0]),int(pygame.mouse.get_pos()[1]))):
            pygame.event.post(pygame.event.Event(self.clickEvent))
            return(True)
                
class Entity(pygame.sprite.Sprite): #Base class for all gameplay objects
    def __init__(self, x, y, colour):
        super().__init__()
        self.x = x #So that I can find an entity's starting point later,
        self.y = y #I'm saving their x and y from initialisation
        self.pos = [x,y]
        self.surf = pygame.Surface((40,40))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
        self.velocity = [0,0]
        self.direction = [1,1]
        self.colour = colour
        self.flag = False
    def move(self):
        if self.velocity == 0:
            pass
        else:
            self.pos[0] += self.velocity[0] * self.direction[0]
            self.pos[1] += self.velocity[1] * self.direction[1]
            self.rect = self.surf.get_rect(center = (self.pos[0], self.pos[1]))
            
        if self.pos[0] >= 900 - 20 :
            self.direction[0] = -1
        elif self.pos[0] <= 0 + 20 :
            self.direction[0] = 1
            
        elif self.pos[1] >= 500 - 20 :
            self.direction[1] = -1
        elif self.pos[1] <= 0 + 20 :
            self.direction[1] = 1
       

class Player(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x,y,colour)
        self.damage = 1
        self.Dspeed = 100
        self.Mspeed = 100
        self.range = 100
        self.maxHealth = 3
        self.health = 3
        
class Enemy(Entity):
    def __init__(self,x,y,colour):
        super().__init__(x,y,colour)
        
        if self.colour == (0,0,0):
            self.damage = 1
            self.health = 1
            self.maxHealth = 1
            self.speed = 1
            
        elif self.colour == (255,255,255):
            self.damage = 2
            self.health = 3
            self.maxHealth = 3
            self.speed = 2
        else:
            self.damage = 0
            self.health = 1
            self.maxHealth = 1
            self.speed = 0
            
class Shield(Entity):
    def __init__(self,x,y,colour):
        super().__init__(x,y,colour)
        self.width = 50
        self.height = 50
        self.surf = pygame.image.load("ShieldTransNoBorder.png")  
        self.surf = pygame.transform.scale_by(self.surf, 1.5)  
        
    def move(self, pEntity):
        self.direction = pEntity.direction
        self.pos[0] = pEntity.pos[0]
        self.pos[1] = pEntity.pos[1]
        self.rect = self.surf.get_rect(center = (self.pos[0] + pEntity.direction[0]*5, self.pos[1] + pEntity.direction[1]*5))
        
    def sizeChange(self, pEntity):
        self.surf = pygame.image.load("ShieldTransNoBorder.png")  
        self.surf = pygame.transform.scale_by(self.surf, ((pEntity.range/100)*0.8)+0.5)


class Sword(Entity):
    def __init__(self, x, y, colour):
        super().__init__(x, y, colour)
        self.surf = pygame.image.load("ColouredSword.png")  
        self.surf = pygame.transform.scale_by(self.surf, 0.6)  
        
    def move(self, pEntity):
        global angleOfSword
        self.direction = pEntity.direction
        self.pos[0] = pEntity.pos[0]
        self.pos[1] = pEntity.pos[1]

        testSurf = self.surf
        testSurf.blit(self.surf, (self.pos[0], self.pos[1]))
        rotatedSurf = pygame.transform.rotate(testSurf, -angleOfSword)
        
        self.rect = rotatedSurf.get_rect(center=((self.pos[0] + (40*(pEntity.range/100))  * math.cos(math.radians(angleOfSword))) ,(self.pos[1] + (40*(pEntity.range/100)) * math.sin(math.radians(angleOfSword)))))
        
        displaySurface.blit(rotatedSurf, self.rect)
        angleOfSword+=5
        
    def sizeChange(self, pEntity):
        self.surf = pygame.image.load("ColouredSword.png")  
        self.surf = pygame.transform.scale_by(self.surf, ((pEntity.range/100)*0.4)+0.2)


      
# Subprograms ====================================================================================================================
def readCSV(pFile):
    global currentFile
    currentFile = pFile
    
    global gameData
    
    global adModeDungeon1Text2 #This code is irrelevant and does nothing
    global adModeDungeon2Text2 #I have kept it as a reminder for myself
    global adModeDungeon3Text2 #Of the redunancies.
    global adModeDungeon4Text2 #Like gameData[0][0] is redundant too
    global adModeDungeon5Text2
    
    gameData = []
    with open(pFile, newline= '', encoding='utf-16') as csvFile :
        csvReader = csv.reader(csvFile)
        for row in csvReader :
            gameData.append(row)
    
    endModeHighScoreDisplayValueText.text = gameData[1][0]
    endModeHighScoreDisplayValueText.surf = pygame.Surface((standardFont.size(endModeHighScoreDisplayValueText.text)[0],standardFont.size(endModeHighScoreDisplayValueText.text)[1]))
    endModeHighScoreDisplayValueText.rect = endModeHighScoreDisplayValueText.surf.get_rect(center = (endModeHighScoreDisplayValueText.pos[0], endModeHighScoreDisplayValueText.pos[1]))
    endModeHighScoreDisplayValueText.surf = standardFont.render(endModeHighScoreDisplayValueText.text, True, endModeHighScoreDisplayValueText.colour)
    
    adModeDungeon1Text2.text = gameData[2][0]
    adModeDungeon1Text2.surf = pygame.Surface((smallFont.size(adModeDungeon1Text2.text)[0],smallFont.size(adModeDungeon1Text2.text)[1]))
    adModeDungeon1Text2.rect = adModeDungeon1Text2.surf.get_rect(center = (adModeDungeon1Text2.pos[0], adModeDungeon1Text2.pos[1]))
    adModeDungeon1Text2.surf = smallFont.render(adModeDungeon1Text2.text, True, adModeDungeon1Text2.colour)
    
    adModeDungeon2Text2.text = gameData[2][1]
    adModeDungeon2Text2.surf = pygame.Surface((smallFont.size(adModeDungeon2Text2.text)[0],smallFont.size(adModeDungeon2Text2.text)[1]))
    adModeDungeon2Text2.rect = adModeDungeon2Text2.surf.get_rect(center = (adModeDungeon2Text2.pos[0], adModeDungeon2Text2.pos[1]))
    adModeDungeon2Text2.surf = smallFont.render(adModeDungeon2Text2.text, True, adModeDungeon2Text2.colour)
    
    adModeDungeon3Text2.text = gameData[2][2]
    adModeDungeon3Text2.surf = pygame.Surface((smallFont.size(adModeDungeon3Text2.text)[0],smallFont.size(adModeDungeon3Text2.text)[1]))
    adModeDungeon3Text2.rect = adModeDungeon3Text2.surf.get_rect(center = (adModeDungeon3Text2.pos[0], adModeDungeon3Text2.pos[1]))
    adModeDungeon3Text2.surf = smallFont.render(adModeDungeon3Text2.text, True, adModeDungeon3Text2.colour)
    
    adModeDungeon4Text2.text = gameData[2][3]
    adModeDungeon4Text2.surf = pygame.Surface((smallFont.size(adModeDungeon4Text2.text)[0],smallFont.size(adModeDungeon4Text2.text)[1]))
    adModeDungeon4Text2.rect = adModeDungeon4Text2.surf.get_rect(center = (adModeDungeon4Text2.pos[0], adModeDungeon4Text2.pos[1]))
    adModeDungeon4Text2.surf = smallFont.render(adModeDungeon4Text2.text, True, adModeDungeon4Text2.colour)
    
    adModeDungeon5Text2.text = gameData[2][4]
    adModeDungeon5Text2.surf = pygame.Surface((smallFont.size(adModeDungeon5Text2.text)[0],smallFont.size(adModeDungeon5Text2.text)[1]))
    adModeDungeon5Text2.rect = adModeDungeon5Text2.surf.get_rect(center = (adModeDungeon5Text2.pos[0], adModeDungeon5Text2.pos[1]))
    adModeDungeon5Text2.surf = smallFont.render(adModeDungeon5Text2.text, True, adModeDungeon5Text2.colour)
    
    player.maxHealth = gameData[3][0]
    player.health = gameData[3][0]
    player.damage = gameData[3][1]
    player.Dspeed = gameData[3][2]
    player.Mspeed = gameData[3][3]
    player.range = gameData[3][4]
    
    settingsSoundButtonText.text = gameData[4][0] #Commented out and not removed to show that these buttons deliberately aren't centred
    #settingsSoundButtonText.surf = pygame.Surface((standardFont.size(settingsSoundButtonText.text)[0],standardFont.size(settingsSoundButtonText.text)[1]))
    #settingsSoundButtonText.rect = settingsSoundButtonText.surf.get_rect(center = (settingsSoundButtonText.pos[0], settingsSoundButtonText.pos[1]))
    settingsSoundButtonText.surf = standardFont.render(settingsSoundButtonText.text, True, settingsSoundButtonText.colour)
    
    settingsGraphicsButtonText.text = gameData[4][1]
    #settingsGraphicsButtonText.surf = pygame.Surface((standardFont.size(settingsGraphicsButtonText.text)[0],standardFont.size(settingsGraphicsButtonText.text)[1]))
    #settingsGraphicsButtonText.rect = settingsGraphicsButtonText.surf.get_rect(center = (settingsGraphicsButtonText.pos[0], settingsGraphicsButtonText.pos[1]))
    settingsGraphicsButtonText.surf = standardFont.render(settingsGraphicsButtonText.text, True, settingsGraphicsButtonText.colour)
    
    controlsAttackButtonText.text = gameData[5][0]
    controlsAttackButtonText.surf = pygame.Surface((standardFont.size(controlsAttackButtonText.text)[0],standardFont.size(controlsAttackButtonText.text)[1]))
    controlsAttackButtonText.rect = controlsAttackButtonText.surf.get_rect(center = (controlsAttackButtonText.pos[0], controlsAttackButtonText.pos[1]))
    controlsAttackButtonText.surf = standardFont.render(controlsAttackButtonText.text, True, controlsAttackButtonText.colour)

    controlsAction1ButtonText.text = gameData[5][1]
    controlsAction1ButtonText.surf = pygame.Surface((standardFont.size(controlsAction1ButtonText.text)[0],standardFont.size(controlsAction1ButtonText.text)[1]))
    controlsAction1ButtonText.rect = controlsAction1ButtonText.surf.get_rect(center = (controlsAction1ButtonText.pos[0], controlsAction1ButtonText.pos[1]))
    controlsAction1ButtonText.surf = standardFont.render(controlsAction1ButtonText.text, True, controlsAction1ButtonText.colour)
    
    controlsAction2ButtonText.text = gameData[5][2]
    controlsAction2ButtonText.surf = pygame.Surface((standardFont.size(controlsAction2ButtonText.text)[0],standardFont.size(controlsAction2ButtonText.text)[1]))
    controlsAction2ButtonText.rect = controlsAction2ButtonText.surf.get_rect(center = (controlsAction2ButtonText.pos[0], controlsAction2ButtonText.pos[1]))
    controlsAction2ButtonText.surf = standardFont.render(controlsAction2ButtonText.text, True, controlsAction2ButtonText.colour)

    currentFloor = gameData[6][0]
    currentDungeon = gameData[6][1]
    
    playerChosenUpgrades = gameData[7]
    playerDiscardedUpgrades = gameData[8]
    if currentDungeon == 1 :
        dungeon1Upgrades = gameData[9]
    elif currentDungeon == 2 :
        dungeon2Upgrades = gameData[9]
    elif currentDungeon == 3 :
        dungeon3Upgrades = gameData[9]
    elif currentDungeon == 4 :
        dungeon4Upgrades = gameData[9]
    elif currentDungeon == 5 :
        dungeon5Upgrades = gameData[9]

def writeCSV(pFile):
    with open(pFile, "w", newline= '',  encoding='utf-16') as csvFile :
        csvWriter = csv.writer(csvFile)
        csvWriter.writerows(gameData)
        
def checkCollide(pGroup):
    pList = pGroup.sprites()
    for i in range(0, len(pList)):
        for j in range(0, len(pList)):
            if i == j : #Without this, the code will check objects against themselves wasting resources/time
                pass
            #elif pList[i].colour == (0,0,255) or pList[j].colour == (0,0,255):
            #    pass
            elif pList[i].rect.colliderect(pList[j].rect):
                #print("colision between " + str(pList[i].colour) + " and " + str(pList[j].colour))
                if pList[i].colour == (0,0,200) and pList[i].flag == False and pList[j].colour != (50,50,0): #Only when the collider is a player will damage be dealt
                    player.health -= pList[j].damage #This stops enemy on enemy violence
                    pList[j].health -= player.damage
                    pList[i].flag = True
                    #print("damage happened block1")
                    #print(pList[i].health)
                elif pList[j].colour == (0,0,200) and pList[j].flag == False and pList[i].colour != (50,50,0):    
                    player.health -= pList[i].damage
                    pList[i].health -= player.damage
                    pList[j].flag = True
                    #print("damage happened block2")
                    
                if pList[i].colour == (0,0,255) and pList[i].flag == False: #Only when the collider is a player will damage be dealt
                    #player.health -= pList[j].damage #This stops enemy on enemy violence
                    pList[j].health -= player.damage
                    pList[i].flag = True
                    #print("damage happened block1")
                    #print(pList[i].health)
                elif pList[j].colour == (0,0,255) and pList[j].flag == False:    
                   #player.health -= pList[i].damage
                    pList[i].health -= player.damage
                    pList[j].flag = True
                    #print("damage happened block2")
                    
                    #print(pList[j].health)
                if pList[i].colour == (50,50,0) and pList[i].flag == False and pList[j].colour != (0,0,200):
                    pList[j].health -= player.damage
                    pList[i].flag = True
                    pList[j].direction[0] = player.direction[0] * -1
                    pList[j].direction[1] = player.direction[1] * -1
                    pList[j].move()
                    if pList[i].rect.colliderect(pList[j].rect):
                        pList[i].move()
                        
                elif pList[j].colour == (50,50,0) and pList[j].flag == False and pList[i].colour != (0,0,200):
                    pList[i].health -= player.damage
                    pList[j].flag = True
                    pList[i].direction[0] = player.direction[0] * -1
                    pList[i].direction[1] = player.direction[1] * -1
                    pList[i].move()
                    if pList[i].rect.colliderect(pList[j].rect):
                        pList[i].move()
                    
                if pList[i].colour == (50,50,0) or pList[j].colour == (50,50,0) :
                    pass
                elif math.fabs(pList[i].rect[0] - pList[j].rect[0]) > math.fabs(pList[i].rect[1] - pList[j].rect[1]) : #Edge Case: left/right bounces
                    if pList[i].direction[0] == pList[j].direction[0] :
                        if pList[i].velocity > pList[j].velocity :
                            if not(pList[i].colour == (0,0,255)):
                                pList[i].direction[0] *= -1
                                pList[i].move()
                                #print("L/R only i not shield")
                            else:
                                player.direction[0] *= -1
                                player.move()
                                pList[i].move(player)
                                #print("L/R only i is shield")
                                
                        elif pList[i].velocity < pList[j].velocity :
                            if not(pList[j].colour == (0,0,255)):
                                pList[j].direction[0] *= -1 #Direction is made negative/postitve to make the entities "bounce"
                                pList[j].move()
                                #print("L/R only j not shield")
                            else:
                                player.direction[0] *= -1
                                player.move()
                                pList[j].move(player)
                                #print("L/R only j is shield")
                    else:
                        
                        if not (pList[i].colour == (0,0,255)):
                            pList[i].direction[0] *= -1
                            pList[i].move()
                            #print("L/R both (i) not shield")
                        else:
                            player.direction[0] *= -1
                            player.move()
                            pList[i].move(player)
                           # print("L/R both (i) is shield")
                        if not (pList[j].colour == (0,0,255)):
                            pList[j].direction[0] *= -1
                            pList[j].move()
                           # print("L/R both (j) not shield")
                        else:
                            player.direction[0] *= -1
                            player.move()
                            pList[j].move(player)
                            #print("L/R both (j) is shield")
                                                                                                                       #Edge Case: top/bottom bounces
                elif math.fabs(pList[i].rect[0] - pList[j].rect[0]) < math.fabs(pList[i].rect[1] - pList[j].rect[1]) : #Math fabs is needed to stop
                    if pList[i].direction[1] == pList[j].direction[1] :                                                #negative differences being compared
                        if pList[i].velocity > pList[j].velocity :
                            if not(pList[i].colour == (0,0,255)):
                                pList[i].direction[1] *= -1
                                pList[i].move()
                                #print("T/B just i not shield")
                            else:
                                player.direction[1] *= -1
                                player.move()
                                pList[i].move(player)
                                #print("T/B just i is shield")
                        elif pList[i].velocity < pList[j].velocity :
                            if not(pList[j].colour == (0,0,255)):
                                pList[j].direction[1] *= -1
                                pList[j].move()
                                #print("T/B just j not shield")
                            else:
                                player.direction[1] *= -1
                                player.move()
                                pList[j].move(player)
                                #print("T/B just j is shield")
                    else:
                        if not (pList[i].colour == (0,0,255)):
                            pList[i].direction[1] *= -1
                            pList[i].move()
                           # print("T/B both (i) not shield")
                        else:
                            player.direction[1] *= -1
                            player.move()
                            pList[i].move(player)
                            #print("T/B both (i) is shield")
                        if not (pList[j].colour == (0,0,255)):
                            pList[j].direction[1] *= -1
                            pList[j].move()
                            #print("T/B both (j) not shield")
                        else:
                            player.direction[1] *= -1
                            player.move()
                            pList[j].move(player)
                            #print("T/B both (j) is shield")
                    
                elif (pList[i].rect[0] - pList[j].rect[0]) == (pList[i].rect[1] - pList[j].rect[1]) : #Edge Case: perfectly diagonal
                    if not (pList[i].colour == (0,0,255)):
                        pList[i].direction[0] *= -1
                        pList[i].direction[1] *= -1
                        pList[i].move()
                        #print("edge case (i) not shield")
                    else:
                        player.direction[0] *= -1
                        player.direction[1] *= -1
                        player.move()
                        pList[i].move(player)
                        #print("edge case (i) is shield")
                    if not (pList[j].colour == (0,0,255)):
                        pList[j].direction[0] *= -1
                        pList[j].direction[1] *= -1
                        pList[j].move()
                        #print("edge case (j) not shield")
                    else:
                        player.direction[0] *= -1
                        player.direction[1] *= -1
                        player.move()
                        pList[j].move(player)
                        #print("edge case (j) is shield")

def abilityDash():
    ratio = [0,0]
    magnitude = 0
    normRatio = [0,0]
    
    if pygame.mouse.get_pos()[0] < player.pos[0] :
        player.direction[0] = -1
    if pygame.mouse.get_pos()[0] > player.pos[0] :
        player.direction[0] = 1
    if pygame.mouse.get_pos()[1] < player.pos[1] :
        player.direction[1] = -1
    if pygame.mouse.get_pos()[1] > player.pos[1] :
        player.direction[1] = 1
    
    ratio[0] = math.fabs(pygame.mouse.get_pos()[0] - player.pos[0])
    ratio[1] = math.fabs(pygame.mouse.get_pos()[1] - player.pos[1])
    
    magnitude = math.sqrt((ratio[0] ** 2) + (ratio[1] ** 2))
    
    normRatio[0] = (ratio[0] / magnitude)
    normRatio[1] = (ratio[1] / magnitude)
    
    player.velocity[0] = math.ceil(normRatio[0] * (3 * (player.Mspeed/100)))
    player.velocity[1] = math.ceil(normRatio[1] * (3 * (player.Mspeed/100)))
 
def abilitySaviour():
    global saviourUsed
    player.health = 1
    saviourUsed = True
    

def abilityRampage():
    global preRampageDamage
    preRampageDamage = player.damage
    player.damage += 20
    
def deactivateRampage():
    player.damage = preRampageDamage
        
def abilityBurst():
    global preBurstDspeed
    preBurstDspeed = player.Dspeed
    player.Dspeed += 500
    
def deactivateBurst():
    player.Dspeed = preBurstDspeed
        
def abilityPulse():
    global prePulseRange
    prePulseRange = player.range
    player.range += 100
    
def deactivatePulse():
    player.range = prePulseRange
        

def checkDeath(pEntity):
    if pEntity.health <= 0 :
        pEntity.kill()
        return(True)
    
def activateShield():
    player.remove(gameplayCollisionsGroup)
    playerShield.add(gameplayCollisionsGroup)
    #print("shield Activated")
    
def deactivateShield():
    playerShield.remove(gameplayCollisionsGroup)
    global shieldActivationLength
    global shieldActivated
    shieldActivationLength = 0
    shieldActivated = False
    player.add(gameplayCollisionsGroup)
    
def activateSword():
    playerSword.add(gameplayCollisionsGroup)
    
def deactivateSword():
    playerSword.remove(gameplayCollisionsGroup)
    global swordActivationLength
    global swordActivated
    swordActivationLength = 0
    swordActivated = False

#def drawOverwriteDecision():
#    for entity in decisionWindowGroup :
#        displaySurface.blit(entity.surf, entity.rect)
#    displaySurface.blit(overwriteText.surf, overwriteText.rect)
#    displaySurface.blit(quitWindowText2.surf,  quitWindowText2.rect)

 
def drawQuitMenu():
    for entity in decisionWindowGroup :
        displaySurface.blit(entity.surf, entity.rect)
    displaySurface.blit(quitWindowText1.surf,  quitWindowText1.rect)
    displaySurface.blit(quitWindowText2.surf,  quitWindowText2.rect)


def quitCheck():
    global showQuitMenu #Treated as a local otherwise
    if pygame.key.get_pressed()[K_ESCAPE] :
        showQuitMenu = True

def showDeathScreen():
    for entity in decisionWindowGroup :
        displaySurface.blit(entity.surf, entity.rect)
    displaySurface.blit(deathWindowText.surf, deathWindowText.rect)
    
def showWinScreen():
    for entity in decisionWindowGroup :
        displaySurface.blit(entity.surf, entity.rect)
    displaySurface.blit(levelClearText1.surf, levelClearText1.rect)
    displaySurface.blit(levelClearText2.surf, levelClearText2.rect)
    
def showDungeonWinScreen():
    displaySurface.blit(decisionWindow.surf, decisionWindow.rect)
    displaySurface.blit(centreYesButton.surf, centreYesButton.rect)
    displaySurface.blit(centreYesButtonText.surf, centreYesButtonText.rect)
    displaySurface.blit(dungeonClearText1.surf, dungeonClearText1.rect)
    displaySurface.blit(dungeonClearText2.surf, dungeonClearText2.rect)
    
def showDungeonLoseScreen():
    displaySurface.blit(decisionWindow.surf, decisionWindow.rect)
    displaySurface.blit(centreNoButton.surf, centreNoButton.rect)
    displaySurface.blit(centreNoButtonText.surf, centreNoButtonText.rect)
    displaySurface.blit(gameOverText.surf, gameOverText.rect)
    
def resetLevel():
    playerSword.remove(gameplayCollisionsGroup)
    global swordActivationLength
    global swordActivated
    swordActivationLength = 0
    swordActivated = False
    player.health = player.maxHealth
    gameplayCollisionsGroup.add(enemy1)
    gameplayCollisionsGroup.add(enemy2)
    gameplayCollisionsGroup.add(enemy3)
    gameplayCollisionsGroup.add(enemy4)
    gameplayCollisionsGroup.add(player)
    for entity in gameplayCollisionsGroup :
        entity.health = entity.maxHealth
        gameplayMovementGroup.add(entity)
        entity.pos = [entity.x,entity.y]
        entity.direction = [1,1]
        
def reinsertItems(pList,pItem1,pItem2,pItem3,pItem4): #Takes in a dungeon list and 4 removed upgrades
    tempList = []                                     #and puts those 4 upgrades back into the dungeon list
    global playerChosenUpgrades
    global playerDiscardedUpgrades
    tempList.append(pItem1)
    tempList.append(pItem2)
    tempList.append(pItem3)
    tempList.append(pItem4)
    if pItem1 == "Sharpen":
        removeSharpenUpgrade()
    elif pItem1 == "Resist":
        removeResistUpgrade()
    elif pItem1 == "Fast":
        removeFastUpgrade()
    elif pItem1 == "Dextrous":
        removeDextrousUpgrade()
    elif pItem1 == "Extend":
        removeExtendUpgrade()
    elif pItem1 == "Honed":
        removeHonedUpgrade()
    elif pItem1 == "Deft":
        removeDeftUpgrade()
    elif pItem1 == "Broaden":
        removeBroadenUpgrade()
    elif pItem1 == "Boost":
        removeBoostUpgrade()
    elif pItem1 == "Blacksmith":
        removeBlacksmithUpgrade()
    elif pItem1 == "Stoic":
        removeStoicUpgrade()
    elif pItem1 == "Temper":
        removeTemperUpgrade()
    elif pItem1 == "Inflate":
        removeInflateUpgrade()
    elif pItem1 == "Exercise":
        removeExerciseUpgrade()
    elif pItem1 == "Unruly":
        removeUnrulyUpgrade()
    elif pItem1 == "Toughen":
       removeToughenUpgrade()
    elif pItem1 == "Speedier":
        removeSpeedierUpgrade()
    elif pItem1 == "Embiggen":
        removeEmbiggenUpgrade()
    elif pItem1 == "Smite":
        removeSmiteUpgrade()
    elif pItem1 == "Fortify":
        removeFortifyUpgrade()
    elif pItem1 == "Rush":
        removeRushUpgrade()
    elif pItem1 == "Lash":
        removeLashUpgrade()
    elif pItem1 == "Bolster":
        removeBolsterUpgrade()
    elif pItem1 == "Dash":
        removeDashUpgrade()
    elif pItem1 == "Saviour":
        removeSaviourUpgrade()
    elif pItem1 == "Rampage":
        removeRampageUpgrade()
    elif pItem1 == "Burst":
        removeBurstUpgrade()
    elif pItem1 == "Pulse":
        removePulseUpgrade()
    elif pItem1 == "Super":
        removeSuperUpgrade()
    playerChosenUpgrades.remove(pItem1)
    playerDiscardedUpgrades.remove(pItem2)
    playerDiscardedUpgrades.remove(pItem3)
    playerDiscardedUpgrades.remove(pItem4)
    for i in range(0,len(pList)) :
        tempList.append(pList[i])
    return(tempList)

#Upgrade Subprograms
#Ordered as Common|Uncommon|Rare|Ability
    #Basic Tier (Common)
def applySharpenUpgrade():
    player.damage += 1

def applyResistUpgrade():
    player.maxHealth += 1
    
def applyFastUpgrade():
    player.Mspeed += 10 #Adds 10%
    
def applyDextrousUpgrade():
    player.Dspeed += 10
    
def applyExtendUpgrade():
    player.range += 10
    
    #Better Tier (Uncommon)
def applyHonedUpgrade():
    player.damage += 1
    player.Dspeed += 10
    
def applyDeftUpgrade():
    player.Dspeed += 10
    player.Mspeed += 10
    
def applyBroadenUpgrade():
    player.maxHealth += 1
    player.range += 10
    
def applyBoostUpgrade():
    player.maxHealth += 1
    player.Mspeed += 10
    
def applyBlacksmithUpgrade():
    player.damage += 1
    player.range += 10
    
    #Trade-Off Tier (Uncommon)
def applyStoicUpgrade():
    player.maxHealth += 2
    player.Dspeed -= 10

def applyTemperUpgrade():
    player.damage += 2
    player.maxHealth -= 1

def applyInflateUpgrade():
    player.range += 20
    player.Mspeed -= 10
    
def applyExerciseUpgrade():
    player.Mspeed += 20
    player.range -= 10
    
def applyUnrulyUpgrade():
    player.Dspeed += 20
    player.damage -= 1
    
    #Weird Tier (Rare)
def applyToughenUpgrade():
    player.maxHealth += 2
    player.damage += 1
    player.Mspeed -= 10
    
def applySpeedierUpgrade():
    player.Dspeed += 20
    player.Mspeed += 10
    player.range -= 10
    
def applyEmbiggenUpgrade():
    player.range += 20
    player.maxHealth += 1
    player.damage -= 1

    #Strong Tier (Rare)
def applySmiteUpgrade():
    player.damage += 3

def applyFortifyUpgrade():
    player.maxHealth += 3
    
def applyRushUpgrade():
    player.Mspeed += 30 
    
def applyLashUpgrade():
    player.Dspeed += 30
    
def applyBolsterUpgrade():
    player.range += 30
    
    #Ability Tier
def applyDashUpgrade():
    global canDash
    player.Mspeed += 10
    canDash = True
    
def applySaviourUpgrade():
    global canSaviour
    player.maxHealth += 2
    canSaviour = True
    
def applyRampageUpgrade():
    global canRampage
    player.damage += 1
    canRampage = True
    
def applyBurstUpgrade():
    global canBurst
    player.Dspeed += 20
    canBurst = True
    
def applyPulseUpgrade():
    global canPulse
    player.range += 10
    canPulse = True
    
def applySuperUpgrade():
    global canSuper
    canSuper = True
    
# Undo Upgrade Functions
# Ordered as Common|Uncommon|Rare|Ability

    #Basic Tier (Common)
def removeSharpenUpgrade():
    player.damage -= 1

def removeResistUpgrade():
    player.maxHealth -= 1
    
def removeFastUpgrade():
    player.Mspeed -= 10 
    
def removeDextrousUpgrade():
    player.Dspeed -= 10
    
def removeExtendUpgrade():
    player.range -= 10
    
    #Better Tier (Uncommon)
def removeHonedUpgrade():
    player.damage -= 1
    player.Dspeed -= 10
    
def removeDeftUpgrade():
    player.Dspeed -= 10
    player.Mspeed -= 10
    
def removeBroadenUpgrade():
    player.maxHealth -= 1
    player.range -= 10
    
def removeBoostUpgrade():
    player.maxHealth -= 1
    player.Mspeed -= 10
    
def removeBlacksmithUpgrade():
    player.range -= 1
    player.range -= 10
    
    #Trade-Off Tier (Uncommon)
def removeStoicUpgrade():
    player.maxHealth -= 2
    player.Dspeed += 10

def removeTemperUpgrade():
    player.damage -= 2
    player.maxHealth += 1

def removeInflateUpgrade():
    player.range -= 20
    player.Mspeed += 10
    
def removeExerciseUpgrade():
    player.Mspeed -= 20
    player.range += 10
    
def removeUnrulyUpgrade():
    player.Dspeed -= 20
    player.damage += 1
    
    #Weird Tier (Rare)
def removeToughenUpgrade():
    player.maxHealth -= 2
    player.damage -= 1
    player.Mspeed += 10
    
def removeSpeedierUpgrade():
    player.Dspeed -= 20
    player.Mspeed -= 10
    player.range += 10
    
def removeEmbiggenUpgrade():
    player.range -= 20
    player.maxHealth -= 1
    player.damage += 1

    #Strong Tier (Rare)
def removeSmiteUpgrade():
    player.damage -= 3

def removeFortifyUpgrade():
    player.maxHealth -= 3
    
def removeRushUpgrade():
    player.Mspeed -= 30 
    
def removeLashUpgrade():
    player.Dspeed -= 30
    
def removeBolsterUpgrade():
    player.range -= 30
    
    #Ability Tier
def removeDashUpgrade():
    global canDash
    player.Mspeed -= 10
    canDash = False
    
def removeSaviourUpgrade():
    global canSaviour
    player.maxHealth -= 2
    canSaviour = False
    
def removeRampageUpgrade():
    global canRampage
    player.damage -= 1
    canRampage = False
    
def removeBurstUpgrade():
    global canBurst
    player.Dspeed -= 20
    canBurst = False
    
def removePulseUpgrade():
    global canPulse
    player.range -= 10
    canPulse = False
    
def removeSuperUpgrade():
    global canSuper
    canSuper = False

# Object Creation ================================================================================================================


# Title Screen Objects
titleScreenButton = Button(450, 420, 400, 120, (0, 0, 200), SAVESELECT)
gameTitleText = TitleText(450, 100,"SAVE THE SCREEN", (0,0,200))
gameTitleButtonText = TitleText(450, 420, "PLAY", (255, 255, 255))

# Decision Window Objects
decisionWindow = Window(450, 300, 650, 275, (0, 0, 255))
yesButton = Button(200, 390, 120, 75, (0, 255, 0), NONE)
noButton = Button(700, 390, 120, 75, (255, 0, 0), NONE)
centreYesButton = Button(450, 390, 120, 75, (0, 255, 0), NONE)
centreNoButton = Button(450, 390, 120, 75, (255, 0, 0), NONE)

#overwriteText = StandardText(450, 250, "Are you sure you want to overwrite this file?", (255,255,255))
quitWindowText1 = StandardText(450, 250, "Are you sure you want to quit the game?", (255,255,255))
quitWindowText2 = StandardText(450,280, "(Unsaved data will be lost!)", (255,255,255))
deathWindowText = StandardText(450, 250, "You Died! Wanna try again?", (255,255,255))

yesButtonText = StandardText(200, 390, "YES", (255, 255, 255))
centreYesButtonText = StandardText(450, 390, "YES", (255, 255, 255))
noButtonText = StandardText(700, 390, "NO", (255, 255, 255))
centreNoButtonText = StandardText(450, 390, "RETURN", (255, 255, 255))

levelClearText1 = TitleText(450, 220, "Level Clear!", (255,255,255))
levelClearText2 = StandardText(450, 270, "Do you wanna go to the next floor?", (255,255,255))

dungeonClearText1 = TitleText(450, 220, "Dungeon Clear!", (255,255,255))
dungeonClearText2 = StandardText(450, 270, "Time to move onto the next Dungeon", (255,255,255))
gameOverText = TitleText(450, 220, "Game Over!", (255,255,255))

#Save Select Objects
saveSelectTitle = Window(450, 50, 450, 50, (0,0,200))
saveSelectTitleText = TitleText(450,50, "SAVE SELECT", (255,255,255))

saveSelectFile1 = Button(200, 200, 200, 125, (0, 0, 200), NONE)
saveSelectFile1Highlight = Window(200,200,220,145, (0,255,0))
saveSelectFile1Text1 = StandardText(200, 160, "File 1", (255,255,255))
saveSelectFile1Text2 = StandardText(200,200, fileName1, (255,255,255))

saveSelectFile2 = Button(450, 200, 200, 125, (0, 0, 200), NONE)
saveSelectFile2Highlight = Window(450,200,220,145, (0,255,0))
saveSelectFile2Text1 = StandardText(450, 160, "File 2", (255,255,255))
saveSelectFile2Text2 = StandardText(450,200, fileName2, (255,255,255))

saveSelectFile3 = Button(700, 200, 200, 125, (0, 0, 200), NONE)
saveSelectFile3Highlight = Window(700,200,220,145, (0,255,0))
saveSelectFile3Text1 = StandardText(700, 160, "File 3", (255,255,255))
saveSelectFile3Text2 = StandardText(700,200, fileName3, (255,255,255))

saveSelectConfirmButton = Button(200, 425, 200, 50, (0, 0, 200), MAINMENU)
saveSelectConfirmButtonText = StandardText(200,425, "SELECT", (255,255,255))

#saveSelectCopyButton = Button(450, 425, 200, 50, (0, 0, 200), NONE)
#saveSelectCopyButtonText = StandardText(450,425, "COPY", (255,255,255))

#saveSelectDeleteButton = Button(700, 425, 200, 50, (0, 0, 200), NONE)
#saveSelectDeleteButtonText = StandardText(700,425, "DELETE", (255,255,255))


#Main Menu
mainMenuTitle = Window(450, 200, 225, 60, (0,0,200))
mainMenuTitleText = StandardText(450, 200, "Select Gamemode", (255,255,255))

mainMenuBackButton = Button(150, 75, 250, 100, (0,0,200), SAVESELECT)
mainMenuBackButtonText = StandardText(150, 75, "Back to Save Select", (255,255,255))

mainMenuQuitButton = Button(775, 75, 200, 100, (0,0,200), NONE)
mainMenuQuitButtonText = StandardText(775, 75, "Quit Game", (255,255,255))

mainMenuAdModeButton = Button(200, 400, 200, 100, (0,0,200), ADMODESELECT)
mainMenuAdModeButtonText = StandardText(200, 400, "Adventure Mode", (255,255,255))

mainMenuEndModeButton = Button(450, 400, 200, 100, (0,0,200), ENDMODESELECT)
mainMenuEndModeButtonText = StandardText(450, 400, "Endless Mode", (255,255,255))

mainMenuSettingsButton = Button(700, 400, 200, 100, (0,0,200), SETTINGS)
mainMenuSettingsButtonText = StandardText(700, 400, "Settings", (255,255,255))

#Adventure Mode

adModeTitle = Window(450, 200, 225, 60, (0,0,200))
adModeTitleText = StandardText(450, 200, "Dungeon Select", (255,255,255))

adModeBackButton = Button(150, 75, 250, 100, (0,0,200), MAINMENU)
adModeBackButtonText = StandardText(150, 75, "Back to Main Menu", (255,255,255))

adModeAchievementsButton = Button(150, 220, 250, 100, (0,0,200), ACHIEVEMENTS)
adModeAchievementsButtonText1 = StandardText(150, 195, "Achievements", (255,255,255))
adModeAchievementsButtonText2 = StandardText(150, 220, "&", (255,255,255))
adModeAchievementsButtonText3 = StandardText(150, 245, "Upgrade List", (255,255,255))

adModeDungeon1 = Button(112,390,120,200,(0,0,200),UPGRADES)
adModeDungeon1Text1 = SmallText(112,310,"Dungeon 1", (255,255,255))
adModeDungeon1Text2 = SmallText(112,375,"Complete!", (255,255,255))
adModeDungeon1Text3 = SmallText(112,450,"Floors: 1-3", (255,255,255))
adModeDungeon1Highlight = Window(112,390, 130,210, (255,255,0))

adModeDungeon2 = Button(337,390,120,200,(0,0,200),UPGRADES)
adModeDungeon2Text1 = SmallText(337,310,"Dungeon 2", (255,255,255))
adModeDungeon2Text2 = SmallText(337,375,"Complete!", (255,255,255))
adModeDungeon2Text3 = SmallText(337,450,"Floors: 3-10", (255,255,255))
adModeDungeon2Highlight = Window(337,390, 130,210, (255,255,0))

adModeDungeon3 = Button(562,390,120,200,(0,0,200),UPGRADES)
adModeDungeon3Text1 = SmallText(562,310,"Dungeon 3", (255,255,255))
adModeDungeon3Text2 = SmallText(562,375,"Complete!", (255,255,255))
adModeDungeon3Text3 = SmallText(562,450,"Floors: 11-25", (255,255,255))
adModeDungeon3Highlight = Window(562,390, 130,210, (255,255,0))

adModeDungeon4 = Button(787,390,120,200,(0,0,200),UPGRADES)
adModeDungeon4Text1 = SmallText(787,310,"Dungeon 4", (255,255,255))
adModeDungeon4Text2 = SmallText(787,375,"In Progress...", (255,255,255))
adModeDungeon4Text3 = SmallText(787,450,"Floors: 26-40", (255,255,255))
adModeDungeon4Highlight = Window(787,390, 130,210, (255,255,0))

adModeDungeon5 = Button(1012,390,120,200,(0,0,200),UPGRADES)
adModeDungeon5Text1 = SmallText(1012,310,"Dungeon 5", (255,255,255))
adModeDungeon5Text2 = SmallText(1012,375,"Not Complete", (255,255,255))
adModeDungeon5Text3 = SmallText(1012,450,"Floors: 41-70", (255,255,255))
adModeDungeon5Highlight = Window(1012,390, 130,210, (255,255,0))

adModeWeaponButton = ImageButton(802, 110, "sword new.png", NONE)
adModeWeaponButtonText = SmallText(802, 50, "Current Weapon:", (200,0,0))

#Endless Mode
endModeTitle = Window(450, 200, 225, 60, (0,0,200))
endModeTitleText = StandardText(450, 200, "Endless Dungeon", (255,255,255))

endModeHighScoreDisplay = Window(95, 220, 140, 100, (0,0,200))
endModeHighScoreDisplayText = StandardText(95,190, "High Score", (255,255,255))
endModeHighScoreDisplayValueText = StandardText(95, 225, "0", (255,255,255))

endModeBackButton = Button(150, 75, 250, 100, (0,0,200), MAINMENU)
endModeBackButtonText = StandardText(150, 75, "Back to Main Menu", (255,255,255))

endModePlayButton = Button(450, 400, 225, 100, (0,0,200), UPGRADES)
endModePlayButtonText = TitleText(450, 400, "PLAY", (255,255,255))

endModeAchievementsButton = Button(750, 425, 250, 100, (0,0,200), ACHIEVEMENTS)
endModeAchievementsButtonText1 = StandardText(750, 400, "Achievements", (255,255,255))
endModeAchievementsButtonText2 = StandardText(750, 425, "&", (255,255,255))
endModeAchievementsButtonText3 = StandardText(750, 450, "Upgrade List", (255,255,255))

endModeWeaponButton = ImageButton(802, 310, "sword new.png", NONE)
endModeWeaponButtonText = SmallText(802, 250, "Current Weapon:", (200,0,0))

#Settings

settingsBackButton = Button(150, 75, 250, 100, (0,0,200), MAINMENU)
settingsBackButtonText = StandardText(150, 75, "Back to Main Menu", (255,255,255))

settingsSoundButton = Button(450, 100, 300, 100, (0,0,200), NONE)
settingsSoundButtonText = StandardText(450, 100, "Game Volume: Medium", (255,255,255))

settingsGraphicsButton = Button(450, 250, 300, 100, (0,0,200), NONE)
settingsGraphicsButtonText = StandardText(450, 250, "Game Graphics: Medium", (255,255,255))

settingsControlsButton = Button(450, 400, 300, 100, (0,0,200), CONTROLS)
settingsControlsButtonText = StandardText(450, 400, "Change Game Controls", (255,255,255))

settingsSaveButton = Button(750, 250, 200, 100, (0,0,200), NONE)
settingsSaveButtonText = StandardText(750,250, "Save Changes", (255,255,255))
#Controls

controlsBackButton = Button(150, 75, 250, 100, (0,0,200), SETTINGS)
controlsBackButtonText = StandardText(150, 75, "Back to Settings", (255,255,255))

controlsAttackWindow = Window(300, 200, 200, 100, (0,0,200))
controlsAttackWindowText = StandardText(300,200, "Attack", (255,255,255))
controlsAttackButton = Button(600, 200, 200, 100, (0,0,200), NONE)
controlsAttackButtonText = StandardText(600,200, "X", (255,255,255))
controlsAttackButtonHighlight = Window(600,200, 220, 120, (0,255,0))

controlsAction1Window = Window(300,310, 200, 100, (0,0,200))
controlsAction1WindowText = StandardText(300,310, "Action 1", (255,255,255))
controlsAction1Button = Button(600,310, 200,100, (0,0,200), NONE)
controlsAction1ButtonText = StandardText(600,310,"Left click", (255,255,255))
controlsAction1ButtonHighlight = Window(600,310, 220, 120, (0,255,0))

controlsAction2Window = Window(300,420, 200, 100, (0,0,200))
controlsAction2WindowText = StandardText(300,420, "Action 2", (255,255,255))
controlsAction2Button = Button(600,420, 200,100, (0,0,200), NONE)
controlsAction2ButtonText = StandardText(600,420,"Z", (255,255,255))
controlsAction2ButtonHighlight = Window(600,420, 220, 120, (0,255,0))

controlsSaveButton = Button(750, 75, 200, 100, (0,0,200), NONE)
controlsSaveButtonText = StandardText(750,75, "Save Changes", (255,255,255))

#Gameplay Objects
playerHealthText = StandardText(70,15, "Health: 100", (255,255,255)) #Used to be HPText

enemy1 = Enemy(20,20, (255,255,255))        
enemy1.velocity[0] = 1
enemy1.velocity[1] = 2

enemy2 = Enemy(20,200, (0,0,0))     
enemy2.velocity[0] = 1
enemy2.velocity[1] = 3

enemy3 = Enemy(200,20, (0,0,0))        #Removed ALL instances of test or new
enemy3.velocity[0] = 4
enemy3.velocity[1] = 4

enemy4 = Enemy(200,200, (0,0,0))        
enemy4.velocity[0] = 5
enemy4.velocity[1] = 5


player = Player(700,99, (0,0,200))
abilityDash() #Randomises player movement direction

playerShield = Shield(100,99,(0,0,255))
playerSword = Sword(200,200,(50,50,0))

attackIndicatorWindow = Window(880,20,30,30,(255,0,0))
ability1IndicatorWindow = Window(880,60,30,30,(255,0,0))
ability2IndicatorWindow = Window(880,100,30,30,(255,0,0))

#Upgrade Menu
upgradesStatsWindow = Window(70,250,120,300,(0,0,200))
upgradesStatsWindowText = SmallText(70,120,"Stats:",(255,255,255))

upgradesStatsWindowHealthText = SmallText(41,160,"Health:",(255,255,255))
upgradesStatsWindowHealthTextValue = SmallText(95,160,"3",(255,255,255))

upgradesStatsWindowDamageText = SmallText(48,200,"Damage:",(255,255,255))
upgradesStatsWindowDamageTextValue = SmallText(95,200,"1",(255,255,255))

upgradesStatsWindowDSpeedText1 = SmallText(45,240,"Damage",(255,255,255))
upgradesStatsWindowDSpeedText2 = SmallText(40,260,"Speed:",(255,255,255))
upgradesStatsWindowDSpeedTextValue = SmallText(95,260,"X1.00",(255,255,255))

upgradesStatsWindowMSpeedText1 = SmallText(54,300,"Movement",(255,255,255))
upgradesStatsWindowMSpeedText2 = SmallText(40,320,"Speed:",(255,255,255))
upgradesStatsWindowMSpeedTextValue = SmallText(95,320,"X1.00",(255,255,255))

upgradesStatsWindowRangeText = SmallText(40,360,"Range:",(255,255,255))
upgradesStatsWindowRangeTextValue = SmallText(95,360,"X1.0",(255,255,255))


#upgradesUpgradeWindow = Window(830,250,120,300,(0,0,200))
#upgradesUpgradeWindowText1 = SmallText(830,120,"Upgrades:",(255,255,255))
#upgradesUpgradeWindowText2 = SmallText(830,160,"Upgrades1",(255,255,255))
#upgradesUpgradeWindowText3 = SmallText(830,185,"Upgrades2",(255,255,255))
#upgradesUpgradeWindowText4 = SmallText(830,210,"Upgrades3",(255,255,255))
#upgradesUpgradeWindowText5 = SmallText(830,235,"Upgrades4",(255,255,255))
#upgradesUpgradeWindowText6 = SmallText(830,260,"Upgrades5",(255,255,255))
#upgradesUpgradeWindowText7 = SmallText(830,285,"Upgrades6",(255,255,255))
#upgradesUpgradeWindowText8 = SmallText(830,310,"Upgrades7",(255,255,255))
#upgradesUpgradeWindowText9 = SmallText(830,335,"Upgrades8",(255,255,255))
#upgradesUpgradeWindowText10 = SmallText(830,360,"Upgrades9",(255,255,255))
#upgradesUpgradeWindowText11 = SmallText(830,385,"Upgrades10",(255,255,255))

#upgradesDungeonMapButton = Button(70,450,120,60,(0,0,200),NONE)
#upgradesDungeonMapButtonText = SmallText(70,450,"Dungeon Map",(255,255,255))
#upgradesUpgradeListButton = Button(830,450,120,60,(0,0,200),NONE)
#upgradesUpgradeListButtonText = SmallText(830,450,"Upgrade List",(255,255,255))

upgradesFloorCountWindow = Window(450,60,140,60,(0,0,200))
upgradesFloorCountWindowText = SmallText(450,60,"Floor:",(255,255,255))
upgradesQuitButton = Button(780,50,220,80,(0,0,200),MAINMENU)
upgradesQuitButtonText = StandardText(780,50,"Save and Quit",(255,255,255))

upgradesOption1Button = Button(240,325,120,250,(0,0,200),GAMEPLAY)
upgradesOption1ButtonText = SmallText(240,220,"UPGRADE1",(255,255,255))
upgradesOption1ButtonStat1 = SmallText(240,260,"Damage +1",(255,255,255))
upgradesOption1ButtonStat2 = SmallText(240,300,"Damage +1",(255,255,255))
upgradesOption1ButtonStat3 = SmallText(240,340,"Damage +1",(255,255,255))

upgradesOption2Button = Button(380,325,120,250,(0,0,200),GAMEPLAY)
upgradesOption2ButtonText = SmallText(380,220,"UPGRADE2",(255,255,255))
upgradesOption2ButtonStat1 = SmallText(380,260,"Damage +1",(255,255,255))
upgradesOption2ButtonStat2 = SmallText(380,300,"Damage +1",(255,255,255))
upgradesOption2ButtonStat3 = SmallText(380,340,"Damage +1",(255,255,255))

upgradesOption3Button = Button(520,325,120,250,(0,0,200),GAMEPLAY)
upgradesOption3ButtonText = SmallText(520,220,"UPGRADE3",(255,255,255))
upgradesOption3ButtonStat1 = SmallText(520,260,"Damage +1",(255,255,255))
upgradesOption3ButtonStat2 = SmallText(520,300,"Damage +1",(255,255,255))
upgradesOption3ButtonStat3 = SmallText(520,340,"Damage +1",(255,255,255))

upgradesOption4Button = Button(660,325,120,250,(0,0,200),GAMEPLAY)
upgradesOption4ButtonText = SmallText(660,220,"UPGRADE4",(255,255,255))
upgradesOption4ButtonStat1 = SmallText(660,260,"Damage +1",(255,255,255))
upgradesOption4ButtonStat2 = SmallText(660,300,"Damage +1",(255,255,255))
upgradesOption4ButtonStat3 = SmallText(660,340,"Damage +1",(255,255,255))

#Achievements

achievementsBackButtonAdMode = Button(150, 75, 250, 100, (0,0,200), ADMODESELECT)
achievementsBackButtonAdModeText1 = StandardText(150, 50, "Back to", (255,255,255))
achievementsBackButtonAdModeText2 = StandardText(150, 90, "Adventure Mode", (255,255,255))

achievementsBackButtonEndMode = Button(150, 75, 250, 100, (0,0,200), ENDMODESELECT)
achievementsBackButtonEndModeText1 = StandardText(150, 50, "Back to", (255,255,255))
achievementsBackButtonEndModeText2 = StandardText(150, 90, "Endless Mode", (255,255,255))

achievementsTile1 = Window(90,195,120,120, (0,0,200))
achievementsTile2 = Window(210,195,120,120, (0,100,200))
achievementsTile3 = Window(330,195,120,120, (0,0,200))
achievementsTile4 = Window(450,195,120,120, (0,100,200))
achievementsTile5 = Window(570,195,120,120, (0,0,200))
achievementsTile6 = Window(690,195,120,120, (0,100,200))
achievementsTile7 = Window(810,195,120,120, (0,0,200))
achievementsTile8 = Window(90,315,120,120, (0,100,200))
achievementsTile9 = Window(210,315,120,120, (0,0,200))
achievementsTile10 = Window(330,315,120,120, (0,100,200))
achievementsTile11 = Window(450,315,120,120, (0,0,200))
achievementsTile12 = Window(570,315,120,120, (0,100,200))
achievementsTile13 = Window(690,315,120,120, (0,0,200))
achievementsTile14 = Window(810,315,120,120, (0,100,200))
achievementsTile15 = Window(90,435,120,120, (0,0,200))
achievementsTile16 = Window(210,435,120,120, (0,100,200))
achievementsTile17 = Window(330,435,120,120, (0,0,200))
achievementsTile18 = Window(450,435,120,120, (0,100,200))
achievementsTile19 = Window(570,435,120,120, (0,0,200))
achievementsTile20 = Window(690,435,120,120, (0,100,200))
achievementsTile21 = Window(810,435,120,120, (0,0,200))

achievementsTile22 = Window(10090,195,120,120, (0,0,200))
achievementsTile23 = Window(10210,195,120,120, (0,100,200))
achievementsTile24 = Window(10330,195,120,120, (0,0,200))
achievementsTile25 = Window(10450,195,120,120, (0,100,200))
achievementsTile26 = Window(10570,195,120,120, (0,0,200))
achievementsTile27 = Window(10690,195,120,120, (0,100,200))
achievementsTile28 = Window(10810,195,120,120, (0,0,200))
achievementsTile29 = Window(10090,315,120,120, (0,100,200))
achievementsTile30 = Window(10210,315,120,120, (0,0,200))
achievementsTile31 = Window(10330,315,120,120, (0,100,200))
achievementsTile32 = Window(10450,315,120,120, (0,0,200))
achievementsTile33 = Window(10570,315,120,120, (0,100,200))
achievementsTile34 = Window(10690,315,120,120, (0,0,200))
achievementsTile35 = Window(10810,315,120,120, (0,100,200))
achievementsTile36 = Window(10090,435,120,120, (0,0,200))
achievementsTile37 = Window(10210,435,120,120, (0,100,200))
achievementsTile38 = Window(10330,435,120,120, (0,0,200))
achievementsTile39 = Window(10450,435,120,120, (0,100,200))
achievementsTile40 = Window(10570,435,120,120, (0,0,200))
achievementsTile41 = Window(10690,435,120,120, (0,100,200))
achievementsTile42 = Window(10810,435,120,120, (0,0,200))

achievementsTile43 = Window(20090, 195, 120,120, (0,0,200))
achievementsTile44 = Window(20210, 195, 120,120, (0,100,200))
achievementsTile45 = Window(20330,195,120,120, (0,0,200))
achievementsTile46 = Window(20450,195,120,120, (0,100,200))
achievementsTile47 = Window(20570,195,120,120, (0,0,200))
achievementsTile48 = Window(20690,195,120,120, (0,100,200))
achievementsTile49 = Window(20810,195,120,120, (0,0,200))
achievementsTile50 = Window(20090,315,120,120, (0,100,200))
achievementsTile51 = Window(20210,315,120,120, (0,0,200))
achievementsTile52 = Window(20330,315,120,120, (0,100,200))
achievementsTile53 = Window(20450,315,120,120, (0,0,200))
achievementsTile54 = Window(20570,315,120,120, (0,100,200))
achievementsTile55 = Window(20690,315,120,120, (0,0,200))
achievementsTile56 = Window(20810,315,120,120, (0,100,200))
achievementsTile57 = Window(20090,435,120,120, (0,0,200))
achievementsTile58 = Window(20210,435,120,120, (0,100,200))
achievementsTile59 = Window(20330,435,120,120, (0,0,200))
achievementsTile60 = Window(20450,435,120,120, (0,100,200))
achievementsTile61 = Window(20570,435,120,120, (0,0,200))
achievementsTile62 = Window(20690,435,120,120, (0,100,200))
achievementsTile63 = Window(20810,435,120,120, (0,0,200))

achievementsTile1Text1 = SmallText(90,150, "Upgrade 1", (255,255,255))
achievementsTile1Text2 = SmallText(90,172, "Stat Change 1", (255,255,255))
achievementsTile1Text3 = SmallText(90,195, "", (255,255,255))
achievementsTile1Text4 = SmallText(90,217, "", (255,255,255))
achievementsTile1Text5 = SmallText(90,240, "Found: 3/12", (255,255,255))

achievementsTile2Text1 = SmallText(210,150, "Upgrade 1", (255,255,255))
achievementsTile2Text2 = SmallText(210,172, "Stat Change 1", (255,255,255))
achievementsTile2Text3 = SmallText(210,195, "", (255,255,255))
achievementsTile2Text4 = SmallText(210,217, "", (255,255,255))
achievementsTile2Text5 = SmallText(210,240, "Found: 3/12", (255,255,255))

achievementsTile3Text1 = SmallText(330,150, "Upgrade 1", (255,255,255))
achievementsTile3Text2 = SmallText(330,172, "Stat Change 1", (255,255,255))
achievementsTile3Text3 = SmallText(330,195, "", (255,255,255))
achievementsTile3Text4 = SmallText(330,217, "", (255,255,255))
achievementsTile3Text5 = SmallText(330,240, "Found: 3/12", (255,255,255))

achievementsTile4Text1 = SmallText(450,150, "Upgrade 1", (255,255,255))
achievementsTile4Text2 = SmallText(450,172, "Stat Change 1", (255,255,255))
achievementsTile4Text3 = SmallText(450,195, "", (255,255,255))
achievementsTile4Text4 = SmallText(450,217, "", (255,255,255))
achievementsTile4Text5 = SmallText(450,240, "Found: 3/12", (255,255,255))

achievementsTile5Text1 = SmallText(570,150, "Upgrade 1", (255,255,255))
achievementsTile5Text2 = SmallText(570,172, "Stat Change 1", (255,255,255))
achievementsTile5Text3 = SmallText(570,195, "", (255,255,255))
achievementsTile5Text4 = SmallText(570,217, "", (255,255,255))
achievementsTile5Text5 = SmallText(570,240, "Found: 3/12", (255,255,255))

achievementsTile6Text1 = SmallText(690,150, "Upgrade 1", (255,255,255))
achievementsTile6Text2 = SmallText(690,172, "Stat Change 1", (255,255,255))
achievementsTile6Text3 = SmallText(690,195, "Stat Change 2", (255,255,255))
achievementsTile6Text4 = SmallText(690,217, "", (255,255,255))
achievementsTile6Text5 = SmallText(690,240, "Found: 3/12", (255,255,255))

achievementsTile7Text1 = SmallText(810,150, "Upgrade 1", (255,255,255))
achievementsTile7Text2 = SmallText(810,172, "Stat Change 1", (255,255,255))
achievementsTile7Text3 = SmallText(810,195, "Stat Change 2", (255,255,255))
achievementsTile7Text4 = SmallText(810,217, "Stat Change 3", (255,255,255))
achievementsTile7Text5 = SmallText(810,240, "Found: 3/12", (255,255,255))

achievementsTile8Text1 = SmallText(90,270, "Upgrade 1", (255,255,255))
achievementsTile8Text2 = SmallText(90,292, "Stat Change 1", (255,255,255))
achievementsTile8Text3 = SmallText(90,315, "Stat Change 2", (255,255,255))
achievementsTile8Text4 = SmallText(90,337, "", (255,255,255))
achievementsTile8Text5 = SmallText(90,360, "Found: 3/12", (255,255,255))

achievementsTile9Text1 = SmallText(210,270, "Upgrade 1", (255,255,255))
achievementsTile9Text2 = SmallText(210,292, "Stat Change 1", (255,255,255))
achievementsTile9Text3 = SmallText(210,315, "Stat Change 2", (255,255,255))
achievementsTile9Text4 = SmallText(210,337, "", (255,255,255))
achievementsTile9Text5 = SmallText(210,360, "Found: 3/12", (255,255,255))

achievementsTile10Text1 = SmallText(330,270, "Upgrade 1", (255,255,255))
achievementsTile10Text2 = SmallText(330,292, "Stat Change 1", (255,255,255))
achievementsTile10Text3 = SmallText(330,315, "Stat Change 2", (255,255,255))
achievementsTile10Text4 = SmallText(330,337, "Stat Change 3", (255,255,255))
achievementsTile10Text5 = SmallText(330,360, "Found: 3/12", (255,255,255))

achievementsTile11Text1 = SmallText(450,270, "Upgrade 1", (255,255,255))
achievementsTile11Text2 = SmallText(450,292, "Stat Change 1", (255,255,255))
achievementsTile11Text3 = SmallText(450,315, "", (255,255,255))
achievementsTile11Text4 = SmallText(450,337, "", (255,255,255))
achievementsTile11Text5 = SmallText(450,360, "Found: 3/12", (255,255,255))

achievementsTile12Text1 = SmallText(570,270, "Upgrade 1", (255,255,255))
achievementsTile12Text2 = SmallText(570,292, "Stat Change 1", (255,255,255))
achievementsTile12Text3 = SmallText(570,315, "Stat Change 2", (255,255,255))
achievementsTile12Text4 = SmallText(570,337, "", (255,255,255))
achievementsTile12Text5 = SmallText(570,360, "Found: 3/12", (255,255,255))

achievementsTile13Text1 = SmallText(690,270, "Upgrade 1", (255,255,255))
achievementsTile13Text2 = SmallText(690,292, "Stat Change 1", (255,255,255))
achievementsTile13Text3 = SmallText(690,315, "Stat Change 2", (255,255,255))
achievementsTile13Text4 = SmallText(690,337, "", (255,255,255))
achievementsTile13Text5 = SmallText(690,360, "Found: 3/12", (255,255,255))

achievementsTile14Text1 = SmallText(810,270, "Upgrade 1", (255,255,255))
achievementsTile14Text2 = SmallText(810,292, "Stat Change 1", (255,255,255))
achievementsTile14Text3 = SmallText(810,315, "Stat Change 2", (255,255,255))
achievementsTile14Text4 = SmallText(810,337, "", (255,255,255))
achievementsTile14Text5 = SmallText(810,360, "Found: 3/12", (255,255,255))

achievementsTile15Text1 = SmallText(90,390, "Upgrade 1", (255,255,255))
achievementsTile15Text2 = SmallText(90,412, "Stat Change 1", (255,255,255))
achievementsTile15Text3 = SmallText(90,435, "Stat Change 2", (255,255,255))
achievementsTile15Text4 = SmallText(90,457, "", (255,255,255))
achievementsTile15Text5 = SmallText(90,480, "Found: 3/12", (255,255,255))

achievementsTile16Text1 = SmallText(210,390, "Upgrade 1", (255,255,255))
achievementsTile16Text2 = SmallText(210,412, "Stat Change 1", (255,255,255))
achievementsTile16Text3 = SmallText(210,435, "Stat Change 2", (255,255,255))
achievementsTile16Text4 = SmallText(210,457, "Stat Change 3", (255,255,255))
achievementsTile16Text5 = SmallText(210,480, "Found: 3/12", (255,255,255))

achievementsTile17Text1 = SmallText(330,390, "Upgrade 1", (255,255,255))
achievementsTile17Text2 = SmallText(330,412, "Stat Change 1", (255,255,255))
achievementsTile17Text3 = SmallText(330,435, "Stat Change 2", (255,255,255))
achievementsTile17Text4 = SmallText(330,457, "Stat Change 3", (255,255,255))
achievementsTile17Text5 = SmallText(330,480, "Found: 3/12", (255,255,255))

achievementsTile18Text1 = SmallText(450,390, "Upgrade 1", (255,255,255))
achievementsTile18Text2 = SmallText(450,412, "Stat Change 1", (255,255,255))
achievementsTile18Text3 = SmallText(450,435, "Stat Change 2", (255,255,255))
achievementsTile18Text4 = SmallText(450,457, "Stat Change 3", (255,255,255))
achievementsTile18Text5 = SmallText(450,480, "Found: 3/12", (255,255,255))

achievementsTile19Text1 = SmallText(570,390, "Upgrade 1", (255,255,255))
achievementsTile19Text2 = SmallText(570,412, "Stat Change 1", (255,255,255))
achievementsTile19Text3 = SmallText(570,435, "Stat Change 2", (255,255,255))
achievementsTile19Text4 = SmallText(570,457, "", (255,255,255))
achievementsTile19Text5 = SmallText(570,480, "Found: 3/12", (255,255,255))

achievementsTile20Text1 = SmallText(690,390, "Upgrade 1", (255,255,255))
achievementsTile20Text2 = SmallText(690,412, "Stat Change 1", (255,255,255))
achievementsTile20Text3 = SmallText(690,435, "Stat Change 2", (255,255,255))
achievementsTile20Text4 = SmallText(690,457, "Stat Change 3", (255,255,255))
achievementsTile20Text5 = SmallText(690,480, "Found: 3/12", (255,255,255))

achievementsTile21Text1 = SmallText(810,390, "Upgrade 1", (255,255,255))
achievementsTile21Text2 = SmallText(810,412, "Stat Change 1", (255,255,255))
achievementsTile21Text3 = SmallText(810,435, "", (255,255,255))
achievementsTile21Text4 = SmallText(810,457, "", (255,255,255))
achievementsTile21Text5 = SmallText(810,480, "Found: 3/12", (255,255,255))

achievementsTile22Text1 = SmallText(10090,150, "Upgrade 1", (255,255,255))
achievementsTile22Text2 = SmallText(10090,172, "Stat Change 1", (255,255,255))
achievementsTile22Text3 = SmallText(10090,195, "Stat Change 2", (255,255,255))
achievementsTile22Text4 = SmallText(10090,217, "Stat Change 3", (255,255,255))
achievementsTile22Text5 = SmallText(10090,240, "Found: 3/12", (255,255,255))

achievementsTile23Text1 = SmallText(10210,150, "Upgrade 1", (255,255,255))
achievementsTile23Text2 = SmallText(10210,172, "Stat Change 1", (255,255,255))
achievementsTile23Text3 = SmallText(10210,195, "Stat Change 2", (255,255,255))
achievementsTile23Text4 = SmallText(10210,217, "Stat Change 3", (255,255,255))
achievementsTile23Text5 = SmallText(10210,240, "Found: 3/12", (255,255,255))

achievementsTile24Text1 = SmallText(10330,150, "Upgrade 1", (255,255,255))
achievementsTile24Text2 = SmallText(10330,172, "Stat Change 1", (255,255,255))
achievementsTile24Text3 = SmallText(10330,195, "", (255,255,255))
achievementsTile24Text4 = SmallText(10330,217, "", (255,255,255))
achievementsTile24Text5 = SmallText(10330,240, "Found: 3/12", (255,255,255))

achievementsTile25Text1 = SmallText(10450,150, "Upgrade 1", (255,255,255))
achievementsTile25Text2 = SmallText(10450,172, "Stat Change 1", (255,255,255))
achievementsTile25Text3 = SmallText(10450,195, "", (255,255,255))
achievementsTile25Text4 = SmallText(10450,217, "", (255,255,255))
achievementsTile25Text5 = SmallText(10450,240, "Found: 3/12", (255,255,255))

achievementsTile26Text1 = SmallText(10570,150, "Upgrade 1", (255,255,255))
achievementsTile26Text2 = SmallText(10570,172, "Stat Change 1", (255,255,255))
achievementsTile26Text3 = SmallText(10570,195, "", (255,255,255))
achievementsTile26Text4 = SmallText(10570,217, "", (255,255,255))
achievementsTile26Text5 = SmallText(10570,240, "Found: 3/12", (255,255,255))

achievementsTile27Text1 = SmallText(10690,150, "Upgrade 1", (255,255,255))
achievementsTile27Text2 = SmallText(10690,172, "Stat Change 1", (255,255,255))
achievementsTile27Text3 = SmallText(10690,195, "Stat Change 2", (255,255,255))
achievementsTile27Text4 = SmallText(10690,217, "", (255,255,255))
achievementsTile27Text5 = SmallText(10690,240, "Found: 3/12", (255,255,255))

achievementsTile28Text1 = SmallText(10810,150, "Upgrade 1", (255,255,255))
achievementsTile28Text2 = SmallText(10810,172, "Stat Change 1", (255,255,255))
achievementsTile28Text3 = SmallText(10810,195, "Stat Change 2", (255,255,255))
achievementsTile28Text4 = SmallText(10810,217, "Stat Change 3", (255,255,255))
achievementsTile28Text5 = SmallText(10810,240, "Found: 3/12", (255,255,255))

achievementsTile29Text1 = SmallText(10090,270, "Upgrade 1", (255,255,255))
achievementsTile29Text2 = SmallText(10090,292, "Stat Change 1", (255,255,255))
achievementsTile29Text3 = SmallText(10090,315, "Stat Change 2", (255,255,255))
achievementsTile29Text4 = SmallText(10090,337, "", (255,255,255))
achievementsTile29Text5 = SmallText(10090,360, "Found: 3/12", (255,255,255))

achievementsTile30Text1 = SmallText(10210,270, "Upgrade 1", (255,255,255))
achievementsTile30Text2 = SmallText(10210,292, "Stat Change 1", (255,255,255))
achievementsTile30Text3 = SmallText(10210,315, "Stat Change 2", (255,255,255))
achievementsTile30Text4 = SmallText(10210,337, "", (255,255,255))
achievementsTile30Text5 = SmallText(10210,360, "Found: 3/12", (255,255,255))

achievementsTile31Text1 = SmallText(10330,270, "Upgrade 1", (255,255,255))
achievementsTile31Text2 = SmallText(10330,292, "Stat Change 1", (255,255,255))
achievementsTile31Text3 = SmallText(10330,315, "Stat Change 2", (255,255,255))
achievementsTile31Text4 = SmallText(10330,337, "Stat Change 3", (255,255,255))
achievementsTile31Text5 = SmallText(10330,360, "Found: 3/12", (255,255,255))

achievementsTile32Text1 = SmallText(10450,270, "Upgrade 1", (255,255,255))
achievementsTile32Text2 = SmallText(10450,292, "Stat Change 1", (255,255,255))
achievementsTile32Text3 = SmallText(10450,315, "", (255,255,255))
achievementsTile32Text4 = SmallText(10450,337, "", (255,255,255))
achievementsTile32Text5 = SmallText(10450,360, "Found: 3/12", (255,255,255))

achievementsTile33Text1 = SmallText(10570,270, "Upgrade 1", (255,255,255))
achievementsTile33Text2 = SmallText(10570,292, "Stat Change 1", (255,255,255))
achievementsTile33Text3 = SmallText(10570,315, "Stat Change 2", (255,255,255))
achievementsTile33Text4 = SmallText(10570,337, "", (255,255,255))
achievementsTile33Text5 = SmallText(10570,360, "Found: 3/12", (255,255,255))

achievementsTile34Text1 = SmallText(10690,270, "Upgrade 1", (255,255,255))
achievementsTile34Text2 = SmallText(10690,292, "Stat Change 1", (255,255,255))
achievementsTile34Text3 = SmallText(10690,315, "Stat Change 2", (255,255,255))
achievementsTile34Text4 = SmallText(10690,337, "", (255,255,255))
achievementsTile34Text5 = SmallText(10690,360, "Found: 3/12", (255,255,255))

achievementsTile35Text1 = SmallText(10810,270, "Upgrade 1", (255,255,255))
achievementsTile35Text2 = SmallText(10810,292, "Stat Change 1", (255,255,255))
achievementsTile35Text3 = SmallText(10810,315, "Stat Change 2", (255,255,255))
achievementsTile35Text4 = SmallText(10810,337, "", (255,255,255))
achievementsTile35Text5 = SmallText(10810,360, "Found: 3/12", (255,255,255))

achievementsTile36Text1 = SmallText(10090,390, "Upgrade 1", (255,255,255))
achievementsTile36Text2 = SmallText(10090,412, "Stat Change 1", (255,255,255))
achievementsTile36Text3 = SmallText(10090,435, "Stat Change 2", (255,255,255))
achievementsTile36Text4 = SmallText(10090,457, "", (255,255,255))
achievementsTile36Text5 = SmallText(10090,480, "Found: 3/12", (255,255,255))

achievementsTile37Text1 = SmallText(10210,390, "Upgrade 1", (255,255,255))
achievementsTile37Text2 = SmallText(10210,412, "Stat Change 1", (255,255,255))
achievementsTile37Text3 = SmallText(10210,435, "Stat Change 2", (255,255,255))
achievementsTile37Text4 = SmallText(10210,457, "Stat Change 3", (255,255,255))
achievementsTile37Text5 = SmallText(10210,480, "Found: 3/12", (255,255,255))

achievementsTile38Text1 = SmallText(10330,390, "Upgrade 1", (255,255,255))
achievementsTile38Text2 = SmallText(10330,412, "Stat Change 1", (255,255,255))
achievementsTile38Text3 = SmallText(10330,435, "Stat Change 2", (255,255,255))
achievementsTile38Text4 = SmallText(10330,457, "Stat Change 3", (255,255,255))
achievementsTile38Text5 = SmallText(10330,480, "Found: 3/12", (255,255,255))

achievementsTile39Text1 = SmallText(10450,390, "Upgrade 1", (255,255,255))
achievementsTile39Text2 = SmallText(10450,412, "Stat Change 1", (255,255,255))
achievementsTile39Text3 = SmallText(10450,435, "Stat Change 2", (255,255,255))
achievementsTile39Text4 = SmallText(10450,457, "Stat Change 3", (255,255,255))
achievementsTile39Text5 = SmallText(10450,480, "Found: 3/12", (255,255,255))

achievementsTile40Text1 = SmallText(10570,390, "Upgrade 1", (255,255,255))
achievementsTile40Text2 = SmallText(10570,412, "Stat Change 1", (255,255,255))
achievementsTile40Text3 = SmallText(10570,435, "Stat Change 2", (255,255,255))
achievementsTile40Text4 = SmallText(10570,457, "", (255,255,255))
achievementsTile40Text5 = SmallText(10570,480, "Found: 3/12", (255,255,255))

achievementsTile41Text1 = SmallText(10690,390, "Upgrade 1", (255,255,255))
achievementsTile41Text2 = SmallText(10690,412, "Stat Change 1", (255,255,255))
achievementsTile41Text3 = SmallText(10690,435, "Stat Change 2", (255,255,255))
achievementsTile41Text4 = SmallText(10690,457, "Stat Change 3", (255,255,255))
achievementsTile41Text5 = SmallText(10690,480, "Found: 3/12", (255,255,255))

achievementsTile42Text1 = SmallText(10810,390, "Upgrade 1", (255,255,255))
achievementsTile42Text2 = SmallText(10810,412, "Stat Change 1", (255,255,255))
achievementsTile42Text3 = SmallText(10810,435, "", (255,255,255))
achievementsTile42Text4 = SmallText(10810,457, "", (255,255,255))
achievementsTile42Text5 = SmallText(10810,480, "Found: 3/12", (255,255,255))

achievementsTile43Text1 = SmallText(20090,150, "Upgrade 1", (255,255,255))
achievementsTile43Text2 = SmallText(20090,172, "Stat Change 1", (255,255,255))
achievementsTile43Text3 = SmallText(20090,195, "", (255,255,255))
achievementsTile43Text4 = SmallText(20090,217, "", (255,255,255))
achievementsTile43Text5 = SmallText(20090,240, "Found: 3/12", (255,255,255))

achievementsTile44Text1 = SmallText(20210,150, "Upgrade 1", (255,255,255))
achievementsTile44Text2 = SmallText(20210,172, "Stat Change 1", (255,255,255))
achievementsTile44Text3 = SmallText(20210,195, "", (255,255,255))
achievementsTile44Text4 = SmallText(20210,217, "", (255,255,255))
achievementsTile44Text5 = SmallText(20210,240, "Found: 3/12", (255,255,255))

achievementsTile45Text1 = SmallText(20330,150, "Upgrade 1", (255,255,255))
achievementsTile45Text2 = SmallText(20330,172, "Stat Change 1", (255,255,255))
achievementsTile45Text3 = SmallText(20330,195, "", (255,255,255))
achievementsTile45Text4 = SmallText(20330,217, "", (255,255,255))
achievementsTile45Text5 = SmallText(20330,240, "Found: 3/12", (255,255,255))

achievementsTile46Text1 = SmallText(20450,150, "Upgrade 1", (255,255,255))
achievementsTile46Text2 = SmallText(20450,172, "Stat Change 1", (255,255,255))
achievementsTile46Text3 = SmallText(20450,195, "", (255,255,255))
achievementsTile46Text4 = SmallText(20450,217, "", (255,255,255))
achievementsTile46Text5 = SmallText(20450,240, "Found: 3/12", (255,255,255))

achievementsTile47Text1 = SmallText(20570,150, "Upgrade 1", (255,255,255))
achievementsTile47Text2 = SmallText(20570,172, "Stat Change 1", (255,255,255))
achievementsTile47Text3 = SmallText(20570,195, "", (255,255,255))
achievementsTile47Text4 = SmallText(20570,217, "", (255,255,255))
achievementsTile47Text5 = SmallText(20570,240, "Found: 3/12", (255,255,255))

achievementsTile48Text1 = SmallText(20690,150, "Upgrade 1", (255,255,255))
achievementsTile48Text2 = SmallText(20690,172, "Stat Change 1", (255,255,255))
achievementsTile48Text3 = SmallText(20690,195, "Stat Change 2", (255,255,255))
achievementsTile48Text4 = SmallText(20690,217, "", (255,255,255))
achievementsTile48Text5 = SmallText(20690,240, "Found: 3/12", (255,255,255))

achievementsTile49Text1 = SmallText(20810,150, "Upgrade 1", (255,255,255))
achievementsTile49Text2 = SmallText(20810,172, "Stat Change 1", (255,255,255))
achievementsTile49Text3 = SmallText(20810,195, "Stat Change 2", (255,255,255))
achievementsTile49Text4 = SmallText(20810,217, "Stat Change 3", (255,255,255))
achievementsTile49Text5 = SmallText(20810,240, "Found: 3/12", (255,255,255))

achievementsTile50Text1 = SmallText(20090,270, "Upgrade 1", (255,255,255))
achievementsTile50Text2 = SmallText(20090,292, "Stat Change 1", (255,255,255))
achievementsTile50Text3 = SmallText(20090,315, "Stat Change 2", (255,255,255))
achievementsTile50Text4 = SmallText(20090,337, "", (255,255,255))
achievementsTile50Text5 = SmallText(20090,360, "Found: 3/12", (255,255,255))

achievementsTile51Text1 = SmallText(20210,270, "Upgrade 1", (255,255,255))
achievementsTile51Text2 = SmallText(20210,292, "Stat Change 1", (255,255,255))
achievementsTile51Text3 = SmallText(20210,315, "Stat Change 2", (255,255,255))
achievementsTile51Text4 = SmallText(20210,337, "", (255,255,255))
achievementsTile51Text5 = SmallText(20210,360, "Found: 3/12", (255,255,255))

achievementsTile52Text1 = SmallText(20330,270, "Upgrade 1", (255,255,255))
achievementsTile52Text2 = SmallText(20330,292, "Stat Change 1", (255,255,255))
achievementsTile52Text3 = SmallText(20330,315, "Stat Change 2", (255,255,255))
achievementsTile52Text4 = SmallText(20330,337, "Stat Change 3", (255,255,255))
achievementsTile52Text5 = SmallText(20330,360, "Found: 3/12", (255,255,255))

achievementsTile53Text1 = SmallText(20450,270, "Upgrade 1", (255,255,255))
achievementsTile53Text2 = SmallText(20450,292, "Stat Change 1", (255,255,255))
achievementsTile53Text3 = SmallText(20450,315, "", (255,255,255))
achievementsTile53Text4 = SmallText(20450,337, "", (255,255,255))
achievementsTile53Text5 = SmallText(20450,360, "Found: 3/12", (255,255,255))

achievementsTile54Text1 = SmallText(20570,270, "Upgrade 1", (255,255,255))
achievementsTile54Text2 = SmallText(20570,292, "Stat Change 1", (255,255,255))
achievementsTile54Text3 = SmallText(20570,315, "Stat Change 2", (255,255,255))
achievementsTile54Text4 = SmallText(20570,337, "", (255,255,255))
achievementsTile54Text5 = SmallText(20570,360, "Found: 3/12", (255,255,255))

achievementsTile55Text1 = SmallText(20690,270, "Upgrade 1", (255,255,255))
achievementsTile55Text2 = SmallText(20690,292, "Stat Change 1", (255,255,255))
achievementsTile55Text3 = SmallText(20690,315, "Stat Change 2", (255,255,255))
achievementsTile55Text4 = SmallText(20690,337, "", (255,255,255))
achievementsTile55Text5 = SmallText(20690,360, "Found: 3/12", (255,255,255))

achievementsTile56Text1 = SmallText(20810,270, "Upgrade 1", (255,255,255))
achievementsTile56Text2 = SmallText(20810,292, "Stat Change 1", (255,255,255))
achievementsTile56Text3 = SmallText(20810,315, "Stat Change 2", (255,255,255))
achievementsTile56Text4 = SmallText(20810,337, "", (255,255,255))
achievementsTile56Text5 = SmallText(20810,360, "Found: 3/12", (255,255,255))

achievementsTile57Text1 = SmallText(20090,390, "Upgrade 1", (255,255,255))
achievementsTile57Text2 = SmallText(20090,412, "Stat Change 1", (255,255,255))
achievementsTile57Text3 = SmallText(20090,435, "Stat Change 2", (255,255,255))
achievementsTile57Text4 = SmallText(20090,457, "", (255,255,255))
achievementsTile57Text5 = SmallText(20090,480, "Found: 3/12", (255,255,255))

achievementsTile58Text1 = SmallText(20210,390, "Upgrade 1", (255,255,255))
achievementsTile58Text2 = SmallText(20210,412, "Stat Change 1", (255,255,255))
achievementsTile58Text3 = SmallText(20210,435, "Stat Change 2", (255,255,255))
achievementsTile58Text4 = SmallText(20210,457, "Stat Change 3", (255,255,255))
achievementsTile58Text5 = SmallText(20210,480, "Found: 3/12", (255,255,255))

achievementsTile59Text1 = SmallText(20330,390, "Upgrade 1", (255,255,255))
achievementsTile59Text2 = SmallText(20330,412, "Stat Change 1", (255,255,255))
achievementsTile59Text3 = SmallText(20330,435, "Stat Change 2", (255,255,255))
achievementsTile59Text4 = SmallText(20330,457, "Stat Change 3", (255,255,255))
achievementsTile59Text5 = SmallText(20330,480, "Found: 3/12", (255,255,255))

achievementsTile60Text1 = SmallText(20450,390, "Upgrade 1", (255,255,255))
achievementsTile60Text2 = SmallText(20450,412, "Stat Change 1", (255,255,255))
achievementsTile60Text3 = SmallText(20450,435, "Stat Change 2", (255,255,255))
achievementsTile60Text4 = SmallText(20450,457, "Stat Change 3", (255,255,255))
achievementsTile60Text5 = SmallText(20450,480, "Found: 3/12", (255,255,255))

achievementsTile61Text1 = SmallText(20570,390, "Upgrade 1", (255,255,255))
achievementsTile61Text2 = SmallText(20570,412, "Stat Change 1", (255,255,255))
achievementsTile61Text3 = SmallText(20570,435, "Stat Change 2", (255,255,255))
achievementsTile61Text4 = SmallText(20570,457, "", (255,255,255))
achievementsTile61Text5 = SmallText(20570,480, "Found: 3/12", (255,255,255))

achievementsTile62Text1 = SmallText(20690,390, "Upgrade 1", (255,255,255))
achievementsTile62Text2 = SmallText(20690,412, "Stat Change 1", (255,255,255))
achievementsTile62Text3 = SmallText(20690,435, "Stat Change 2", (255,255,255))
achievementsTile62Text4 = SmallText(20690,457, "Stat Change 3", (255,255,255))
achievementsTile62Text5 = SmallText(20690,480, "Found: 3/12", (255,255,255))

achievementsTile63Text1 = SmallText(20810,390, "Upgrade 1", (255,255,255))
achievementsTile63Text2 = SmallText(20810,412, "Stat Change 1", (255,255,255))
achievementsTile63Text3 = SmallText(20810,435, "", (255,255,255))
achievementsTile63Text4 = SmallText(20810,457, "", (255,255,255))
achievementsTile63Text5 = SmallText(20810,480, "Found: 3/12", (255,255,255))

# Group Making and Appending =====================================================================================================

#Title Screen
titleScreenGroup = pygame.sprite.Group()
titleScreenButtonsGroup = pygame.sprite.Group() #I only need to check buttons for being clickable hence their separation

titleScreenGroup.add(titleScreenButton)
titleScreenGroup.add(gameTitleText)
titleScreenGroup.add(gameTitleButtonText)

titleScreenButtonsGroup.add(titleScreenButton)


#Save Select
saveSelectGroup = pygame.sprite.Group()

#saveSelectGroup.add(saveSelectCopyButton)
#saveSelectGroup.add(saveSelectDeleteButton)
saveSelectGroup.add(saveSelectConfirmButton)
saveSelectGroup.add(saveSelectFile1)
saveSelectGroup.add(saveSelectFile2)
saveSelectGroup.add(saveSelectFile3)
saveSelectGroup.add(saveSelectTitle)
saveSelectGroup.add(saveSelectFile1Text1)
saveSelectGroup.add(saveSelectFile1Text2)
saveSelectGroup.add(saveSelectFile2Text1)
saveSelectGroup.add(saveSelectFile2Text2)
saveSelectGroup.add(saveSelectFile3Text1)
saveSelectGroup.add(saveSelectFile3Text2)
saveSelectGroup.add(saveSelectTitleText)
saveSelectGroup.add(saveSelectConfirmButtonText)
#saveSelectGroup.add(saveSelectCopyButtonText)
#saveSelectGroup.add(saveSelectDeleteButtonText)

#Decision Window 
decisionWindowGroup = pygame.sprite.Group()

decisionWindowGroup.add(decisionWindow)
decisionWindowGroup.add(noButton)
decisionWindowGroup.add(yesButton)
decisionWindowGroup.add(noButtonText)
decisionWindowGroup.add(yesButtonText)


#Main Menu
mainMenuGroup = pygame.sprite.Group()
mainMenuButtonsGroup = pygame.sprite.Group()

mainMenuGroup.add(mainMenuTitle)
mainMenuGroup.add(mainMenuTitleText)
mainMenuGroup.add(mainMenuBackButton)
mainMenuGroup.add(mainMenuBackButtonText)
mainMenuGroup.add(mainMenuQuitButton)
mainMenuGroup.add(mainMenuQuitButtonText)
mainMenuGroup.add(mainMenuAdModeButton)
mainMenuGroup.add(mainMenuAdModeButtonText)
mainMenuGroup.add(mainMenuEndModeButton)
mainMenuGroup.add(mainMenuEndModeButtonText)
mainMenuGroup.add(mainMenuSettingsButton)
mainMenuGroup.add(mainMenuSettingsButtonText)

mainMenuButtonsGroup.add(mainMenuBackButton)
mainMenuButtonsGroup.add(mainMenuAdModeButton)
mainMenuButtonsGroup.add(mainMenuEndModeButton)
mainMenuButtonsGroup.add(mainMenuSettingsButton)

#Adventure Mode
adModeGroup = pygame.sprite.Group()
adModeButtonsGroup = pygame.sprite.Group()
adModeSlidingMenuGroup = pygame.sprite.Group()

adModeGroup.add(adModeTitle)
adModeGroup.add(adModeTitleText)
adModeGroup.add(adModeBackButton)
adModeGroup.add(adModeBackButtonText)
adModeGroup.add(adModeAchievementsButton) 
adModeGroup.add(adModeAchievementsButtonText1)
adModeGroup.add(adModeAchievementsButtonText2)
adModeGroup.add(adModeAchievementsButtonText3)
adModeGroup.add(adModeWeaponButton)
adModeGroup.add(adModeWeaponButtonText)

adModeGroup.add(adModeDungeon1Highlight)
adModeGroup.add(adModeDungeon2Highlight)
adModeGroup.add(adModeDungeon3Highlight)
adModeGroup.add(adModeDungeon4Highlight)
adModeGroup.add(adModeDungeon5Highlight)

adModeGroup.add(adModeDungeon1)
adModeGroup.add(adModeDungeon2)
adModeGroup.add(adModeDungeon3)
adModeGroup.add(adModeDungeon4)
adModeGroup.add(adModeDungeon5)

adModeGroup.add(adModeDungeon1Text1)
adModeGroup.add(adModeDungeon1Text2)
adModeGroup.add(adModeDungeon1Text3)

adModeGroup.add(adModeDungeon2Text1)
adModeGroup.add(adModeDungeon2Text2)
adModeGroup.add(adModeDungeon2Text3)

adModeGroup.add(adModeDungeon3Text1)
adModeGroup.add(adModeDungeon3Text2)
adModeGroup.add(adModeDungeon3Text3)

adModeGroup.add(adModeDungeon4Text1)
adModeGroup.add(adModeDungeon4Text2)
adModeGroup.add(adModeDungeon4Text3)

adModeGroup.add(adModeDungeon5Text1)
adModeGroup.add(adModeDungeon5Text2)
adModeGroup.add(adModeDungeon5Text3)


adModeButtonsGroup.add(adModeBackButton)
adModeButtonsGroup.add(adModeAchievementsButton)


adModeSlidingMenuGroup.add(adModeDungeon1Highlight)
adModeSlidingMenuGroup.add(adModeDungeon2Highlight)
adModeSlidingMenuGroup.add(adModeDungeon3Highlight)
adModeSlidingMenuGroup.add(adModeDungeon4Highlight)
adModeSlidingMenuGroup.add(adModeDungeon5Highlight)

adModeSlidingMenuGroup.add(adModeDungeon1)
adModeSlidingMenuGroup.add(adModeDungeon2)
adModeSlidingMenuGroup.add(adModeDungeon3)
adModeSlidingMenuGroup.add(adModeDungeon4)
adModeSlidingMenuGroup.add(adModeDungeon5)

adModeSlidingMenuGroup.add(adModeDungeon1Text1)
adModeSlidingMenuGroup.add(adModeDungeon1Text2)
adModeSlidingMenuGroup.add(adModeDungeon1Text3)

adModeSlidingMenuGroup.add(adModeDungeon2Text1)
adModeSlidingMenuGroup.add(adModeDungeon2Text2)
adModeSlidingMenuGroup.add(adModeDungeon2Text3)

adModeSlidingMenuGroup.add(adModeDungeon3Text1)
adModeSlidingMenuGroup.add(adModeDungeon3Text2)
adModeSlidingMenuGroup.add(adModeDungeon3Text3)

adModeSlidingMenuGroup.add(adModeDungeon4Text1)
adModeSlidingMenuGroup.add(adModeDungeon4Text2)
adModeSlidingMenuGroup.add(adModeDungeon4Text3)

adModeSlidingMenuGroup.add(adModeDungeon5Text1)
adModeSlidingMenuGroup.add(adModeDungeon5Text2)
adModeSlidingMenuGroup.add(adModeDungeon5Text3)


#Endless Mode
endModeGroup = pygame.sprite.Group()
endModeButtonsGroup = pygame.sprite.Group()

endModeGroup.add(endModeTitle)
endModeGroup.add(endModeTitleText)
endModeGroup.add(endModeHighScoreDisplay)
endModeGroup.add(endModeHighScoreDisplayText)
endModeGroup.add(endModeHighScoreDisplayValueText)
endModeGroup.add(endModeBackButton)
endModeGroup.add(endModeBackButtonText)
endModeGroup.add(endModePlayButton)
endModeGroup.add(endModePlayButtonText)
endModeGroup.add(endModeAchievementsButton)
endModeGroup.add(endModeAchievementsButtonText1)
endModeGroup.add(endModeAchievementsButtonText2)
endModeGroup.add(endModeAchievementsButtonText3)
endModeGroup.add(endModeWeaponButton)
endModeGroup.add(endModeWeaponButtonText)

endModeButtonsGroup.add(endModeBackButton)
endModeButtonsGroup.add(endModePlayButton)
endModeButtonsGroup.add(endModeAchievementsButton)
endModeButtonsGroup.add(endModeWeaponButton)

#Settings
settingsGroup = pygame.sprite.Group()
settingsButtonsGroup = pygame.sprite.Group()

settingsGroup.add(settingsBackButton)
settingsGroup.add(settingsBackButtonText)
settingsGroup.add(settingsSoundButton)
settingsGroup.add(settingsSoundButtonText)
settingsGroup.add(settingsGraphicsButton)
settingsGroup.add(settingsGraphicsButtonText)
settingsGroup.add(settingsControlsButton)
settingsGroup.add(settingsControlsButtonText)
settingsGroup.add(settingsSaveButton)
settingsGroup.add(settingsSaveButtonText)

settingsButtonsGroup.add(settingsBackButton)
settingsButtonsGroup.add(settingsControlsButton)
#settingsButtonsGroup.add(settingsSaveButton)

#Controls
controlsGroup = pygame.sprite.Group()
#controlsButtonsGroup = pygame.sprite.Group() Commented out due to only 1 use for it | may re-include, exists for modularity

controlsGroup.add(controlsBackButton)
controlsGroup.add(controlsBackButtonText)
controlsGroup.add(controlsAttackWindow)
controlsGroup.add(controlsAttackWindowText)
controlsGroup.add(controlsAttackButton)
controlsGroup.add(controlsAttackButtonText)
controlsGroup.add(controlsAction1Window)
controlsGroup.add(controlsAction1WindowText)
controlsGroup.add(controlsAction1Button)
controlsGroup.add(controlsAction1ButtonText)
controlsGroup.add(controlsAction2Window)
controlsGroup.add(controlsAction2WindowText)
controlsGroup.add(controlsAction2Button)
controlsGroup.add(controlsAction2ButtonText)
controlsGroup.add(controlsSaveButton)
controlsGroup.add(controlsSaveButtonText)

#controlsButtonsGroup.add(controlsBackButton)

#Gameplay Objects
gameplayCollisionsGroup = pygame.sprite.Group()
gameplayMovementGroup = pygame.sprite.Group()

gameplayCollisionsGroup.add(enemy1)
gameplayCollisionsGroup.add(enemy2)
gameplayCollisionsGroup.add(enemy3)
gameplayCollisionsGroup.add(enemy4)
gameplayCollisionsGroup.add(player)
#gameplayCollisionsGroup.add(playerShield) 
#gameplayCollisionsGroup.add(playerSword)

gameplayMovementGroup.add(enemy1)
gameplayMovementGroup.add(enemy2)
gameplayMovementGroup.add(enemy3)
gameplayMovementGroup.add(enemy4)
gameplayMovementGroup.add(player)

#Upgrade Select
upgradeSelectGroup = pygame.sprite.Group()
upgradeSelectGroup.add(upgradesStatsWindow)
upgradeSelectGroup.add(upgradesStatsWindowText)
upgradeSelectGroup.add(upgradesStatsWindowHealthText)
upgradeSelectGroup.add(upgradesStatsWindowHealthTextValue)
upgradeSelectGroup.add(upgradesStatsWindowDamageText)
upgradeSelectGroup.add(upgradesStatsWindowDamageTextValue)
upgradeSelectGroup.add(upgradesStatsWindowDSpeedText1)
upgradeSelectGroup.add(upgradesStatsWindowDSpeedText2)
upgradeSelectGroup.add(upgradesStatsWindowDSpeedTextValue)
upgradeSelectGroup.add(upgradesStatsWindowMSpeedText1)
upgradeSelectGroup.add(upgradesStatsWindowMSpeedText2)
upgradeSelectGroup.add(upgradesStatsWindowMSpeedTextValue)
upgradeSelectGroup.add(upgradesStatsWindowRangeText)
upgradeSelectGroup.add(upgradesStatsWindowRangeTextValue)


#upgradeSelectGroup.add(upgradesUpgradeWindow)
#upgradeSelectGroup.add(upgradesUpgradeWindowText1)
#upgradeSelectGroup.add(upgradesUpgradeWindowText2)
#upgradeSelectGroup.add(upgradesUpgradeWindowText3)
#upgradeSelectGroup.add(upgradesUpgradeWindowText4)
#upgradeSelectGroup.add(upgradesUpgradeWindowText5)
#upgradeSelectGroup.add(upgradesUpgradeWindowText6)
#upgradeSelectGroup.add(upgradesUpgradeWindowText7)
#upgradeSelectGroup.add(upgradesUpgradeWindowText8)
#upgradeSelectGroup.add(upgradesUpgradeWindowText9)
#upgradeSelectGroup.add(upgradesUpgradeWindowText10)
#upgradeSelectGroup.add(upgradesUpgradeWindowText11)


#upgradeSelectGroup.add(upgradesUpgradeListButton)
#upgradeSelectGroup.add(upgradesUpgradeListButtonText)
#upgradeSelectGroup.add(upgradesDungeonMapButton)
#upgradeSelectGroup.add(upgradesDungeonMapButtonText)

upgradeSelectGroup.add(upgradesFloorCountWindow)
upgradeSelectGroup.add(upgradesFloorCountWindowText)
upgradeSelectGroup.add(upgradesQuitButton)
upgradeSelectGroup.add(upgradesQuitButtonText)

upgradeSelectGroup.add(upgradesOption1Button)
upgradeSelectGroup.add(upgradesOption1ButtonText)
upgradeSelectGroup.add(upgradesOption1ButtonStat1)
upgradeSelectGroup.add(upgradesOption1ButtonStat2)
upgradeSelectGroup.add(upgradesOption1ButtonStat3)

upgradeSelectGroup.add(upgradesOption2Button)
upgradeSelectGroup.add(upgradesOption2ButtonText)
upgradeSelectGroup.add(upgradesOption2ButtonStat1)
upgradeSelectGroup.add(upgradesOption2ButtonStat2)
upgradeSelectGroup.add(upgradesOption2ButtonStat3)

upgradeSelectGroup.add(upgradesOption3Button)
upgradeSelectGroup.add(upgradesOption3ButtonText)
upgradeSelectGroup.add(upgradesOption3ButtonStat1)
upgradeSelectGroup.add(upgradesOption3ButtonStat2)
upgradeSelectGroup.add(upgradesOption3ButtonStat3)

upgradeSelectGroup.add(upgradesOption4Button)
upgradeSelectGroup.add(upgradesOption4ButtonText)
upgradeSelectGroup.add(upgradesOption4ButtonStat1)
upgradeSelectGroup.add(upgradesOption4ButtonStat2)
upgradeSelectGroup.add(upgradesOption4ButtonStat3)

#Achievements
achievementsGroup = pygame.sprite.Group()
achievementsGroup.add(achievementsTile1)
achievementsGroup.add(achievementsTile2)
achievementsGroup.add(achievementsTile3)
achievementsGroup.add(achievementsTile4)
achievementsGroup.add(achievementsTile5)
achievementsGroup.add(achievementsTile6)
achievementsGroup.add(achievementsTile7)
achievementsGroup.add(achievementsTile8)
achievementsGroup.add(achievementsTile9)
achievementsGroup.add(achievementsTile10)
achievementsGroup.add(achievementsTile11)
achievementsGroup.add(achievementsTile12)
achievementsGroup.add(achievementsTile13)
achievementsGroup.add(achievementsTile14)
achievementsGroup.add(achievementsTile15)
achievementsGroup.add(achievementsTile16)
achievementsGroup.add(achievementsTile17)
achievementsGroup.add(achievementsTile18)
achievementsGroup.add(achievementsTile19)
achievementsGroup.add(achievementsTile20)
achievementsGroup.add(achievementsTile21)
achievementsGroup.add(achievementsTile22)
achievementsGroup.add(achievementsTile23)
achievementsGroup.add(achievementsTile24)
achievementsGroup.add(achievementsTile25)
achievementsGroup.add(achievementsTile26)
achievementsGroup.add(achievementsTile27)
achievementsGroup.add(achievementsTile28)
achievementsGroup.add(achievementsTile29)
achievementsGroup.add(achievementsTile30)
achievementsGroup.add(achievementsTile31)
achievementsGroup.add(achievementsTile32)
achievementsGroup.add(achievementsTile33)
achievementsGroup.add(achievementsTile34)
achievementsGroup.add(achievementsTile35)
achievementsGroup.add(achievementsTile36)
achievementsGroup.add(achievementsTile37)
achievementsGroup.add(achievementsTile38)
achievementsGroup.add(achievementsTile39)
achievementsGroup.add(achievementsTile40)
achievementsGroup.add(achievementsTile41)
achievementsGroup.add(achievementsTile42)
achievementsGroup.add(achievementsTile43)
achievementsGroup.add(achievementsTile44)
achievementsGroup.add(achievementsTile45)
achievementsGroup.add(achievementsTile46)
achievementsGroup.add(achievementsTile47)
achievementsGroup.add(achievementsTile48)
achievementsGroup.add(achievementsTile49)
achievementsGroup.add(achievementsTile50)
achievementsGroup.add(achievementsTile51)
achievementsGroup.add(achievementsTile52)
achievementsGroup.add(achievementsTile53)
achievementsGroup.add(achievementsTile54)
achievementsGroup.add(achievementsTile55)
achievementsGroup.add(achievementsTile56)
achievementsGroup.add(achievementsTile57)
achievementsGroup.add(achievementsTile58)
achievementsGroup.add(achievementsTile59)
achievementsGroup.add(achievementsTile60)
achievementsGroup.add(achievementsTile61)
achievementsGroup.add(achievementsTile62)
achievementsGroup.add(achievementsTile63)

achievementsGroup.add(achievementsTile1Text1)
achievementsGroup.add(achievementsTile1Text2)
achievementsGroup.add(achievementsTile1Text3)
achievementsGroup.add(achievementsTile1Text4)
achievementsGroup.add(achievementsTile1Text5)

achievementsGroup.add(achievementsTile2Text1)
achievementsGroup.add(achievementsTile2Text2)
achievementsGroup.add(achievementsTile2Text3)
achievementsGroup.add(achievementsTile2Text4)
achievementsGroup.add(achievementsTile2Text5)

achievementsGroup.add(achievementsTile3Text1)
achievementsGroup.add(achievementsTile3Text2)
achievementsGroup.add(achievementsTile3Text3)
achievementsGroup.add(achievementsTile3Text4)
achievementsGroup.add(achievementsTile3Text5)

achievementsGroup.add(achievementsTile4Text1)
achievementsGroup.add(achievementsTile4Text2)
achievementsGroup.add(achievementsTile4Text3)
achievementsGroup.add(achievementsTile4Text4)
achievementsGroup.add(achievementsTile4Text5)

achievementsGroup.add(achievementsTile5Text1)
achievementsGroup.add(achievementsTile5Text2)
achievementsGroup.add(achievementsTile5Text3)
achievementsGroup.add(achievementsTile5Text4)
achievementsGroup.add(achievementsTile5Text5)

achievementsGroup.add(achievementsTile6Text1)
achievementsGroup.add(achievementsTile6Text2)
achievementsGroup.add(achievementsTile6Text3)
achievementsGroup.add(achievementsTile6Text4)
achievementsGroup.add(achievementsTile6Text5)

achievementsGroup.add(achievementsTile7Text1)
achievementsGroup.add(achievementsTile7Text2)
achievementsGroup.add(achievementsTile7Text3)
achievementsGroup.add(achievementsTile7Text4)
achievementsGroup.add(achievementsTile7Text5)

achievementsGroup.add(achievementsTile8Text1)
achievementsGroup.add(achievementsTile8Text2)
achievementsGroup.add(achievementsTile8Text3)
achievementsGroup.add(achievementsTile8Text4)
achievementsGroup.add(achievementsTile8Text5)

achievementsGroup.add(achievementsTile9Text1)
achievementsGroup.add(achievementsTile9Text2)
achievementsGroup.add(achievementsTile9Text3)
achievementsGroup.add(achievementsTile9Text4)
achievementsGroup.add(achievementsTile9Text5)

achievementsGroup.add(achievementsTile10Text1)
achievementsGroup.add(achievementsTile10Text2)
achievementsGroup.add(achievementsTile10Text3)
achievementsGroup.add(achievementsTile10Text4)
achievementsGroup.add(achievementsTile10Text5)

achievementsGroup.add(achievementsTile11Text1)
achievementsGroup.add(achievementsTile11Text2)
achievementsGroup.add(achievementsTile11Text3)
achievementsGroup.add(achievementsTile11Text4)
achievementsGroup.add(achievementsTile11Text5)

achievementsGroup.add(achievementsTile12Text1)
achievementsGroup.add(achievementsTile12Text2)
achievementsGroup.add(achievementsTile12Text3)
achievementsGroup.add(achievementsTile12Text4)
achievementsGroup.add(achievementsTile12Text5)

achievementsGroup.add(achievementsTile13Text1)
achievementsGroup.add(achievementsTile13Text2)
achievementsGroup.add(achievementsTile13Text3)
achievementsGroup.add(achievementsTile13Text4)
achievementsGroup.add(achievementsTile13Text5)

achievementsGroup.add(achievementsTile14Text1)
achievementsGroup.add(achievementsTile14Text2)
achievementsGroup.add(achievementsTile14Text3)
achievementsGroup.add(achievementsTile14Text4)
achievementsGroup.add(achievementsTile14Text5)

achievementsGroup.add(achievementsTile15Text1)
achievementsGroup.add(achievementsTile15Text2)
achievementsGroup.add(achievementsTile15Text3)
achievementsGroup.add(achievementsTile15Text4)
achievementsGroup.add(achievementsTile15Text5)

achievementsGroup.add(achievementsTile16Text1)
achievementsGroup.add(achievementsTile16Text2)
achievementsGroup.add(achievementsTile16Text3)
achievementsGroup.add(achievementsTile16Text4)
achievementsGroup.add(achievementsTile16Text5)

achievementsGroup.add(achievementsTile17Text1)
achievementsGroup.add(achievementsTile17Text2)
achievementsGroup.add(achievementsTile17Text3)
achievementsGroup.add(achievementsTile17Text4)
achievementsGroup.add(achievementsTile17Text5)

achievementsGroup.add(achievementsTile18Text1)
achievementsGroup.add(achievementsTile18Text2)
achievementsGroup.add(achievementsTile18Text3)
achievementsGroup.add(achievementsTile18Text4)
achievementsGroup.add(achievementsTile18Text5)

achievementsGroup.add(achievementsTile19Text1)
achievementsGroup.add(achievementsTile19Text2)
achievementsGroup.add(achievementsTile19Text3)
achievementsGroup.add(achievementsTile19Text4)
achievementsGroup.add(achievementsTile19Text5)

achievementsGroup.add(achievementsTile20Text1)
achievementsGroup.add(achievementsTile20Text2)
achievementsGroup.add(achievementsTile20Text3)
achievementsGroup.add(achievementsTile20Text4)
achievementsGroup.add(achievementsTile20Text5)

achievementsGroup.add(achievementsTile21Text1)
achievementsGroup.add(achievementsTile21Text2)
achievementsGroup.add(achievementsTile21Text3)
achievementsGroup.add(achievementsTile21Text4)
achievementsGroup.add(achievementsTile21Text5)

achievementsGroup.add(achievementsTile22Text1)
achievementsGroup.add(achievementsTile22Text2)
achievementsGroup.add(achievementsTile22Text3)
achievementsGroup.add(achievementsTile22Text4)
achievementsGroup.add(achievementsTile22Text5)

achievementsGroup.add(achievementsTile23Text1)
achievementsGroup.add(achievementsTile23Text2)
achievementsGroup.add(achievementsTile23Text3)
achievementsGroup.add(achievementsTile23Text4)
achievementsGroup.add(achievementsTile23Text5)

achievementsGroup.add(achievementsTile24Text1)
achievementsGroup.add(achievementsTile24Text2)
achievementsGroup.add(achievementsTile24Text3)
achievementsGroup.add(achievementsTile24Text4)
achievementsGroup.add(achievementsTile24Text5)

achievementsGroup.add(achievementsTile25Text1)
achievementsGroup.add(achievementsTile25Text2)
achievementsGroup.add(achievementsTile25Text3)
achievementsGroup.add(achievementsTile25Text4)
achievementsGroup.add(achievementsTile25Text5)

achievementsGroup.add(achievementsTile26Text1)
achievementsGroup.add(achievementsTile26Text2)
achievementsGroup.add(achievementsTile26Text3)
achievementsGroup.add(achievementsTile26Text4)
achievementsGroup.add(achievementsTile26Text5)

achievementsGroup.add(achievementsTile27Text1)
achievementsGroup.add(achievementsTile27Text2)
achievementsGroup.add(achievementsTile27Text3)
achievementsGroup.add(achievementsTile27Text4)
achievementsGroup.add(achievementsTile27Text5)

achievementsGroup.add(achievementsTile28Text1)
achievementsGroup.add(achievementsTile28Text2)
achievementsGroup.add(achievementsTile28Text3)
achievementsGroup.add(achievementsTile28Text4)
achievementsGroup.add(achievementsTile28Text5)

achievementsGroup.add(achievementsTile29Text1)
achievementsGroup.add(achievementsTile29Text2)
achievementsGroup.add(achievementsTile29Text3)
achievementsGroup.add(achievementsTile29Text4)
achievementsGroup.add(achievementsTile29Text5)

achievementsGroup.add(achievementsTile30Text1)
achievementsGroup.add(achievementsTile30Text2)
achievementsGroup.add(achievementsTile30Text3)
achievementsGroup.add(achievementsTile30Text4)
achievementsGroup.add(achievementsTile30Text5)

achievementsGroup.add(achievementsTile31Text1)
achievementsGroup.add(achievementsTile31Text2)
achievementsGroup.add(achievementsTile31Text3)
achievementsGroup.add(achievementsTile31Text4)
achievementsGroup.add(achievementsTile31Text5)

achievementsGroup.add(achievementsTile32Text1)
achievementsGroup.add(achievementsTile32Text2)
achievementsGroup.add(achievementsTile32Text3)
achievementsGroup.add(achievementsTile32Text4)
achievementsGroup.add(achievementsTile32Text5)

achievementsGroup.add(achievementsTile33Text1)
achievementsGroup.add(achievementsTile33Text2)
achievementsGroup.add(achievementsTile33Text3)
achievementsGroup.add(achievementsTile33Text4)
achievementsGroup.add(achievementsTile33Text5)

achievementsGroup.add(achievementsTile34Text1)
achievementsGroup.add(achievementsTile34Text2)
achievementsGroup.add(achievementsTile34Text3)
achievementsGroup.add(achievementsTile34Text4)
achievementsGroup.add(achievementsTile34Text5)

achievementsGroup.add(achievementsTile35Text1)
achievementsGroup.add(achievementsTile35Text2)
achievementsGroup.add(achievementsTile35Text3)
achievementsGroup.add(achievementsTile35Text4)
achievementsGroup.add(achievementsTile35Text5)

achievementsGroup.add(achievementsTile36Text1)
achievementsGroup.add(achievementsTile36Text2)
achievementsGroup.add(achievementsTile36Text3)
achievementsGroup.add(achievementsTile36Text4)
achievementsGroup.add(achievementsTile36Text5)

achievementsGroup.add(achievementsTile37Text1)
achievementsGroup.add(achievementsTile37Text2)
achievementsGroup.add(achievementsTile37Text3)
achievementsGroup.add(achievementsTile37Text4)
achievementsGroup.add(achievementsTile37Text5)

achievementsGroup.add(achievementsTile38Text1)
achievementsGroup.add(achievementsTile38Text2)
achievementsGroup.add(achievementsTile38Text3)
achievementsGroup.add(achievementsTile38Text4)
achievementsGroup.add(achievementsTile38Text5)

achievementsGroup.add(achievementsTile39Text1)
achievementsGroup.add(achievementsTile39Text2)
achievementsGroup.add(achievementsTile39Text3)
achievementsGroup.add(achievementsTile39Text4)
achievementsGroup.add(achievementsTile39Text5)

achievementsGroup.add(achievementsTile40Text1)
achievementsGroup.add(achievementsTile40Text2)
achievementsGroup.add(achievementsTile40Text3)
achievementsGroup.add(achievementsTile40Text4)
achievementsGroup.add(achievementsTile40Text5)

achievementsGroup.add(achievementsTile41Text1)
achievementsGroup.add(achievementsTile41Text2)
achievementsGroup.add(achievementsTile41Text3)
achievementsGroup.add(achievementsTile41Text4)
achievementsGroup.add(achievementsTile41Text5)

achievementsGroup.add(achievementsTile42Text1)
achievementsGroup.add(achievementsTile42Text2)
achievementsGroup.add(achievementsTile42Text3)
achievementsGroup.add(achievementsTile42Text4)
achievementsGroup.add(achievementsTile42Text5)

achievementsGroup.add(achievementsTile43Text1)
achievementsGroup.add(achievementsTile43Text2)
achievementsGroup.add(achievementsTile43Text3)
achievementsGroup.add(achievementsTile43Text4)
achievementsGroup.add(achievementsTile43Text5)

achievementsGroup.add(achievementsTile44Text1)
achievementsGroup.add(achievementsTile44Text2)
achievementsGroup.add(achievementsTile44Text3)
achievementsGroup.add(achievementsTile44Text4)
achievementsGroup.add(achievementsTile44Text5)

achievementsGroup.add(achievementsTile45Text1)
achievementsGroup.add(achievementsTile45Text2)
achievementsGroup.add(achievementsTile45Text3)
achievementsGroup.add(achievementsTile45Text4)
achievementsGroup.add(achievementsTile45Text5)

achievementsGroup.add(achievementsTile46Text1)
achievementsGroup.add(achievementsTile46Text2)
achievementsGroup.add(achievementsTile46Text3)
achievementsGroup.add(achievementsTile46Text4)
achievementsGroup.add(achievementsTile46Text5)

achievementsGroup.add(achievementsTile47Text1)
achievementsGroup.add(achievementsTile47Text2)
achievementsGroup.add(achievementsTile47Text3)
achievementsGroup.add(achievementsTile47Text4)
achievementsGroup.add(achievementsTile47Text5)

achievementsGroup.add(achievementsTile48Text1)
achievementsGroup.add(achievementsTile48Text2)
achievementsGroup.add(achievementsTile48Text3)
achievementsGroup.add(achievementsTile48Text4)
achievementsGroup.add(achievementsTile48Text5)

achievementsGroup.add(achievementsTile49Text1)
achievementsGroup.add(achievementsTile49Text2)
achievementsGroup.add(achievementsTile49Text3)
achievementsGroup.add(achievementsTile49Text4)
achievementsGroup.add(achievementsTile49Text5)

achievementsGroup.add(achievementsTile50Text1)
achievementsGroup.add(achievementsTile50Text2)
achievementsGroup.add(achievementsTile50Text3)
achievementsGroup.add(achievementsTile50Text4)
achievementsGroup.add(achievementsTile50Text5)

achievementsGroup.add(achievementsTile51Text1)
achievementsGroup.add(achievementsTile51Text2)
achievementsGroup.add(achievementsTile51Text3)
achievementsGroup.add(achievementsTile51Text4)
achievementsGroup.add(achievementsTile51Text5)

achievementsGroup.add(achievementsTile51Text1)
achievementsGroup.add(achievementsTile51Text2)
achievementsGroup.add(achievementsTile51Text3)
achievementsGroup.add(achievementsTile51Text4)
achievementsGroup.add(achievementsTile51Text5)

achievementsGroup.add(achievementsTile52Text1)
achievementsGroup.add(achievementsTile52Text2)
achievementsGroup.add(achievementsTile52Text3)
achievementsGroup.add(achievementsTile52Text4)
achievementsGroup.add(achievementsTile52Text5)

achievementsGroup.add(achievementsTile53Text1)
achievementsGroup.add(achievementsTile53Text2)
achievementsGroup.add(achievementsTile53Text3)
achievementsGroup.add(achievementsTile53Text4)
achievementsGroup.add(achievementsTile53Text5)

achievementsGroup.add(achievementsTile54Text1)
achievementsGroup.add(achievementsTile54Text2)
achievementsGroup.add(achievementsTile54Text3)
achievementsGroup.add(achievementsTile54Text4)
achievementsGroup.add(achievementsTile54Text5)

achievementsGroup.add(achievementsTile55Text1)
achievementsGroup.add(achievementsTile55Text2)
achievementsGroup.add(achievementsTile55Text3)
achievementsGroup.add(achievementsTile55Text4)
achievementsGroup.add(achievementsTile55Text5)

achievementsGroup.add(achievementsTile56Text1)
achievementsGroup.add(achievementsTile56Text2)
achievementsGroup.add(achievementsTile56Text3)
achievementsGroup.add(achievementsTile56Text4)
achievementsGroup.add(achievementsTile56Text5)

achievementsGroup.add(achievementsTile57Text1)
achievementsGroup.add(achievementsTile57Text2)
achievementsGroup.add(achievementsTile57Text3)
achievementsGroup.add(achievementsTile57Text4)
achievementsGroup.add(achievementsTile57Text5)

achievementsGroup.add(achievementsTile58Text1)
achievementsGroup.add(achievementsTile58Text2)
achievementsGroup.add(achievementsTile58Text3)
achievementsGroup.add(achievementsTile58Text4)
achievementsGroup.add(achievementsTile58Text5)

achievementsGroup.add(achievementsTile59Text1)
achievementsGroup.add(achievementsTile59Text2)
achievementsGroup.add(achievementsTile59Text3)
achievementsGroup.add(achievementsTile59Text4)
achievementsGroup.add(achievementsTile59Text5)

achievementsGroup.add(achievementsTile60Text1)
achievementsGroup.add(achievementsTile60Text2)
achievementsGroup.add(achievementsTile60Text3)
achievementsGroup.add(achievementsTile60Text4)
achievementsGroup.add(achievementsTile60Text5)

achievementsGroup.add(achievementsTile61Text1)
achievementsGroup.add(achievementsTile61Text2)
achievementsGroup.add(achievementsTile61Text3)
achievementsGroup.add(achievementsTile61Text4)
achievementsGroup.add(achievementsTile61Text5)

achievementsGroup.add(achievementsTile62Text1)
achievementsGroup.add(achievementsTile62Text2)
achievementsGroup.add(achievementsTile62Text3)
achievementsGroup.add(achievementsTile62Text4)
achievementsGroup.add(achievementsTile62Text5)

achievementsGroup.add(achievementsTile63Text1)
achievementsGroup.add(achievementsTile63Text2)
achievementsGroup.add(achievementsTile63Text3)
achievementsGroup.add(achievementsTile63Text4)
achievementsGroup.add(achievementsTile63Text5)


# Debug/Screen Initialisation
pygame.event.post(pygame.event.Event(TITLESCREEN))
currentMenu = "Title Screen"


        
# Game Loop =====================================================================================================================



while True:
    quitCheck()
    
    
    #Event Manager
 
    for event in pygame.event.get():
        #Quit Checks
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif showQuitMenu == True : 
            drawQuitMenu()
            
            if yesButton.clicked(event) :
                pygame.event.post(pygame.event.Event(QUIT))
                
            elif noButton.clicked(event) : #Brings you back to the screen you were on without the submenu showing now
        
                if currentMenu == "Title Screen" :
                    pygame.event.post(pygame.event.Event(TITLESCREEN))
                elif currentMenu == "Save Select" :
                    pygame.event.post(pygame.event.Event(SAVESELECT))
                elif currentMenu == "Main Menu" :
                    pygame.event.post(pygame.event.Event(MAINMENU))
                elif currentMenu == "Endless Mode Select" :
                    pygame.event.post(pygame.event.Event(ENDMODESELECT)) 
                elif currentMenu == "Adventure Mode Select" :            
                    pygame.event.post(pygame.event.Event(ADMODESELECT))  
                elif currentMenu == "Settings" :
                    pygame.event.post(pygame.event.Event(SETTINGS))
                elif currentMenu == "Controls" :
                    pygame.event.post(pygame.event.Event(CONTROLS))
                elif currentMenu == "Achievements" :
                    pygame.event.post(pygame.event.Event(ACHIEVEMENTS))
                elif currentMenu == "Gameplay" :
                    pygame.event.post(pygame.event.Event(GAMEPLAY))
                    
                showQuitMenu = False


        
       #Menu Event Checks     
        elif event.type == TITLESCREEN :
            currentMenu = "Title Screen"
            displaySurface.fill((255,255,255))
            for entity in titleScreenGroup :
                displaySurface.blit(entity.surf, entity.rect)
            
            
        elif event.type == SAVESELECT :
            currentMenu = "Save Select"
            displaySurface.fill((255,255,255))
            
            if saveFileSelectedButton == "File 1":
                displaySurface.blit(saveSelectFile1Highlight.surf, saveSelectFile1Highlight.rect)
            if saveFileSelectedButton == "File 2":
                displaySurface.blit(saveSelectFile2Highlight.surf, saveSelectFile2Highlight.rect)
            if saveFileSelectedButton == "File 3":
                displaySurface.blit(saveSelectFile3Highlight.surf, saveSelectFile3Highlight.rect)
                
            for entity in saveSelectGroup:
                displaySurface.blit(entity.surf, entity.rect)
                
         
        elif event.type == MAINMENU :
            currentMenu = "Main Menu"
            displaySurface.fill((255,255,255))
            for entity in mainMenuGroup:
                displaySurface.blit(entity.surf, entity.rect)
                
                
        elif event.type == ADMODESELECT :
            currentMenu = "Adventure Mode Select"
            displaySurface.fill((255,255,255))
            if adModeDungeon1Text2.text == "Complete!" and adModeDungeon1Text2.colour != (0,255,0) :
                adModeDungeon1Highlight.colour = (0,255,0)
                adModeDungeon1Highlight.surf.fill((0,255,0))
            elif adModeDungeon1Text2.text == "In Progress..." and adModeDungeon1Text2.colour != (255,255,0) :
                adModeDungeon1Highlight.colour = (255,255,0)
                adModeDungeon1Highlight.surf.fill((255,255,0))    
            elif adModeDungeon1Text2.text == "Not Complete" and adModeDungeon1Text2.colour != (255,0,0) :
                adModeDungeon1Highlight.colour = (255,0,0)
                adModeDungeon1Highlight.surf.fill((255,0,0))
                
            if adModeDungeon2Text2.text == "Complete!" and adModeDungeon2Text2.colour != (0,255,0) :
                adModeDungeon2Highlight.colour = (0,255,0)
                adModeDungeon2Highlight.surf.fill((0,255,0))
            elif adModeDungeon2Text2.text == "In Progress..." and adModeDungeon2Text2.colour != (255,255,0) :
                adModeDungeon2Highlight.colour = (255,255,0)
                adModeDungeon2Highlight.surf.fill((255,255,0))    
            elif adModeDungeon2Text2.text == "Not Complete" and adModeDungeon2Text2.colour != (255,0,0) :
                adModeDungeon2Highlight.colour = (255,0,0)
                adModeDungeon2Highlight.surf.fill((255,0,0))
                
            if adModeDungeon3Text2.text == "Complete!" and adModeDungeon3Text2.colour != (0,255,0) :
                adModeDungeon3Highlight.colour = (0,255,0)
                adModeDungeon3Highlight.surf.fill((0,255,0))
            elif adModeDungeon3Text2.text == "In Progress..." and adModeDungeon3Text2.colour != (255,255,0) :
                adModeDungeon3Highlight.colour = (255,255,0)
                adModeDungeon3Highlight.surf.fill((255,255,0))    
            elif adModeDungeon3Text2.text == "Not Complete" and adModeDungeon3Text2.colour != (255,0,0) :
                adModeDungeon3Highlight.colour = (255,0,0)
                adModeDungeon3Highlight.surf.fill((255,0,0))    
                
            if adModeDungeon4Text2.text == "Complete!" and adModeDungeon4Text2.colour != (0,255,0) :
                adModeDungeon4Highlight.colour = (0,255,0)
                adModeDungeon4Highlight.surf.fill((0,255,0))
            elif adModeDungeon4Text2.text == "In Progress..." and adModeDungeon4Text2.colour != (255,255,0) :
                adModeDungeon4Highlight.colour = (255,255,0)
                adModeDungeon4Highlight.surf.fill((255,255,0))    
            elif adModeDungeon4Text2.text == "Not Complete" and adModeDungeon4Text2.colour != (255,0,0) :
                adModeDungeon4Highlight.colour = (255,0,0)
                adModeDungeon4Highlight.surf.fill((255,0,0))
                
            if adModeDungeon5Text2.text == "Complete!" and adModeDungeon5Text2.colour != (0,255,0) :
                adModeDungeon5Highlight.colour = (0,255,0)
                adModeDungeon5Highlight.surf.fill((0,255,0))
            elif adModeDungeon5Text2.text == "In Progress..." and adModeDungeon5Text2.colour != (255,255,0) :
                adModeDungeon5Highlight.colour = (255,255,0)
                adModeDungeon5Highlight.surf.fill((255,255,0))    
            elif adModeDungeon5Text2.text == "Not Complete" and adModeDungeon5Text2.colour != (255,0,0) :
                adModeDungeon5Highlight.colour = (255,0,0)
                adModeDungeon5Highlight.surf.fill((255,0,0))    
            
            for entity in adModeGroup:
                displaySurface.blit(entity.surf, entity.rect)
            if adModeDungeon1.rect.x == 52 :
                pygame.draw.polygon(displaySurface, (100,100,100), [[40,350],[40,450],[10,400]])
                pygame.draw.polygon(displaySurface, (0,201,0), [[860,350],[860,450],[890,400]])
            elif adModeDungeon5.rect.x == 727 :
                pygame.draw.polygon(displaySurface, (0,200,0), [[40,350],[40,450],[10,400]])
                pygame.draw.polygon(displaySurface, (100,100,100), [[860,350],[860,450],[890,400]])
            else:
                pygame.draw.polygon(displaySurface, (0,200,0), [[40,350],[40,450],[10,400]])
                pygame.draw.polygon(displaySurface, (0,201,0), [[860,350],[860,450],[890,400]])
                
                
        elif event.type == ENDMODESELECT :
            currentMenu = "Endless Mode Select"
            displaySurface.fill((255,255,255))
            for entity in endModeGroup :
                displaySurface.blit(entity.surf, entity.rect)
                
        elif event.type == SETTINGS :
            currentMenu = "Settings"
            displaySurface.fill((255,255,255))
            for entity in settingsGroup :
                displaySurface.blit(entity.surf, entity.rect)
                
        elif event.type == CONTROLS :
            currentMenu = "Controls"
            displaySurface.fill((255,255,255))
            if controlsSelectedButton == "Attack":
                displaySurface.blit(controlsAttackButtonHighlight.surf, controlsAttackButtonHighlight.rect)
            elif controlsSelectedButton == "Action 1":
                displaySurface.blit(controlsAction1ButtonHighlight.surf, controlsAction1ButtonHighlight.rect)
            elif controlsSelectedButton == "Action 2":
                displaySurface.blit(controlsAction2ButtonHighlight.surf, controlsAction2ButtonHighlight.rect)
            for entity in controlsGroup :
                displaySurface.blit(entity.surf, entity.rect) 
                
        elif event.type == ACHIEVEMENTS :
            displaySurface.fill((255,255,255))
            if currentMenu == "Adventure Mode Select" :
                displaySurface.blit(achievementsBackButtonAdMode.surf, achievementsBackButtonAdMode.rect)
                displaySurface.blit(achievementsBackButtonAdModeText1.surf, achievementsBackButtonAdModeText1.rect)
                displaySurface.blit(achievementsBackButtonAdModeText2.surf, achievementsBackButtonAdModeText2.rect)
                previousMenu = currentMenu
            elif currentMenu == "Endless Mode Select"  :
                displaySurface.blit(achievementsBackButtonEndMode.surf, achievementsBackButtonEndMode.rect)
                displaySurface.blit(achievementsBackButtonEndModeText1.surf, achievementsBackButtonEndModeText1.rect)
                displaySurface.blit(achievementsBackButtonEndModeText2.surf, achievementsBackButtonEndModeText2.rect)
                previousMenu = currentMenu
            elif previousMenu == "Adventure Mode Select":
                displaySurface.blit(achievementsBackButtonAdMode.surf, achievementsBackButtonAdMode.rect)
                displaySurface.blit(achievementsBackButtonAdModeText1.surf, achievementsBackButtonAdModeText1.rect)
                displaySurface.blit(achievementsBackButtonAdModeText2.surf, achievementsBackButtonAdModeText2.rect)
            elif previousMenu == "Endless Mode Select":
                displaySurface.blit(achievementsBackButtonEndMode.surf, achievementsBackButtonEndMode.rect)
                displaySurface.blit(achievementsBackButtonEndModeText1.surf, achievementsBackButtonEndModeText1.rect)
                displaySurface.blit(achievementsBackButtonEndModeText2.surf, achievementsBackButtonEndModeText2.rect)

            currentMenu = "Achievements"
            for entity in achievementsGroup :
                displaySurface.blit(entity.surf, entity.rect)
                
            if achievementsTile1.rect.x == 30 :
                pygame.draw.polygon(displaySurface, (100,100,100), [[25,265],[25,365],[1,315]])
                pygame.draw.polygon(displaySurface, (0,201,0), [[875,265],[875,365],[899,315]])
            elif achievementsTile43.rect.x == 30 :
                pygame.draw.polygon(displaySurface, (0,200,0), [[25,265],[25,365],[1,315]])
                pygame.draw.polygon(displaySurface, (100,100,100), [[875,265],[875,365],[899,315]])
            else:
                pygame.draw.polygon(displaySurface, (0,200,0), [[25,265],[25,365],[1,315]])
                pygame.draw.polygon(displaySurface, (0,201,0), [[875,265],[875,365],[899,315]])
                
        elif event.type == GAMEPLAY :
            displaySurface.fill((255,255,255))
            currentMenu = "Gameplay"
            
            
        elif event.type == UPGRADES :
            displaySurface.fill((255,255,255))
            if gameMode == "adMode":
                if dungeon1Upgrades == [""] and dungeon2Upgrades == [""] and dungeon3Upgrades == [""] and dungeon4Upgrades == [""] and dungeon5Upgrades == [""] :
                    for i in range(startingFloor[currentDungeon-1],endingFloor[currentDungeon-1],1):
                        if floorReward[i] == 0: #Common
                            randomUpgrade1 = random.randint(0,4)
                            randomUpgrade2 = random.randint(0,4)
                            randomUpgrade3 = random.randint(0,4)
                            randomUpgrade4 = random.randint(0,4)
                        elif floorReward[i] == 1: #Uncommon
                            randomUpgrade1 = random.randint(0,9)
                            randomUpgrade2 = random.randint(0,9)
                            randomUpgrade3 = random.randint(0,9)
                            randomUpgrade4 = random.randint(0,9)
                        elif floorReward[i] == 2: #Rare
                            randomUpgrade1 = random.randint(0,7)
                            randomUpgrade2 = random.randint(0,7) 
                            randomUpgrade3 = random.randint(0,7)
                            randomUpgrade4 = random.randint(0,7)
                        elif floorReward[i] == 3: #Ability
                            randomUpgrade1 = random.randint(1,4)
                            randomUpgrade2 = random.randint(1,4)
                            randomUpgrade3 = random.randint(1,4)
                            randomUpgrade4 = random.randint(1,4)
                        while (randomUpgrade1 == randomUpgrade2) or (randomUpgrade1 == randomUpgrade3) or (randomUpgrade1 == randomUpgrade4) or (randomUpgrade2 == randomUpgrade3) or (randomUpgrade2 == randomUpgrade4) or (randomUpgrade3 == randomUpgrade4) :
                            if floorReward[i] == 0: #Common
                                randomUpgrade1 = random.randint(0,4)
                                randomUpgrade2 = random.randint(0,4)
                                randomUpgrade3 = random.randint(0,4)
                                randomUpgrade4 = random.randint(0,4)
                            elif floorReward[i] == 1: #Uncommon
                                randomUpgrade1 = random.randint(0,9)
                                randomUpgrade2 = random.randint(0,9)
                                randomUpgrade3 = random.randint(0,9)
                                randomUpgrade4 = random.randint(0,9)
                            elif floorReward[i] == 2: #Rare
                                randomUpgrade1 = random.randint(0,7)
                                randomUpgrade2 = random.randint(0,7) 
                                randomUpgrade3 = random.randint(0,7)
                                randomUpgrade4 = random.randint(0,7)
                            elif floorReward[i] == 3: #Ability
                                randomUpgrade1 = random.randint(1,4)
                                randomUpgrade2 = random.randint(1,4)
                                randomUpgrade3 = random.randint(1,4)
                                randomUpgrade4 = random.randint(1,4)
                        if currentDungeon == 1 :
                            if dungeon1Upgrades == [""] :
                                dungeon1Upgrades = []
                            dungeon1Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade1])
                            dungeon1Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade2])
                            dungeon1Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade3])
                            dungeon1Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade4])
                        elif currentDungeon == 2 :
                            if dungeon2Upgrades == [""] :
                                dungeon2Upgrades = []
                            dungeon2Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade1])
                            dungeon2Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade2])
                            dungeon2Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade3])
                            dungeon2Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade4])
                        elif currentDungeon == 3 :
                            if dungeon3Upgrades == [""] :
                                dungeon3Upgrades = []
                            dungeon3Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade1])
                            dungeon3Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade2])
                            dungeon3Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade3])
                            dungeon3Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade4])
                        elif currentDungeon == 4 :
                            if dungeon4Upgrades == [""] :
                                dungeon4Upgrades = []
                            dungeon4Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade1])
                            dungeon4Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade2])
                            dungeon4Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade3])
                            dungeon4Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade4])
                        elif currentDungeon == 5 :
                            if dungeon5Upgrades == [""] :
                                dungeon5Upgrades = []
                            dungeon5Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade1])
                            dungeon5Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade2])
                            dungeon5Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade3])
                            dungeon5Upgrades.append(masterUpgradeList[floorReward[i]][randomUpgrade4])
                            
                upgradesFloorCountWindowText.text = "Floor: " + str(currentFloor+1 + (loopsOfEndless *70))
                upgradesFloorCountWindowText.surf = pygame.Surface((smallFont.size(upgradesFloorCountWindowText.text)[0],smallFont.size(upgradesFloorCountWindowText.text)[1]))
                upgradesFloorCountWindowText.rect = upgradesFloorCountWindowText.surf.get_rect(center = (upgradesFloorCountWindowText.pos[0], upgradesFloorCountWindowText.pos[1]))
                upgradesFloorCountWindowText.surf = smallFont.render(upgradesFloorCountWindowText.text, True, upgradesFloorCountWindowText.colour)
                
                upgradesStatsWindowHealthTextValue.text = str(player.maxHealth)
                upgradesStatsWindowHealthTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowHealthTextValue.text)[0],smallFont.size(upgradesStatsWindowHealthTextValue.text)[1]))
                upgradesStatsWindowHealthTextValue.rect = upgradesStatsWindowHealthTextValue.surf.get_rect(center = (upgradesStatsWindowHealthTextValue.pos[0], upgradesStatsWindowHealthTextValue.pos[1]))
                upgradesStatsWindowHealthTextValue.surf = smallFont.render(upgradesStatsWindowHealthTextValue.text, True, upgradesStatsWindowHealthTextValue.colour)
                
                upgradesStatsWindowDamageTextValue.text = str(player.damage)
                upgradesStatsWindowDamageTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowDamageTextValue.text)[0],smallFont.size(upgradesStatsWindowDamageTextValue.text)[1]))
                upgradesStatsWindowDamageTextValue.rect = upgradesStatsWindowDamageTextValue.surf.get_rect(center = (upgradesStatsWindowDamageTextValue.pos[0], upgradesStatsWindowDamageTextValue.pos[1]))
                upgradesStatsWindowDamageTextValue.surf = smallFont.render(upgradesStatsWindowDamageTextValue.text, True, upgradesStatsWindowDamageTextValue.colour)
                
                if player.Dspeed // 100 >= 1 : #Handles 100% or greater
                    upgradesStatsWindowDSpeedTextValue.text = "X" + str(player.Dspeed)[0] + "." + str(player.Dspeed)[1:]
                else:                              #Handles 99% or less
                    upgradesStatsWindowDSpeedTextValue.text = "X" + "0" + "." + str(player.Dspeed)[0:]
                upgradesStatsWindowDSpeedTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowDSpeedTextValue.text)[0],smallFont.size(upgradesStatsWindowDSpeedTextValue.text)[1]))
                upgradesStatsWindowDSpeedTextValue.rect = upgradesStatsWindowDSpeedTextValue.surf.get_rect(center = (upgradesStatsWindowDSpeedTextValue.pos[0], upgradesStatsWindowDSpeedTextValue.pos[1]))
                upgradesStatsWindowDSpeedTextValue.surf = smallFont.render(upgradesStatsWindowDSpeedTextValue.text, True, upgradesStatsWindowDSpeedTextValue.colour)
                
                if player.Mspeed // 100 >= 1 : 
                    upgradesStatsWindowMSpeedTextValue.text = "X" + str(player.Mspeed)[0] + "." + str(player.Mspeed)[1:]
                else:                              
                    upgradesStatsWindowMSpeedTextValue.text = "X" + "0" + "." + str(player.Mspeed)[0:]
                upgradesStatsWindowMSpeedTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowMSpeedTextValue.text)[0],smallFont.size(upgradesStatsWindowMSpeedTextValue.text)[1]))
                upgradesStatsWindowMSpeedTextValue.rect = upgradesStatsWindowMSpeedTextValue.surf.get_rect(center = (upgradesStatsWindowMSpeedTextValue.pos[0], upgradesStatsWindowMSpeedTextValue.pos[1]))
                upgradesStatsWindowMSpeedTextValue.surf = smallFont.render(upgradesStatsWindowMSpeedTextValue.text, True, upgradesStatsWindowMSpeedTextValue.colour)

                if player.range // 100 >= 1 : 
                    upgradesStatsWindowRangeTextValue.text = "X" + str(player.range)[0] + "." + str(player.range)[1:]
                else:                              
                    upgradesStatsWindowRangeTextValue.text = "X" + "0" + "." + str(player.range)[0:]
                upgradesStatsWindowRangeTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowRangeTextValue.text)[0],smallFont.size(upgradesStatsWindowRangeTextValue.text)[1]))
                upgradesStatsWindowRangeTextValue.rect = upgradesStatsWindowRangeTextValue.surf.get_rect(center = (upgradesStatsWindowRangeTextValue.pos[0], upgradesStatsWindowRangeTextValue.pos[1]))
                upgradesStatsWindowRangeTextValue.surf = smallFont.render(upgradesStatsWindowRangeTextValue.text, True, upgradesStatsWindowRangeTextValue.colour)
                    
               
                if dungeon1Upgrades[0] == "Sharpen" or dungeon2Upgrades[0] == "Sharpen" or dungeon3Upgrades[0] == "Sharpen" or dungeon4Upgrades[0] == "Sharpen" or dungeon5Upgrades[0] == "Sharpen":
                    upgradesOption1ButtonText.text = "Sharpen"
                    upgradesOption1ButtonStat1.text = "+1 Damage"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Resist" or dungeon2Upgrades[0] == "Resist" or dungeon3Upgrades[0] == "Resist" or dungeon4Upgrades[0] == "Resist" or dungeon5Upgrades[0] == "Resist":
                    upgradesOption1ButtonText.text = "Resist"
                    upgradesOption1ButtonStat1.text = "+1 Max Health"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fast" or dungeon2Upgrades[0] == "Fast" or dungeon3Upgrades[0] == "Fast" or dungeon4Upgrades[0] == "Fast" or dungeon5Upgrades[0] == "Fast":
                    upgradesOption1ButtonText.text = "Fast"
                    upgradesOption1ButtonStat1.text = "+10% Velocity"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dextrous" or dungeon2Upgrades[0] == "Dextrous" or dungeon3Upgrades[0] == "Dextrous" or dungeon4Upgrades[0] == "Dextrous" or dungeon5Upgrades[0] == "Dextrous":
                    upgradesOption1ButtonText.text = "Dextrous"
                    upgradesOption1ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Extend" or dungeon2Upgrades[0] == "Extend" or dungeon3Upgrades[0] == "Extend" or dungeon4Upgrades[0] == "Extend" or dungeon5Upgrades[0] == "Extend":
                    upgradesOption1ButtonText.text = "Extend"
                    upgradesOption1ButtonStat1.text = "+10% Range"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Honed" or dungeon2Upgrades[0] == "Honed" or dungeon3Upgrades[0] == "Honed" or dungeon4Upgrades[0] == "Honed" or dungeon5Upgrades[0] == "Honed":
                    upgradesOption1ButtonText.text = "Honed"
                    upgradesOption1ButtonStat1.text = "+1 Damage"
                    upgradesOption1ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Deft" or dungeon2Upgrades[0] == "Deft" or dungeon3Upgrades[0] == "Deft" or dungeon4Upgrades[0] == "Deft" or dungeon5Upgrades[0] == "Deft":
                    upgradesOption1ButtonText.text = "Deft"
                    upgradesOption1ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Broaden" or dungeon2Upgrades[0] == "Broaden" or dungeon3Upgrades[0] == "Broaden" or dungeon4Upgrades[0] == "Broaden" or dungeon5Upgrades[0] == "Broaden":
                    upgradesOption1ButtonText.text = "Broaden"
                    upgradesOption1ButtonStat1.text = "+1 Max Health"
                    upgradesOption1ButtonStat2.text = "+10% Range"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Boost" or dungeon2Upgrades[0] == "Boost" or dungeon3Upgrades[0] == "Boost" or dungeon4Upgrades[0] == "Boost" or dungeon5Upgrades[0] == "Boost":
                    upgradesOption1ButtonText.text = "Boost"
                    upgradesOption1ButtonStat1.text = "+1 Max Health"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Blacksmith" or dungeon2Upgrades[0] == "Blacksmith" or dungeon3Upgrades[0] == "Blacksmith" or dungeon4Upgrades[0] == "Blacksmith" or dungeon5Upgrades[0] == "Blacksmith":
                    upgradesOption1ButtonText.text = "Blacksmith"
                    upgradesOption1ButtonStat1.text = "+1 Damage"
                    upgradesOption1ButtonStat2.text = "+10% Range"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Stoic" or dungeon2Upgrades[0] == "Stoic" or dungeon3Upgrades[0] == "Stoic" or dungeon4Upgrades[0] == "Stoic" or dungeon5Upgrades[0] == "Stoic":
                    upgradesOption1ButtonText.text = "Stoic"
                    upgradesOption1ButtonStat1.text = "+2 Max Health"
                    upgradesOption1ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Temper" or dungeon2Upgrades[0] == "Temper" or dungeon3Upgrades[0] == "Temper" or dungeon4Upgrades[0] == "Temper" or dungeon5Upgrades[0] == "Temper":
                    upgradesOption1ButtonText.text = "Temper"
                    upgradesOption1ButtonStat1.text = "+2 Damage"
                    upgradesOption1ButtonStat2.text = "-1 Max Health"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Inflate" or dungeon2Upgrades[0] == "Inflate" or dungeon3Upgrades[0] == "Inflate" or dungeon4Upgrades[0] == "Inflate" or dungeon5Upgrades[0] == "Inflate":
                    upgradesOption1ButtonText.text = "Inflate"
                    upgradesOption1ButtonStat1.text = "+20% Range"
                    upgradesOption1ButtonStat2.text = "-10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Exercise" or dungeon2Upgrades[0] == "Exercise" or dungeon3Upgrades[0] == "Exercise" or dungeon4Upgrades[0] == "Exercise" or dungeon5Upgrades[0] == "Exercise":
                    upgradesOption1ButtonText.text = "Exercise"
                    upgradesOption1ButtonStat1.text = "+20% Velocity"
                    upgradesOption1ButtonStat2.text = "-10% Range"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Unruly" or dungeon2Upgrades[0] == "Unruly" or dungeon3Upgrades[0] == "Unruly" or dungeon4Upgrades[0] == "Unruly" or dungeon5Upgrades[0] == "Unruly":
                    upgradesOption1ButtonText.text = "Unruly"
                    upgradesOption1ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption1ButtonStat2.text = "-1 Damage"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Toughen" or dungeon2Upgrades[0] == "Toughen" or dungeon3Upgrades[0] == "Toughen" or dungeon4Upgrades[0] == "Toughen" or dungeon5Upgrades[0] == "Toughen":
                    upgradesOption1ButtonText.text = "Toughen"
                    upgradesOption1ButtonStat1.text = "+2 Max Health"
                    upgradesOption1ButtonStat2.text = "+1 Damage"
                    upgradesOption1ButtonStat3.text = "-10% Velocity"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Speedier" or dungeon2Upgrades[0] == "Speedier" or dungeon3Upgrades[0] == "Speedier" or dungeon4Upgrades[0] == "Speedier" or dungeon5Upgrades[0] == "Speedier":
                    upgradesOption1ButtonText.text = "Speedier"
                    upgradesOption1ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = "-10% Range"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Embiggen" or dungeon2Upgrades[0] == "Embiggen" or dungeon3Upgrades[0] == "Embiggen" or dungeon4Upgrades[0] == "Embiggen" or dungeon5Upgrades[0] == "Embiggen":
                    upgradesOption1ButtonText.text = "Embiggen"
                    upgradesOption1ButtonStat1.text = "+20% Range"
                    upgradesOption1ButtonStat2.text = "+1 Max Health"
                    upgradesOption1ButtonStat3.text = "-1 Damage"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Smite" or dungeon2Upgrades[0] == "Smite" or dungeon3Upgrades[0] == "Smite" or dungeon4Upgrades[0] == "Smite" or dungeon5Upgrades[0] == "Smite":
                    upgradesOption1ButtonText.text = "Smite"
                    upgradesOption1ButtonStat1.text = "+3 Damage"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fortify" or dungeon2Upgrades[0] == "Fortify" or dungeon3Upgrades[0] == "Fortify" or dungeon4Upgrades[0] == "Fortify" or dungeon5Upgrades[0] == "Fortify":
                    upgradesOption1ButtonText.text = "Fortify"
                    upgradesOption1ButtonStat1.text = "+3 Max Health"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rush" or dungeon2Upgrades[0] == "Rush" or dungeon3Upgrades[0] == "Rush" or dungeon4Upgrades[0] == "Rush" or dungeon5Upgrades[0] == "Rush":
                    upgradesOption1ButtonText.text = "Rush"
                    upgradesOption1ButtonStat1.text = "+30% Velocity"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Lash" or dungeon2Upgrades[0] == "Lash" or dungeon3Upgrades[0] == "Lash" or dungeon4Upgrades[0] == "Lash" or dungeon5Upgrades[0] == "Lash":
                    upgradesOption1ButtonText.text = "Lash"
                    upgradesOption1ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Bolster" or dungeon2Upgrades[0] == "Bolster" or dungeon3Upgrades[0] == "Bolster" or dungeon4Upgrades[0] == "Bolster" or dungeon5Upgrades[0] == "Bolster":
                    upgradesOption1ButtonText.text = "Bolster"
                    upgradesOption1ButtonStat1.text = "+30% Range"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dash" or dungeon2Upgrades[0] == "Dash" or dungeon3Upgrades[0] == "Dash" or dungeon4Upgrades[0] == "Dash" or dungeon5Upgrades[0] == "Dash":
                    upgradesOption1ButtonText.text = "Dash"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Saviour" or dungeon2Upgrades[0] == "Saviour" or dungeon3Upgrades[0] == "Saviour" or dungeon4Upgrades[0] == "Saviour" or dungeon5Upgrades[0] == "Saviour":
                    upgradesOption1ButtonText.text = "Saviour"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+2 Max Health"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rampage" or dungeon2Upgrades[0] == "Rampage" or dungeon3Upgrades[0] == "Rampage" or dungeon4Upgrades[0] == "Rampage" or dungeon5Upgrades[0] == "Rampage":
                    upgradesOption1ButtonText.text = "Rampage"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+1 Damage"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Burst" or dungeon2Upgrades[0] == "Burst" or dungeon3Upgrades[0] == "Burst" or dungeon4Upgrades[0] == "Burst" or dungeon5Upgrades[0] == "Burst":
                    upgradesOption1ButtonText.text = "Burst"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Pulse" or dungeon2Upgrades[0] == "Pulse" or dungeon3Upgrades[0] == "Pulse" or dungeon4Upgrades[0] == "Pulse" or dungeon5Upgrades[0] == "Pulse":
                    upgradesOption1ButtonText.text = "Pulse"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+10% Range"
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Super" or dungeon2Upgrades[0] == "Super" or dungeon3Upgrades[0] == "Super" or dungeon4Upgrades[0] == "Super" or dungeon5Upgrades[0] == "Super":
                    upgradesOption1ButtonText.text = "Super"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                        
                upgradesOption1ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonText.text)[0],smallFont.size(upgradesOption1ButtonText.text)[1]))
                upgradesOption1ButtonText.rect = upgradesOption1ButtonText.surf.get_rect(center = (upgradesOption1ButtonText.pos[0], upgradesOption1ButtonText.pos[1]))
                upgradesOption1ButtonText.surf = smallFont.render(upgradesOption1ButtonText.text, True, upgradesOption1ButtonText.colour)
                    
                upgradesOption1ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonStat1.text)[0],smallFont.size(upgradesOption1ButtonStat1.text)[1]))
                upgradesOption1ButtonStat1.rect = upgradesOption1ButtonStat1.surf.get_rect(center = (upgradesOption1ButtonStat1.pos[0], upgradesOption1ButtonStat1.pos[1]))
                upgradesOption1ButtonStat1.surf = smallFont.render(upgradesOption1ButtonStat1.text, True, upgradesOption1ButtonStat1.colour)
                    
                upgradesOption1ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonStat2.text)[0],smallFont.size(upgradesOption1ButtonStat2.text)[1]))
                upgradesOption1ButtonStat2.rect = upgradesOption1ButtonStat2.surf.get_rect(center = (upgradesOption1ButtonStat2.pos[0], upgradesOption1ButtonStat2.pos[1]))
                upgradesOption1ButtonStat2.surf = smallFont.render(upgradesOption1ButtonStat2.text, True, upgradesOption1ButtonStat2.colour)
                    
                upgradesOption1ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonStat3.text)[0],smallFont.size(upgradesOption1ButtonStat3.text)[1]))
                upgradesOption1ButtonStat3.rect = upgradesOption1ButtonStat3.surf.get_rect(center = (upgradesOption1ButtonStat3.pos[0], upgradesOption1ButtonStat3.pos[1]))
                upgradesOption1ButtonStat3.surf = smallFont.render(upgradesOption1ButtonStat3.text, True, upgradesOption1ButtonStat3.colour)
                
                
                if dungeon1Upgrades[0] == "Sharpen" or dungeon2Upgrades[0] == "Sharpen" or dungeon3Upgrades[0] == "Sharpen" or dungeon4Upgrades[0] == "Sharpen" or dungeon5Upgrades[0] == "Sharpen":
                    upgradesOption2ButtonText.text = "Sharpen"
                    upgradesOption2ButtonStat1.text = "+1 Damage"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Resist" or dungeon2Upgrades[0] == "Resist" or dungeon3Upgrades[0] == "Resist" or dungeon4Upgrades[0] == "Resist" or dungeon5Upgrades[0] == "Resist":
                    upgradesOption2ButtonText.text = "Resist"
                    upgradesOption2ButtonStat1.text = "+1 Max Health"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fast" or dungeon2Upgrades[0] == "Fast" or dungeon3Upgrades[0] == "Fast" or dungeon4Upgrades[0] == "Fast" or dungeon5Upgrades[0] == "Fast":
                    upgradesOption2ButtonText.text = "Fast"
                    upgradesOption2ButtonStat1.text = "+10% Velocity"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dextrous" or dungeon2Upgrades[0] == "Dextrous" or dungeon3Upgrades[0] == "Dextrous" or dungeon4Upgrades[0] == "Dextrous" or dungeon5Upgrades[0] == "Dextrous":
                    upgradesOption2ButtonText.text = "Dextrous"
                    upgradesOption2ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Extend" or dungeon2Upgrades[0] == "Extend" or dungeon3Upgrades[0] == "Extend" or dungeon4Upgrades[0] == "Extend" or dungeon5Upgrades[0] == "Extend":
                    upgradesOption2ButtonText.text = "Extend"
                    upgradesOption2ButtonStat1.text = "+10% Range"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Honed" or dungeon2Upgrades[0] == "Honed" or dungeon3Upgrades[0] == "Honed" or dungeon4Upgrades[0] == "Honed" or dungeon5Upgrades[0] == "Honed":
                    upgradesOption2ButtonText.text = "Honed"
                    upgradesOption2ButtonStat1.text = "+1 Damage"
                    upgradesOption2ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Deft" or dungeon2Upgrades[0] == "Deft" or dungeon3Upgrades[0] == "Deft" or dungeon4Upgrades[0] == "Deft" or dungeon5Upgrades[0] == "Deft":
                    upgradesOption2ButtonText.text = "Deft"
                    upgradesOption2ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Broaden" or dungeon2Upgrades[0] == "Broaden" or dungeon3Upgrades[0] == "Broaden" or dungeon4Upgrades[0] == "Broaden" or dungeon5Upgrades[0] == "Broaden":
                    upgradesOption2ButtonText.text = "Broaden"
                    upgradesOption2ButtonStat1.text = "+1 Max Health"
                    upgradesOption2ButtonStat2.text = "+10% Range"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Boost" or dungeon2Upgrades[0] == "Boost" or dungeon3Upgrades[0] == "Boost" or dungeon4Upgrades[0] == "Boost" or dungeon5Upgrades[0] == "Boost":
                    upgradesOption2ButtonText.text = "Boost"
                    upgradesOption2ButtonStat1.text = "+1 Max Health"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Blacksmith" or dungeon2Upgrades[0] == "Blacksmith" or dungeon3Upgrades[0] == "Blacksmith" or dungeon4Upgrades[0] == "Blacksmith" or dungeon5Upgrades[0] == "Blacksmith":
                    upgradesOption2ButtonText.text = "Blacksmith"
                    upgradesOption2ButtonStat1.text = "+1 Damage"
                    upgradesOption2ButtonStat2.text = "+10% Range"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Stoic" or dungeon2Upgrades[0] == "Stoic" or dungeon3Upgrades[0] == "Stoic" or dungeon4Upgrades[0] == "Stoic" or dungeon5Upgrades[0] == "Stoic":
                    upgradesOption2ButtonText.text = "Stoic"
                    upgradesOption2ButtonStat1.text = "+2 Max Health"
                    upgradesOption2ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Temper" or dungeon2Upgrades[0] == "Temper" or dungeon3Upgrades[0] == "Temper" or dungeon4Upgrades[0] == "Temper" or dungeon5Upgrades[0] == "Temper":
                    upgradesOption2ButtonText.text = "Temper"
                    upgradesOption2ButtonStat1.text = "+2 Damage"
                    upgradesOption2ButtonStat2.text = "-1 Max Health"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Inflate" or dungeon2Upgrades[0] == "Inflate" or dungeon3Upgrades[0] == "Inflate" or dungeon4Upgrades[0] == "Inflate" or dungeon5Upgrades[0] == "Inflate":
                    upgradesOption2ButtonText.text = "Inflate"
                    upgradesOption2ButtonStat1.text = "+20% Range"
                    upgradesOption2ButtonStat2.text = "-10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Exercise" or dungeon2Upgrades[0] == "Exercise" or dungeon3Upgrades[0] == "Exercise" or dungeon4Upgrades[0] == "Exercise" or dungeon5Upgrades[0] == "Exercise":
                    upgradesOption2ButtonText.text = "Exercise"
                    upgradesOption2ButtonStat1.text = "+20% Velocity"
                    upgradesOption2ButtonStat2.text = "-10% Range"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Unruly" or dungeon2Upgrades[0] == "Unruly" or dungeon3Upgrades[0] == "Unruly" or dungeon4Upgrades[0] == "Unruly" or dungeon5Upgrades[0] == "Unruly":
                    upgradesOption2ButtonText.text = "Unruly"
                    upgradesOption2ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption2ButtonStat2.text = "-1 Damage"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Toughen" or dungeon2Upgrades[0] == "Toughen" or dungeon3Upgrades[0] == "Toughen" or dungeon4Upgrades[0] == "Toughen" or dungeon5Upgrades[0] == "Toughen":
                    upgradesOption2ButtonText.text = "Toughen"
                    upgradesOption2ButtonStat1.text = "+2 Max Health"
                    upgradesOption2ButtonStat2.text = "+1 Damage"
                    upgradesOption2ButtonStat3.text = "-10% Velocity"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Speedier" or dungeon2Upgrades[0] == "Speedier" or dungeon3Upgrades[0] == "Speedier" or dungeon4Upgrades[0] == "Speedier" or dungeon5Upgrades[0] == "Speedier":
                    upgradesOption2ButtonText.text = "Speedier"
                    upgradesOption2ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = "-10% Range"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Embiggen" or dungeon2Upgrades[0] == "Embiggen" or dungeon3Upgrades[0] == "Embiggen" or dungeon4Upgrades[0] == "Embiggen" or dungeon5Upgrades[0] == "Embiggen":
                    upgradesOption2ButtonText.text = "Embiggen"
                    upgradesOption2ButtonStat1.text = "+20% Range"
                    upgradesOption2ButtonStat2.text = "+1 Max Health"
                    upgradesOption2ButtonStat3.text = "-1 Damage"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Smite" or dungeon2Upgrades[0] == "Smite" or dungeon3Upgrades[0] == "Smite" or dungeon4Upgrades[0] == "Smite" or dungeon5Upgrades[0] == "Smite":
                    upgradesOption2ButtonText.text = "Smite"
                    upgradesOption2ButtonStat1.text = "+3 Damage"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fortify" or dungeon2Upgrades[0] == "Fortify" or dungeon3Upgrades[0] == "Fortify" or dungeon4Upgrades[0] == "Fortify" or dungeon5Upgrades[0] == "Fortify":
                    upgradesOption2ButtonText.text = "Fortify"
                    upgradesOption2ButtonStat1.text = "+3 Max Health"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rush" or dungeon2Upgrades[0] == "Rush" or dungeon3Upgrades[0] == "Rush" or dungeon4Upgrades[0] == "Rush" or dungeon5Upgrades[0] == "Rush":
                    upgradesOption2ButtonText.text = "Rush"
                    upgradesOption2ButtonStat1.text = "+30% Velocity"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Lash" or dungeon2Upgrades[0] == "Lash" or dungeon3Upgrades[0] == "Lash" or dungeon4Upgrades[0] == "Lash" or dungeon5Upgrades[0] == "Lash":
                    upgradesOption2ButtonText.text = "Lash"
                    upgradesOption2ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Bolster" or dungeon2Upgrades[0] == "Bolster" or dungeon3Upgrades[0] == "Bolster" or dungeon4Upgrades[0] == "Bolster" or dungeon5Upgrades[0] == "Bolster":
                    upgradesOption2ButtonText.text = "Bolster"
                    upgradesOption2ButtonStat1.text = "+30% Range"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dash" or dungeon2Upgrades[0] == "Dash" or dungeon3Upgrades[0] == "Dash" or dungeon4Upgrades[0] == "Dash" or dungeon5Upgrades[0] == "Dash":
                    upgradesOption2ButtonText.text = "Dash"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Saviour" or dungeon2Upgrades[0] == "Saviour" or dungeon3Upgrades[0] == "Saviour" or dungeon4Upgrades[0] == "Saviour" or dungeon5Upgrades[0] == "Saviour":
                    upgradesOption2ButtonText.text = "Saviour"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+2 Max Health"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rampage" or dungeon2Upgrades[0] == "Rampage" or dungeon3Upgrades[0] == "Rampage" or dungeon4Upgrades[0] == "Rampage" or dungeon5Upgrades[0] == "Rampage":
                    upgradesOption2ButtonText.text = "Rampage"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+1 Damage"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Burst" or dungeon2Upgrades[0] == "Burst" or dungeon3Upgrades[0] == "Burst" or dungeon4Upgrades[0] == "Burst" or dungeon5Upgrades[0] == "Burst":
                    upgradesOption2ButtonText.text = "Burst"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Pulse" or dungeon2Upgrades[0] == "Pulse" or dungeon3Upgrades[0] == "Pulse" or dungeon4Upgrades[0] == "Pulse" or dungeon5Upgrades[0] == "Pulse":
                    upgradesOption2ButtonText.text = "Pulse"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+10% Range"
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Super" or dungeon2Upgrades[0] == "Super" or dungeon3Upgrades[0] == "Super" or dungeon4Upgrades[0] == "Super" or dungeon5Upgrades[0] == "Super":
                    upgradesOption2ButtonText.text = "Super"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                        
                upgradesOption2ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonText.text)[0],smallFont.size(upgradesOption2ButtonText.text)[1]))
                upgradesOption2ButtonText.rect = upgradesOption2ButtonText.surf.get_rect(center = (upgradesOption2ButtonText.pos[0], upgradesOption2ButtonText.pos[1]))
                upgradesOption2ButtonText.surf = smallFont.render(upgradesOption2ButtonText.text, True, upgradesOption2ButtonText.colour)
                    
                upgradesOption2ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonStat1.text)[0],smallFont.size(upgradesOption2ButtonStat1.text)[1]))
                upgradesOption2ButtonStat1.rect = upgradesOption2ButtonStat1.surf.get_rect(center = (upgradesOption2ButtonStat1.pos[0], upgradesOption2ButtonStat1.pos[1]))
                upgradesOption2ButtonStat1.surf = smallFont.render(upgradesOption2ButtonStat1.text, True, upgradesOption2ButtonStat1.colour)
                    
                upgradesOption2ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonStat2.text)[0],smallFont.size(upgradesOption2ButtonStat2.text)[1]))
                upgradesOption2ButtonStat2.rect = upgradesOption2ButtonStat2.surf.get_rect(center = (upgradesOption2ButtonStat2.pos[0], upgradesOption2ButtonStat2.pos[1]))
                upgradesOption2ButtonStat2.surf = smallFont.render(upgradesOption2ButtonStat2.text, True, upgradesOption2ButtonStat2.colour)
                    
                upgradesOption2ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonStat3.text)[0],smallFont.size(upgradesOption2ButtonStat3.text)[1]))
                upgradesOption2ButtonStat3.rect = upgradesOption2ButtonStat3.surf.get_rect(center = (upgradesOption2ButtonStat3.pos[0], upgradesOption2ButtonStat3.pos[1]))
                upgradesOption2ButtonStat3.surf = smallFont.render(upgradesOption2ButtonStat3.text, True, upgradesOption2ButtonStat3.colour)    
            
                if dungeon1Upgrades[0] == "Sharpen" or dungeon2Upgrades[0] == "Sharpen" or dungeon3Upgrades[0] == "Sharpen" or dungeon4Upgrades[0] == "Sharpen" or dungeon5Upgrades[0] == "Sharpen":
                    upgradesOption3ButtonText.text = "Sharpen"
                    upgradesOption3ButtonStat1.text = "+1 Damage"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Resist" or dungeon2Upgrades[0] == "Resist" or dungeon3Upgrades[0] == "Resist" or dungeon4Upgrades[0] == "Resist" or dungeon5Upgrades[0] == "Resist":
                    upgradesOption3ButtonText.text = "Resist"
                    upgradesOption3ButtonStat1.text = "+1 Max Health"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fast" or dungeon2Upgrades[0] == "Fast" or dungeon3Upgrades[0] == "Fast" or dungeon4Upgrades[0] == "Fast" or dungeon5Upgrades[0] == "Fast":
                    upgradesOption3ButtonText.text = "Fast"
                    upgradesOption3ButtonStat1.text = "+10% Velocity"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dextrous" or dungeon2Upgrades[0] == "Dextrous" or dungeon3Upgrades[0] == "Dextrous" or dungeon4Upgrades[0] == "Dextrous" or dungeon5Upgrades[0] == "Dextrous":
                    upgradesOption3ButtonText.text = "Dextrous"
                    upgradesOption3ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Extend" or dungeon2Upgrades[0] == "Extend" or dungeon3Upgrades[0] == "Extend" or dungeon4Upgrades[0] == "Extend" or dungeon5Upgrades[0] == "Extend":
                    upgradesOption3ButtonText.text = "Extend"
                    upgradesOption3ButtonStat1.text = "+10% Range"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Honed" or dungeon2Upgrades[0] == "Honed" or dungeon3Upgrades[0] == "Honed" or dungeon4Upgrades[0] == "Honed" or dungeon5Upgrades[0] == "Honed":
                    upgradesOption3ButtonText.text = "Honed"
                    upgradesOption3ButtonStat1.text = "+1 Damage"
                    upgradesOption3ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Deft" or dungeon2Upgrades[0] == "Deft" or dungeon3Upgrades[0] == "Deft" or dungeon4Upgrades[0] == "Deft" or dungeon5Upgrades[0] == "Deft":
                    upgradesOption3ButtonText.text = "Deft"
                    upgradesOption3ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Broaden" or dungeon2Upgrades[0] == "Broaden" or dungeon3Upgrades[0] == "Broaden" or dungeon4Upgrades[0] == "Broaden" or dungeon5Upgrades[0] == "Broaden":
                    upgradesOption3ButtonText.text = "Broaden"
                    upgradesOption3ButtonStat1.text = "+1 Max Health"
                    upgradesOption3ButtonStat2.text = "+10% Range"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Boost" or dungeon2Upgrades[0] == "Boost" or dungeon3Upgrades[0] == "Boost" or dungeon4Upgrades[0] == "Boost" or dungeon5Upgrades[0] == "Boost":
                    upgradesOption3ButtonText.text = "Boost"
                    upgradesOption3ButtonStat1.text = "+1 Max Health"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Blacksmith" or dungeon2Upgrades[0] == "Blacksmith" or dungeon3Upgrades[0] == "Blacksmith" or dungeon4Upgrades[0] == "Blacksmith" or dungeon5Upgrades[0] == "Blacksmith":
                    upgradesOption3ButtonText.text = "Blacksmith"
                    upgradesOption3ButtonStat1.text = "+1 Damage"
                    upgradesOption3ButtonStat2.text = "+10% Range"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Stoic" or dungeon2Upgrades[0] == "Stoic" or dungeon3Upgrades[0] == "Stoic" or dungeon4Upgrades[0] == "Stoic" or dungeon5Upgrades[0] == "Stoic":
                    upgradesOption3ButtonText.text = "Stoic"
                    upgradesOption3ButtonStat1.text = "+2 Max Health"
                    upgradesOption3ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Temper" or dungeon2Upgrades[0] == "Temper" or dungeon3Upgrades[0] == "Temper" or dungeon4Upgrades[0] == "Temper" or dungeon5Upgrades[0] == "Temper":
                    upgradesOption3ButtonText.text = "Temper"
                    upgradesOption3ButtonStat1.text = "+2 Damage"
                    upgradesOption3ButtonStat2.text = "-1 Max Health"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Inflate" or dungeon2Upgrades[0] == "Inflate" or dungeon3Upgrades[0] == "Inflate" or dungeon4Upgrades[0] == "Inflate" or dungeon5Upgrades[0] == "Inflate":
                    upgradesOption3ButtonText.text = "Inflate"
                    upgradesOption3ButtonStat1.text = "+20% Range"
                    upgradesOption3ButtonStat2.text = "-10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Exercise" or dungeon2Upgrades[0] == "Exercise" or dungeon3Upgrades[0] == "Exercise" or dungeon4Upgrades[0] == "Exercise" or dungeon5Upgrades[0] == "Exercise":
                    upgradesOption3ButtonText.text = "Exercise"
                    upgradesOption3ButtonStat1.text = "+20% Velocity"
                    upgradesOption3ButtonStat2.text = "-10% Range"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Unruly" or dungeon2Upgrades[0] == "Unruly" or dungeon3Upgrades[0] == "Unruly" or dungeon4Upgrades[0] == "Unruly" or dungeon5Upgrades[0] == "Unruly":
                    upgradesOption3ButtonText.text = "Unruly"
                    upgradesOption3ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption3ButtonStat2.text = "-1 Damage"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Toughen" or dungeon2Upgrades[0] == "Toughen" or dungeon3Upgrades[0] == "Toughen" or dungeon4Upgrades[0] == "Toughen" or dungeon5Upgrades[0] == "Toughen":
                    upgradesOption3ButtonText.text = "Toughen"
                    upgradesOption3ButtonStat1.text = "+2 Max Health"
                    upgradesOption3ButtonStat2.text = "+1 Damage"
                    upgradesOption3ButtonStat3.text = "-10% Velocity"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Speedier" or dungeon2Upgrades[0] == "Speedier" or dungeon3Upgrades[0] == "Speedier" or dungeon4Upgrades[0] == "Speedier" or dungeon5Upgrades[0] == "Speedier":
                    upgradesOption3ButtonText.text = "Speedier"
                    upgradesOption3ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = "-10% Range"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Embiggen" or dungeon2Upgrades[0] == "Embiggen" or dungeon3Upgrades[0] == "Embiggen" or dungeon4Upgrades[0] == "Embiggen" or dungeon5Upgrades[0] == "Embiggen":
                    upgradesOption3ButtonText.text = "Embiggen"
                    upgradesOption3ButtonStat1.text = "+20% Range"
                    upgradesOption3ButtonStat2.text = "+1 Max Health"
                    upgradesOption3ButtonStat3.text = "-1 Damage"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Smite" or dungeon2Upgrades[0] == "Smite" or dungeon3Upgrades[0] == "Smite" or dungeon4Upgrades[0] == "Smite" or dungeon5Upgrades[0] == "Smite":
                    upgradesOption3ButtonText.text = "Smite"
                    upgradesOption3ButtonStat1.text = "+3 Damage"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fortify" or dungeon2Upgrades[0] == "Fortify" or dungeon3Upgrades[0] == "Fortify" or dungeon4Upgrades[0] == "Fortify" or dungeon5Upgrades[0] == "Fortify":
                    upgradesOption3ButtonText.text = "Fortify"
                    upgradesOption3ButtonStat1.text = "+3 Max Health"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rush" or dungeon2Upgrades[0] == "Rush" or dungeon3Upgrades[0] == "Rush" or dungeon4Upgrades[0] == "Rush" or dungeon5Upgrades[0] == "Rush":
                    upgradesOption3ButtonText.text = "Rush"
                    upgradesOption3ButtonStat1.text = "+30% Velocity"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Lash" or dungeon2Upgrades[0] == "Lash" or dungeon3Upgrades[0] == "Lash" or dungeon4Upgrades[0] == "Lash" or dungeon5Upgrades[0] == "Lash":
                    upgradesOption3ButtonText.text = "Lash"
                    upgradesOption3ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Bolster" or dungeon2Upgrades[0] == "Bolster" or dungeon3Upgrades[0] == "Bolster" or dungeon4Upgrades[0] == "Bolster" or dungeon5Upgrades[0] == "Bolster":
                    upgradesOption3ButtonText.text = "Bolster"
                    upgradesOption3ButtonStat1.text = "+30% Range"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dash" or dungeon2Upgrades[0] == "Dash" or dungeon3Upgrades[0] == "Dash" or dungeon4Upgrades[0] == "Dash" or dungeon5Upgrades[0] == "Dash":
                    upgradesOption3ButtonText.text = "Dash"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Saviour" or dungeon2Upgrades[0] == "Saviour" or dungeon3Upgrades[0] == "Saviour" or dungeon4Upgrades[0] == "Saviour" or dungeon5Upgrades[0] == "Saviour":
                    upgradesOption3ButtonText.text = "Saviour"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+2 Max Health"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rampage" or dungeon2Upgrades[0] == "Rampage" or dungeon3Upgrades[0] == "Rampage" or dungeon4Upgrades[0] == "Rampage" or dungeon5Upgrades[0] == "Rampage":
                    upgradesOption3ButtonText.text = "Rampage"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+1 Damage"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Burst" or dungeon2Upgrades[0] == "Burst" or dungeon3Upgrades[0] == "Burst" or dungeon4Upgrades[0] == "Burst" or dungeon5Upgrades[0] == "Burst":
                    upgradesOption3ButtonText.text = "Burst"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Pulse" or dungeon2Upgrades[0] == "Pulse" or dungeon3Upgrades[0] == "Pulse" or dungeon4Upgrades[0] == "Pulse" or dungeon5Upgrades[0] == "Pulse":
                    upgradesOption3ButtonText.text = "Pulse"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+10% Range"
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Super" or dungeon2Upgrades[0] == "Super" or dungeon3Upgrades[0] == "Super" or dungeon4Upgrades[0] == "Super" or dungeon5Upgrades[0] == "Super":
                    upgradesOption3ButtonText.text = "Super"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                        
                upgradesOption3ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonText.text)[0],smallFont.size(upgradesOption3ButtonText.text)[1]))
                upgradesOption3ButtonText.rect = upgradesOption3ButtonText.surf.get_rect(center = (upgradesOption3ButtonText.pos[0], upgradesOption3ButtonText.pos[1]))
                upgradesOption3ButtonText.surf = smallFont.render(upgradesOption3ButtonText.text, True, upgradesOption3ButtonText.colour)
                    
                upgradesOption3ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonStat1.text)[0],smallFont.size(upgradesOption3ButtonStat1.text)[1]))
                upgradesOption3ButtonStat1.rect = upgradesOption3ButtonStat1.surf.get_rect(center = (upgradesOption3ButtonStat1.pos[0], upgradesOption3ButtonStat1.pos[1]))
                upgradesOption3ButtonStat1.surf = smallFont.render(upgradesOption3ButtonStat1.text, True, upgradesOption3ButtonStat1.colour)
                    
                upgradesOption3ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonStat2.text)[0],smallFont.size(upgradesOption3ButtonStat2.text)[1]))
                upgradesOption3ButtonStat2.rect = upgradesOption3ButtonStat2.surf.get_rect(center = (upgradesOption3ButtonStat2.pos[0], upgradesOption3ButtonStat2.pos[1]))
                upgradesOption3ButtonStat2.surf = smallFont.render(upgradesOption3ButtonStat2.text, True, upgradesOption3ButtonStat2.colour)
                    
                upgradesOption3ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonStat3.text)[0],smallFont.size(upgradesOption3ButtonStat3.text)[1]))
                upgradesOption3ButtonStat3.rect = upgradesOption3ButtonStat3.surf.get_rect(center = (upgradesOption3ButtonStat3.pos[0], upgradesOption3ButtonStat3.pos[1]))
                upgradesOption3ButtonStat3.surf = smallFont.render(upgradesOption3ButtonStat3.text, True, upgradesOption3ButtonStat3.colour)            


                if dungeon1Upgrades[0] == "Sharpen" or dungeon2Upgrades[0] == "Sharpen" or dungeon3Upgrades[0] == "Sharpen" or dungeon4Upgrades[0] == "Sharpen" or dungeon5Upgrades[0] == "Sharpen":
                    upgradesOption4ButtonText.text = "Sharpen"
                    upgradesOption4ButtonStat1.text = "+1 Damage"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Resist" or dungeon2Upgrades[0] == "Resist" or dungeon3Upgrades[0] == "Resist" or dungeon4Upgrades[0] == "Resist" or dungeon5Upgrades[0] == "Resist":
                    upgradesOption4ButtonText.text = "Resist"
                    upgradesOption4ButtonStat1.text = "+1 Max Health"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fast" or dungeon2Upgrades[0] == "Fast" or dungeon3Upgrades[0] == "Fast" or dungeon4Upgrades[0] == "Fast" or dungeon5Upgrades[0] == "Fast":
                    upgradesOption4ButtonText.text = "Fast"
                    upgradesOption4ButtonStat1.text = "+10% Velocity"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dextrous" or dungeon2Upgrades[0] == "Dextrous" or dungeon3Upgrades[0] == "Dextrous" or dungeon4Upgrades[0] == "Dextrous" or dungeon5Upgrades[0] == "Dextrous":
                    upgradesOption4ButtonText.text = "Dextrous"
                    upgradesOption4ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Extend" or dungeon2Upgrades[0] == "Extend" or dungeon3Upgrades[0] == "Extend" or dungeon4Upgrades[0] == "Extend" or dungeon5Upgrades[0] == "Extend":
                    upgradesOption4ButtonText.text = "Extend"
                    upgradesOption4ButtonStat1.text = "+10% Range"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Honed" or dungeon2Upgrades[0] == "Honed" or dungeon3Upgrades[0] == "Honed" or dungeon4Upgrades[0] == "Honed" or dungeon5Upgrades[0] == "Honed":
                    upgradesOption4ButtonText.text = "Honed"
                    upgradesOption4ButtonStat1.text = "+1 Damage"
                    upgradesOption4ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Deft" or dungeon2Upgrades[0] == "Deft" or dungeon3Upgrades[0] == "Deft" or dungeon4Upgrades[0] == "Deft" or dungeon5Upgrades[0] == "Deft":
                    upgradesOption4ButtonText.text = "Deft"
                    upgradesOption4ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Broaden" or dungeon2Upgrades[0] == "Broaden" or dungeon3Upgrades[0] == "Broaden" or dungeon4Upgrades[0] == "Broaden" or dungeon5Upgrades[0] == "Broaden":
                    upgradesOption4ButtonText.text = "Broaden"
                    upgradesOption4ButtonStat1.text = "+1 Max Health"
                    upgradesOption4ButtonStat2.text = "+10% Range"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Boost" or dungeon2Upgrades[0] == "Boost" or dungeon3Upgrades[0] == "Boost" or dungeon4Upgrades[0] == "Boost" or dungeon5Upgrades[0] == "Boost":
                    upgradesOption4ButtonText.text = "Boost"
                    upgradesOption4ButtonStat1.text = "+1 Max Health"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Blacksmith" or dungeon2Upgrades[0] == "Blacksmith" or dungeon3Upgrades[0] == "Blacksmith" or dungeon4Upgrades[0] == "Blacksmith" or dungeon5Upgrades[0] == "Blacksmith":
                    upgradesOption4ButtonText.text = "Blacksmith"
                    upgradesOption4ButtonStat1.text = "+1 Damage"
                    upgradesOption4ButtonStat2.text = "+10% Range"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Stoic" or dungeon2Upgrades[0] == "Stoic" or dungeon3Upgrades[0] == "Stoic" or dungeon4Upgrades[0] == "Stoic" or dungeon5Upgrades[0] == "Stoic":
                    upgradesOption4ButtonText.text = "Stoic"
                    upgradesOption4ButtonStat1.text = "+2 Max Health"
                    upgradesOption4ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Temper" or dungeon2Upgrades[0] == "Temper" or dungeon3Upgrades[0] == "Temper" or dungeon4Upgrades[0] == "Temper" or dungeon5Upgrades[0] == "Temper":
                    upgradesOption4ButtonText.text = "Temper"
                    upgradesOption4ButtonStat1.text = "+2 Damage"
                    upgradesOption4ButtonStat2.text = "-1 Max Health"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Inflate" or dungeon2Upgrades[0] == "Inflate" or dungeon3Upgrades[0] == "Inflate" or dungeon4Upgrades[0] == "Inflate" or dungeon5Upgrades[0] == "Inflate":
                    upgradesOption4ButtonText.text = "Inflate"
                    upgradesOption4ButtonStat1.text = "+20% Range"
                    upgradesOption4ButtonStat2.text = "-10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Exercise" or dungeon2Upgrades[0] == "Exercise" or dungeon3Upgrades[0] == "Exercise" or dungeon4Upgrades[0] == "Exercise" or dungeon5Upgrades[0] == "Exercise":
                    upgradesOption4ButtonText.text = "Exercise"
                    upgradesOption4ButtonStat1.text = "+20% Velocity"
                    upgradesOption4ButtonStat2.text = "-10% Range"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Unruly" or dungeon2Upgrades[0] == "Unruly" or dungeon3Upgrades[0] == "Unruly" or dungeon4Upgrades[0] == "Unruly" or dungeon5Upgrades[0] == "Unruly":
                    upgradesOption4ButtonText.text = "Unruly"
                    upgradesOption4ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption4ButtonStat2.text = "-1 Damage"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Toughen" or dungeon2Upgrades[0] == "Toughen" or dungeon3Upgrades[0] == "Toughen" or dungeon4Upgrades[0] == "Toughen" or dungeon5Upgrades[0] == "Toughen":
                    upgradesOption4ButtonText.text = "Toughen"
                    upgradesOption4ButtonStat1.text = "+2 Max Health"
                    upgradesOption4ButtonStat2.text = "+1 Damage"
                    upgradesOption4ButtonStat3.text = "-10% Velocity"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Speedier" or dungeon2Upgrades[0] == "Speedier" or dungeon3Upgrades[0] == "Speedier" or dungeon4Upgrades[0] == "Speedier" or dungeon5Upgrades[0] == "Speedier":
                    upgradesOption4ButtonText.text = "Speedier"
                    upgradesOption4ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = "-10% Range"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Embiggen" or dungeon2Upgrades[0] == "Embiggen" or dungeon3Upgrades[0] == "Embiggen" or dungeon4Upgrades[0] == "Embiggen" or dungeon5Upgrades[0] == "Embiggen":
                    upgradesOption4ButtonText.text = "Embiggen"
                    upgradesOption4ButtonStat1.text = "+20% Range"
                    upgradesOption4ButtonStat2.text = "+1 Max Health"
                    upgradesOption4ButtonStat3.text = "-1 Damage"
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Smite" or dungeon2Upgrades[0] == "Smite" or dungeon3Upgrades[0] == "Smite" or dungeon4Upgrades[0] == "Smite" or dungeon5Upgrades[0] == "Smite":
                    upgradesOption4ButtonText.text = "Smite"
                    upgradesOption4ButtonStat1.text = "+3 Damage"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Fortify" or dungeon2Upgrades[0] == "Fortify" or dungeon3Upgrades[0] == "Fortify" or dungeon4Upgrades[0] == "Fortify" or dungeon5Upgrades[0] == "Fortify":
                    upgradesOption4ButtonText.text = "Fortify"
                    upgradesOption4ButtonStat1.text = "+3 Max Health"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rush" or dungeon2Upgrades[0] == "Rush" or dungeon3Upgrades[0] == "Rush" or dungeon4Upgrades[0] == "Rush" or dungeon5Upgrades[0] == "Rush":
                    upgradesOption4ButtonText.text = "Rush"
                    upgradesOption4ButtonStat1.text = "+30% Velocity"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Lash" or dungeon2Upgrades[0] == "Lash" or dungeon3Upgrades[0] == "Lash" or dungeon4Upgrades[0] == "Lash" or dungeon5Upgrades[0] == "Lash":
                    upgradesOption4ButtonText.text = "Lash"
                    upgradesOption4ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Bolster" or dungeon2Upgrades[0] == "Bolster" or dungeon3Upgrades[0] == "Bolster" or dungeon4Upgrades[0] == "Bolster" or dungeon5Upgrades[0] == "Bolster":
                    upgradesOption4ButtonText.text = "Bolster"
                    upgradesOption4ButtonStat1.text = "+30% Range"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Dash" or dungeon2Upgrades[0] == "Dash" or dungeon3Upgrades[0] == "Dash" or dungeon4Upgrades[0] == "Dash" or dungeon5Upgrades[0] == "Dash":
                    upgradesOption4ButtonText.text = "Dash"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Saviour" or dungeon2Upgrades[0] == "Saviour" or dungeon3Upgrades[0] == "Saviour" or dungeon4Upgrades[0] == "Saviour" or dungeon5Upgrades[0] == "Saviour":
                    upgradesOption4ButtonText.text = "Saviour"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+2 Max Health"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Rampage" or dungeon2Upgrades[0] == "Rampage" or dungeon3Upgrades[0] == "Rampage" or dungeon4Upgrades[0] == "Rampage" or dungeon5Upgrades[0] == "Rampage":
                    upgradesOption4ButtonText.text = "Rampage"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+1 Damage"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Burst" or dungeon2Upgrades[0] == "Burst" or dungeon3Upgrades[0] == "Burst" or dungeon4Upgrades[0] == "Burst" or dungeon5Upgrades[0] == "Burst":
                    upgradesOption4ButtonText.text = "Burst"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Pulse" or dungeon2Upgrades[0] == "Pulse" or dungeon3Upgrades[0] == "Pulse" or dungeon4Upgrades[0] == "Pulse" or dungeon5Upgrades[0] == "Pulse":
                    upgradesOption4ButtonText.text = "Pulse"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+10% Range"
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                elif dungeon1Upgrades[0] == "Super" or dungeon2Upgrades[0] == "Super" or dungeon3Upgrades[0] == "Super" or dungeon4Upgrades[0] == "Super" or dungeon5Upgrades[0] == "Super":
                    upgradesOption4ButtonText.text = "Super"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                    if currentDungeon == 1 :
                        dungeon1Upgrades.remove(dungeon1Upgrades[0])
                    elif currentDungeon == 2 :
                        dungeon2Upgrades.remove(dungeon2Upgrades[0])
                    elif currentDungeon == 3 :
                        dungeon3Upgrades.remove(dungeon3Upgrades[0])
                    elif currentDungeon == 4 :
                        dungeon4Upgrades.remove(dungeon4Upgrades[0])
                    elif currentDungeon == 5 :
                        dungeon5Upgrades.remove(dungeon5Upgrades[0])
                        
                upgradesOption4ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonText.text)[0],smallFont.size(upgradesOption4ButtonText.text)[1]))
                upgradesOption4ButtonText.rect = upgradesOption4ButtonText.surf.get_rect(center = (upgradesOption4ButtonText.pos[0], upgradesOption4ButtonText.pos[1]))
                upgradesOption4ButtonText.surf = smallFont.render(upgradesOption4ButtonText.text, True, upgradesOption4ButtonText.colour)
                    
                upgradesOption4ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonStat1.text)[0],smallFont.size(upgradesOption4ButtonStat1.text)[1]))
                upgradesOption4ButtonStat1.rect = upgradesOption4ButtonStat1.surf.get_rect(center = (upgradesOption4ButtonStat1.pos[0], upgradesOption4ButtonStat1.pos[1]))
                upgradesOption4ButtonStat1.surf = smallFont.render(upgradesOption4ButtonStat1.text, True, upgradesOption4ButtonStat1.colour)
                    
                upgradesOption4ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonStat2.text)[0],smallFont.size(upgradesOption4ButtonStat2.text)[1]))
                upgradesOption4ButtonStat2.rect = upgradesOption4ButtonStat2.surf.get_rect(center = (upgradesOption4ButtonStat2.pos[0], upgradesOption4ButtonStat2.pos[1]))
                upgradesOption4ButtonStat2.surf = smallFont.render(upgradesOption4ButtonStat2.text, True, upgradesOption4ButtonStat2.colour)
                    
                upgradesOption4ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonStat3.text)[0],smallFont.size(upgradesOption4ButtonStat3.text)[1]))
                upgradesOption4ButtonStat3.rect = upgradesOption4ButtonStat3.surf.get_rect(center = (upgradesOption4ButtonStat3.pos[0], upgradesOption4ButtonStat3.pos[1]))
                upgradesOption4ButtonStat3.surf = smallFont.render(upgradesOption4ButtonStat3.text, True, upgradesOption4ButtonStat3.colour)


            else:
                
                if floorReward[currentFloor] == 0: #Common
                    randomUpgrade1 = random.randint(0,4)
                    randomUpgrade2 = random.randint(0,4)
                    randomUpgrade3 = random.randint(0,4)
                    randomUpgrade4 = random.randint(0,4)
                elif floorReward[currentFloor] == 1: #Uncommon
                    randomUpgrade1 = random.randint(0,9)
                    randomUpgrade2 = random.randint(0,9)
                    randomUpgrade3 = random.randint(0,9)
                    randomUpgrade4 = random.randint(0,9)
                elif floorReward[currentFloor] == 2: #Rare
                    randomUpgrade1 = random.randint(0,7)
                    randomUpgrade2 = random.randint(0,7) 
                    randomUpgrade3 = random.randint(0,7)
                    randomUpgrade4 = random.randint(0,7)
                elif floorReward[currentFloor] == 3: #Ability
                    randomUpgrade1 = random.randint(1,4)
                    randomUpgrade2 = random.randint(1,4)
                    randomUpgrade3 = random.randint(1,4)
                    randomUpgrade4 = random.randint(1,4)
                while (randomUpgrade1 == randomUpgrade2) or (randomUpgrade1 == randomUpgrade3) or (randomUpgrade1 == randomUpgrade4) or (randomUpgrade2 == randomUpgrade3) or (randomUpgrade2 == randomUpgrade4) or (randomUpgrade3 == randomUpgrade4) :
                    if floorReward[currentFloor] == 0: #Common
                        randomUpgrade1 = random.randint(0,4)
                        randomUpgrade2 = random.randint(0,4)
                        randomUpgrade3 = random.randint(0,4)
                        randomUpgrade4 = random.randint(0,4)
                    elif floorReward[currentFloor] == 1: #Uncommon
                        randomUpgrade1 = random.randint(0,9)
                        randomUpgrade2 = random.randint(0,9)
                        randomUpgrade3 = random.randint(0,9)
                        randomUpgrade4 = random.randint(0,9)
                    elif floorReward[currentFloor] == 2: #Rare
                        randomUpgrade1 = random.randint(0,7)
                        randomUpgrade2 = random.randint(0,7) 
                        randomUpgrade3 = random.randint(0,7)
                        randomUpgrade4 = random.randint(0,7)
                    elif floorReward[currentFloor] == 3: #Ability
                        randomUpgrade1 = random.randint(1,4)
                        randomUpgrade2 = random.randint(1,4)
                        randomUpgrade3 = random.randint(1,4)
                        randomUpgrade4 = random.randint(1,4)
                
                upgradesFloorCountWindowText.text = "Floor: " + str(currentFloor+1 + (loopsOfEndless *70))
                upgradesFloorCountWindowText.surf = pygame.Surface((smallFont.size(upgradesFloorCountWindowText.text)[0],smallFont.size(upgradesFloorCountWindowText.text)[1]))
                upgradesFloorCountWindowText.rect = upgradesFloorCountWindowText.surf.get_rect(center = (upgradesFloorCountWindowText.pos[0], upgradesFloorCountWindowText.pos[1]))
                upgradesFloorCountWindowText.surf = smallFont.render(upgradesFloorCountWindowText.text, True, upgradesFloorCountWindowText.colour)
                
                upgradesStatsWindowHealthTextValue.text = str(player.maxHealth)
                upgradesStatsWindowHealthTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowHealthTextValue.text)[0],smallFont.size(upgradesStatsWindowHealthTextValue.text)[1]))
                upgradesStatsWindowHealthTextValue.rect = upgradesStatsWindowHealthTextValue.surf.get_rect(center = (upgradesStatsWindowHealthTextValue.pos[0], upgradesStatsWindowHealthTextValue.pos[1]))
                upgradesStatsWindowHealthTextValue.surf = smallFont.render(upgradesStatsWindowHealthTextValue.text, True, upgradesStatsWindowHealthTextValue.colour)
                
                upgradesStatsWindowDamageTextValue.text = str(player.damage)
                upgradesStatsWindowDamageTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowDamageTextValue.text)[0],smallFont.size(upgradesStatsWindowDamageTextValue.text)[1]))
                upgradesStatsWindowDamageTextValue.rect = upgradesStatsWindowDamageTextValue.surf.get_rect(center = (upgradesStatsWindowDamageTextValue.pos[0], upgradesStatsWindowDamageTextValue.pos[1]))
                upgradesStatsWindowDamageTextValue.surf = smallFont.render(upgradesStatsWindowDamageTextValue.text, True, upgradesStatsWindowDamageTextValue.colour)
                
                if player.Dspeed // 100 >= 1 : #Handles 100% or greater
                    upgradesStatsWindowDSpeedTextValue.text = "X" + str(player.Dspeed)[0] + "." + str(player.Dspeed)[1:]
                else:                              #Handles 99% or less
                    upgradesStatsWindowDSpeedTextValue.text = "X" + "0" + "." + str(player.Dspeed)[0:]
                upgradesStatsWindowDSpeedTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowDSpeedTextValue.text)[0],smallFont.size(upgradesStatsWindowDSpeedTextValue.text)[1]))
                upgradesStatsWindowDSpeedTextValue.rect = upgradesStatsWindowDSpeedTextValue.surf.get_rect(center = (upgradesStatsWindowDSpeedTextValue.pos[0], upgradesStatsWindowDSpeedTextValue.pos[1]))
                upgradesStatsWindowDSpeedTextValue.surf = smallFont.render(upgradesStatsWindowDSpeedTextValue.text, True, upgradesStatsWindowDSpeedTextValue.colour)
                
                if player.Mspeed // 100 >= 1 : 
                    upgradesStatsWindowMSpeedTextValue.text = "X" + str(player.Mspeed)[0] + "." + str(player.Mspeed)[1:]
                else:                              
                    upgradesStatsWindowMSpeedTextValue.text = "X" + "0" + "." + str(player.Mspeed)[0:]
                upgradesStatsWindowMSpeedTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowMSpeedTextValue.text)[0],smallFont.size(upgradesStatsWindowMSpeedTextValue.text)[1]))
                upgradesStatsWindowMSpeedTextValue.rect = upgradesStatsWindowMSpeedTextValue.surf.get_rect(center = (upgradesStatsWindowMSpeedTextValue.pos[0], upgradesStatsWindowMSpeedTextValue.pos[1]))
                upgradesStatsWindowMSpeedTextValue.surf = smallFont.render(upgradesStatsWindowMSpeedTextValue.text, True, upgradesStatsWindowMSpeedTextValue.colour)

                if player.range // 100 >= 1 : 
                    upgradesStatsWindowRangeTextValue.text = "X" + str(player.range)[0] + "." + str(player.range)[1:]
                else:                              
                    upgradesStatsWindowRangeTextValue.text = "X" + "0" + "." + str(player.range)[0:]
                upgradesStatsWindowRangeTextValue.surf = pygame.Surface((smallFont.size(upgradesStatsWindowRangeTextValue.text)[0],smallFont.size(upgradesStatsWindowRangeTextValue.text)[1]))
                upgradesStatsWindowRangeTextValue.rect = upgradesStatsWindowRangeTextValue.surf.get_rect(center = (upgradesStatsWindowRangeTextValue.pos[0], upgradesStatsWindowRangeTextValue.pos[1]))
                upgradesStatsWindowRangeTextValue.surf = smallFont.render(upgradesStatsWindowRangeTextValue.text, True, upgradesStatsWindowRangeTextValue.colour)

    #Upgrade Button Checks ========================================================================================================================================================            
                if masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Sharpen":
                    upgradesOption1ButtonText.text = "Sharpen"
                    upgradesOption1ButtonStat1.text = "+1 Damage"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Resist":
                    upgradesOption1ButtonText.text = "Resist"
                    upgradesOption1ButtonStat1.text = "+1 Max Health"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Fast":
                    upgradesOption1ButtonText.text = "Fast"
                    upgradesOption1ButtonStat1.text = "+10% Velocity"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Dextrous":
                    upgradesOption1ButtonText.text = "Dextrous"
                    upgradesOption1ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Extend":
                    upgradesOption1ButtonText.text = "Extend"
                    upgradesOption1ButtonStat1.text = "+10% Range"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Honed":
                    upgradesOption1ButtonText.text = "Honed"
                    upgradesOption1ButtonStat1.text = "+1 Damage"
                    upgradesOption1ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Deft":
                    upgradesOption1ButtonText.text = "Deft"
                    upgradesOption1ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Broaden":
                    upgradesOption1ButtonText.text = "Broaden"
                    upgradesOption1ButtonStat1.text = "+1 Max Health"
                    upgradesOption1ButtonStat2.text = "+10% Range"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Boost":
                    upgradesOption1ButtonText.text = "Boost"
                    upgradesOption1ButtonStat1.text = "+1 Max Health"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Blacksmith":
                    upgradesOption1ButtonText.text = "Blacksmith"
                    upgradesOption1ButtonStat1.text = "+1 Damage"
                    upgradesOption1ButtonStat2.text = "+10% Range"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Stoic":
                    upgradesOption1ButtonText.text = "Stoic"
                    upgradesOption1ButtonStat1.text = "+2 Max Health"
                    upgradesOption1ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Temper":
                    upgradesOption1ButtonText.text = "Temper"
                    upgradesOption1ButtonStat1.text = "+2 Damage"
                    upgradesOption1ButtonStat2.text = "-1 Max Health"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Inflate":
                    upgradesOption1ButtonText.text = "Inflate"
                    upgradesOption1ButtonStat1.text = "+20% Range"
                    upgradesOption1ButtonStat2.text = "-10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Exercise":
                    upgradesOption1ButtonText.text = "Exercise"
                    upgradesOption1ButtonStat1.text = "+20% Velocity"
                    upgradesOption1ButtonStat2.text = "-10% Range"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Unruly":
                    upgradesOption1ButtonText.text = "Unruly"
                    upgradesOption1ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption1ButtonStat2.text = "-1 Damage"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Toughen":
                    upgradesOption1ButtonText.text = "Toughen"
                    upgradesOption1ButtonStat1.text = "+2 Max Health"
                    upgradesOption1ButtonStat2.text = "+1 Damage"
                    upgradesOption1ButtonStat3.text = "-10% Velocity"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Speedier":
                    upgradesOption1ButtonText.text = "Speedier"
                    upgradesOption1ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = "-10% Range"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Embiggen":
                    upgradesOption1ButtonText.text = "Embiggen"
                    upgradesOption1ButtonStat1.text = "+20% Range"
                    upgradesOption1ButtonStat2.text = "+1 Max Health"
                    upgradesOption1ButtonStat3.text = "-1 Damage"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Smite":
                    upgradesOption1ButtonText.text = "Smite"
                    upgradesOption1ButtonStat1.text = "+3 Damage"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Fortify":
                    upgradesOption1ButtonText.text = "Fortify"
                    upgradesOption1ButtonStat1.text = "+3 Max Health"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Rush":
                    upgradesOption1ButtonText.text = "Rush"
                    upgradesOption1ButtonStat1.text = "+30% Velocity"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Lash":
                    upgradesOption1ButtonText.text = "Lash"
                    upgradesOption1ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Bolster":
                    upgradesOption1ButtonText.text = "Bolster"
                    upgradesOption1ButtonStat1.text = "+30% Range"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Dash":
                    upgradesOption1ButtonText.text = "Dash"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+10% Velocity"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Saviour":
                    upgradesOption1ButtonText.text = "Saviour"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+2 Max Health"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Rampage":
                    upgradesOption1ButtonText.text = "Rampage"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+1 Damage"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Burst":
                    upgradesOption1ButtonText.text = "Burst"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Pulse":
                    upgradesOption1ButtonText.text = "Pulse"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = "+10% Range"
                    upgradesOption1ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade1] == "Super":
                    upgradesOption1ButtonText.text = "Super"
                    upgradesOption1ButtonStat1.text = "+Ability"
                    upgradesOption1ButtonStat2.text = ""
                    upgradesOption1ButtonStat3.text = ""
                upgradesOption1ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonText.text)[0],smallFont.size(upgradesOption1ButtonText.text)[1]))
                upgradesOption1ButtonText.rect = upgradesOption1ButtonText.surf.get_rect(center = (upgradesOption1ButtonText.pos[0], upgradesOption1ButtonText.pos[1]))
                upgradesOption1ButtonText.surf = smallFont.render(upgradesOption1ButtonText.text, True, upgradesOption1ButtonText.colour)
                    
                upgradesOption1ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonStat1.text)[0],smallFont.size(upgradesOption1ButtonStat1.text)[1]))
                upgradesOption1ButtonStat1.rect = upgradesOption1ButtonStat1.surf.get_rect(center = (upgradesOption1ButtonStat1.pos[0], upgradesOption1ButtonStat1.pos[1]))
                upgradesOption1ButtonStat1.surf = smallFont.render(upgradesOption1ButtonStat1.text, True, upgradesOption1ButtonStat1.colour)
                    
                upgradesOption1ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonStat2.text)[0],smallFont.size(upgradesOption1ButtonStat2.text)[1]))
                upgradesOption1ButtonStat2.rect = upgradesOption1ButtonStat2.surf.get_rect(center = (upgradesOption1ButtonStat2.pos[0], upgradesOption1ButtonStat2.pos[1]))
                upgradesOption1ButtonStat2.surf = smallFont.render(upgradesOption1ButtonStat2.text, True, upgradesOption1ButtonStat2.colour)
                    
                upgradesOption1ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption1ButtonStat3.text)[0],smallFont.size(upgradesOption1ButtonStat3.text)[1]))
                upgradesOption1ButtonStat3.rect = upgradesOption1ButtonStat3.surf.get_rect(center = (upgradesOption1ButtonStat3.pos[0], upgradesOption1ButtonStat3.pos[1]))
                upgradesOption1ButtonStat3.surf = smallFont.render(upgradesOption1ButtonStat3.text, True, upgradesOption1ButtonStat3.colour)

    #=======================================================================================================================================================================================================
                
                if masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Sharpen":
                    upgradesOption2ButtonText.text = "Sharpen"
                    upgradesOption2ButtonStat1.text = "+1 Damage"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Resist":
                    upgradesOption2ButtonText.text = "Resist"
                    upgradesOption2ButtonStat1.text = "+1 Max Health"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Fast":
                    upgradesOption2ButtonText.text = "Fast"
                    upgradesOption2ButtonStat1.text = "+10% Velocity"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Dextrous":
                    upgradesOption2ButtonText.text = "Dextrous"
                    upgradesOption2ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Extend":
                    upgradesOption2ButtonText.text = "Extend"
                    upgradesOption2ButtonStat1.text = "+10% Range"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Honed":
                    upgradesOption2ButtonText.text = "Honed"
                    upgradesOption2ButtonStat1.text = "+1 Damage"
                    upgradesOption2ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Deft":
                    upgradesOption2ButtonText.text = "Deft"
                    upgradesOption2ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Broaden":
                    upgradesOption2ButtonText.text = "Broaden"
                    upgradesOption2ButtonStat1.text = "+1 Max Health"
                    upgradesOption2ButtonStat2.text = "+10% Range"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Boost":
                    upgradesOption2ButtonText.text = "Boost"
                    upgradesOption2ButtonStat1.text = "+1 Max Health"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Blacksmith":
                    upgradesOption2ButtonText.text = "Blacksmith"
                    upgradesOption2ButtonStat1.text = "+1 Damage"
                    upgradesOption2ButtonStat2.text = "+10% Range"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Stoic":
                    upgradesOption2ButtonText.text = "Stoic"
                    upgradesOption2ButtonStat1.text = "+2 Max Health"
                    upgradesOption2ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Temper":
                    upgradesOption2ButtonText.text = "Temper"
                    upgradesOption2ButtonStat1.text = "+2 Damage"
                    upgradesOption2ButtonStat2.text = "-1 Max Health"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Inflate":
                    upgradesOption2ButtonText.text = "Inflate"
                    upgradesOption2ButtonStat1.text = "+20% Range"
                    upgradesOption2ButtonStat2.text = "-10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Exercise":
                    upgradesOption2ButtonText.text = "Exercise"
                    upgradesOption2ButtonStat1.text = "+20% Velocity"
                    upgradesOption2ButtonStat2.text = "-10% Range"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Unruly":
                    upgradesOption2ButtonText.text = "Unruly"
                    upgradesOption2ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption2ButtonStat2.text = "-1 Damage"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Toughen":
                    upgradesOption2ButtonText.text = "Toughen"
                    upgradesOption2ButtonStat1.text = "+2 Max Health"
                    upgradesOption2ButtonStat2.text = "+1 Damage"
                    upgradesOption2ButtonStat3.text = "-10% Velocity"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Speedier":
                    upgradesOption2ButtonText.text = "Speedier"
                    upgradesOption2ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = "-10% Range"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Embiggen":
                    upgradesOption2ButtonText.text = "Embiggen"
                    upgradesOption2ButtonStat1.text = "+20% Range"
                    upgradesOption2ButtonStat2.text = "+1 Max Health"
                    upgradesOption2ButtonStat3.text = "-1 Damage"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Smite":
                    upgradesOption2ButtonText.text = "Smite"
                    upgradesOption2ButtonStat1.text = "+3 Damage"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Fortify":
                    upgradesOption2ButtonText.text = "Fortify"
                    upgradesOption2ButtonStat1.text = "+3 Max Health"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Rush":
                    upgradesOption2ButtonText.text = "Rush"
                    upgradesOption2ButtonStat1.text = "+30% Velocity"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Lash":
                    upgradesOption2ButtonText.text = "Lash"
                    upgradesOption2ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Bolster":
                    upgradesOption2ButtonText.text = "Bolster"
                    upgradesOption2ButtonStat1.text = "+30% Range"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Dash":
                    upgradesOption2ButtonText.text = "Dash"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+10% Velocity"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Saviour":
                    upgradesOption2ButtonText.text = "Saviour"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+2 Max Health"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Rampage":
                    upgradesOption2ButtonText.text = "Rampage"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+1 Damage"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Burst":
                    upgradesOption2ButtonText.text = "Burst"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Pulse":
                    upgradesOption2ButtonText.text = "Pulse"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = "+10% Range"
                    upgradesOption2ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade2] == "Super":
                    upgradesOption2ButtonText.text = "Super"
                    upgradesOption2ButtonStat1.text = "+Ability"
                    upgradesOption2ButtonStat2.text = ""
                    upgradesOption2ButtonStat3.text = ""
                upgradesOption2ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonText.text)[0],smallFont.size(upgradesOption2ButtonText.text)[1]))
                upgradesOption2ButtonText.rect = upgradesOption2ButtonText.surf.get_rect(center = (upgradesOption2ButtonText.pos[0], upgradesOption2ButtonText.pos[1]))
                upgradesOption2ButtonText.surf = smallFont.render(upgradesOption2ButtonText.text, True, upgradesOption2ButtonText.colour)

                upgradesOption2ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonStat1.text)[0],smallFont.size(upgradesOption2ButtonStat1.text)[1]))
                upgradesOption2ButtonStat1.rect = upgradesOption2ButtonStat1.surf.get_rect(center = (upgradesOption2ButtonStat1.pos[0], upgradesOption2ButtonStat1.pos[1]))
                upgradesOption2ButtonStat1.surf = smallFont.render(upgradesOption2ButtonStat1.text, True, upgradesOption2ButtonStat1.colour)

                upgradesOption2ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonStat2.text)[0],smallFont.size(upgradesOption2ButtonStat2.text)[1]))
                upgradesOption2ButtonStat2.rect = upgradesOption2ButtonStat2.surf.get_rect(center = (upgradesOption2ButtonStat2.pos[0], upgradesOption2ButtonStat2.pos[1]))
                upgradesOption2ButtonStat2.surf = smallFont.render(upgradesOption2ButtonStat2.text, True, upgradesOption2ButtonStat2.colour)

                upgradesOption2ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption2ButtonStat3.text)[0],smallFont.size(upgradesOption2ButtonStat3.text)[1]))
                upgradesOption2ButtonStat3.rect = upgradesOption2ButtonStat3.surf.get_rect(center = (upgradesOption2ButtonStat3.pos[0], upgradesOption2ButtonStat3.pos[1]))
                upgradesOption2ButtonStat3.surf = smallFont.render(upgradesOption2ButtonStat3.text, True, upgradesOption2ButtonStat3.colour)

    #=================================================================================================================================================================================

                if masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Sharpen":
                    upgradesOption3ButtonText.text = "Sharpen"
                    upgradesOption3ButtonStat1.text = "+1 Damage"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Resist":
                    upgradesOption3ButtonText.text = "Resist"
                    upgradesOption3ButtonStat1.text = "+1 Max Health"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Fast":
                    upgradesOption3ButtonText.text = "Fast"
                    upgradesOption3ButtonStat1.text = "+10% Velocity"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Dextrous":
                    upgradesOption3ButtonText.text = "Dextrous"
                    upgradesOption3ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Extend":
                    upgradesOption3ButtonText.text = "Extend"
                    upgradesOption3ButtonStat1.text = "+10% Range"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Honed":
                    upgradesOption3ButtonText.text = "Honed"
                    upgradesOption3ButtonStat1.text = "+1 Damage"
                    upgradesOption3ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Deft":
                    upgradesOption3ButtonText.text = "Deft"
                    upgradesOption3ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Broaden":
                    upgradesOption3ButtonText.text = "Broaden"
                    upgradesOption3ButtonStat1.text = "+1 Max Health"
                    upgradesOption3ButtonStat2.text = "+10% Range"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Boost":
                    upgradesOption3ButtonText.text = "Boost"
                    upgradesOption3ButtonStat1.text = "+1 Max Health"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Blacksmith":
                    upgradesOption3ButtonText.text = "Blacksmith"
                    upgradesOption3ButtonStat1.text = "+1 Damage"
                    upgradesOption3ButtonStat2.text = "+10% Range"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Stoic":
                    upgradesOption3ButtonText.text = "Stoic"
                    upgradesOption3ButtonStat1.text = "+2 Max Health"
                    upgradesOption3ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Temper":
                    upgradesOption3ButtonText.text = "Temper"
                    upgradesOption3ButtonStat1.text = "+2 Damage"
                    upgradesOption3ButtonStat2.text = "-1 Max Health"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Inflate":
                    upgradesOption3ButtonText.text = "Inflate"
                    upgradesOption3ButtonStat1.text = "+20% Range"
                    upgradesOption3ButtonStat2.text = "-10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Exercise":
                    upgradesOption3ButtonText.text = "Exercise"
                    upgradesOption3ButtonStat1.text = "+20% Velocity"
                    upgradesOption3ButtonStat2.text = "-10% Range"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Unruly":
                    upgradesOption3ButtonText.text = "Unruly"
                    upgradesOption3ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption3ButtonStat2.text = "-1 Damage"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Toughen":
                    upgradesOption3ButtonText.text = "Toughen"
                    upgradesOption3ButtonStat1.text = "+2 Max Health"
                    upgradesOption3ButtonStat2.text = "+1 Damage"
                    upgradesOption3ButtonStat3.text = "-10% Velocity"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Speedier":
                    upgradesOption3ButtonText.text = "Speedier"
                    upgradesOption3ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = "-10% Range"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Embiggen":
                    upgradesOption3ButtonText.text = "Embiggen"
                    upgradesOption3ButtonStat1.text = "+20% Range"
                    upgradesOption3ButtonStat2.text = "+1 Max Health"
                    upgradesOption3ButtonStat3.text = "-1 Damage"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Smite":
                    upgradesOption3ButtonText.text = "Smite"
                    upgradesOption3ButtonStat1.text = "+3 Damage"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Fortify":
                    upgradesOption3ButtonText.text = "Fortify"
                    upgradesOption3ButtonStat1.text = "+3 Max Health"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Rush":
                    upgradesOption3ButtonText.text = "Rush"
                    upgradesOption3ButtonStat1.text = "+30% Velocity"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Lash":
                    upgradesOption3ButtonText.text = "Lash"
                    upgradesOption3ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Bolster":
                    upgradesOption3ButtonText.text = "Bolster"
                    upgradesOption3ButtonStat1.text = "+30% Range"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Dash":
                    upgradesOption3ButtonText.text = "Dash"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+10% Velocity"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Saviour":
                    upgradesOption3ButtonText.text = "Saviour"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+2 Max Health"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Rampage":
                    upgradesOption3ButtonText.text = "Rampage"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+1 Damage"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Burst":
                    upgradesOption3ButtonText.text = "Burst"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Pulse":
                    upgradesOption3ButtonText.text = "Pulse"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = "+10% Range"
                    upgradesOption3ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade3] == "Super":
                    upgradesOption3ButtonText.text = "Super"
                    upgradesOption3ButtonStat1.text = "+Ability"
                    upgradesOption3ButtonStat2.text = ""
                    upgradesOption3ButtonStat3.text = ""
                upgradesOption3ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonText.text)[0],smallFont.size(upgradesOption3ButtonText.text)[1]))
                upgradesOption3ButtonText.rect = upgradesOption3ButtonText.surf.get_rect(center = (upgradesOption3ButtonText.pos[0], upgradesOption3ButtonText.pos[1]))
                upgradesOption3ButtonText.surf = smallFont.render(upgradesOption3ButtonText.text, True, upgradesOption3ButtonText.colour)
                    
                upgradesOption3ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonStat1.text)[0],smallFont.size(upgradesOption3ButtonStat1.text)[1]))
                upgradesOption3ButtonStat1.rect = upgradesOption3ButtonStat1.surf.get_rect(center = (upgradesOption3ButtonStat1.pos[0], upgradesOption3ButtonStat1.pos[1]))
                upgradesOption3ButtonStat1.surf = smallFont.render(upgradesOption3ButtonStat1.text, True, upgradesOption3ButtonStat1.colour)
                    
                upgradesOption3ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonStat2.text)[0],smallFont.size(upgradesOption3ButtonStat2.text)[1]))
                upgradesOption3ButtonStat2.rect = upgradesOption3ButtonStat2.surf.get_rect(center = (upgradesOption3ButtonStat2.pos[0], upgradesOption3ButtonStat2.pos[1]))
                upgradesOption3ButtonStat2.surf = smallFont.render(upgradesOption3ButtonStat2.text, True, upgradesOption3ButtonStat2.colour)
                    
                upgradesOption3ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption3ButtonStat3.text)[0],smallFont.size(upgradesOption3ButtonStat3.text)[1]))
                upgradesOption3ButtonStat3.rect = upgradesOption3ButtonStat3.surf.get_rect(center = (upgradesOption3ButtonStat3.pos[0], upgradesOption3ButtonStat3.pos[1]))
                upgradesOption3ButtonStat3.surf = smallFont.render(upgradesOption3ButtonStat3.text, True, upgradesOption3ButtonStat3.colour)

    #=====================================================================================================================================================================================

                if masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Sharpen":
                    upgradesOption4ButtonText.text = "Sharpen"
                    upgradesOption4ButtonStat1.text = "+1 Damage"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Resist":
                    upgradesOption4ButtonText.text = "Resist"
                    upgradesOption4ButtonStat1.text = "+1 Max Health"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Fast":
                    upgradesOption4ButtonText.text = "Fast"
                    upgradesOption4ButtonStat1.text = "+10% Velocity"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Dextrous":
                    upgradesOption4ButtonText.text = "Dextrous"
                    upgradesOption4ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Extend":
                    upgradesOption4ButtonText.text = "Extend"
                    upgradesOption4ButtonStat1.text = "+10% Range"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Honed":
                    upgradesOption4ButtonText.text = "Honed"
                    upgradesOption4ButtonStat1.text = "+1 Damage"
                    upgradesOption4ButtonStat2.text = "+10% Hit Speed"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Deft":
                    upgradesOption4ButtonText.text = "Deft"
                    upgradesOption4ButtonStat1.text = "+10% Hit Speed"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Broaden":
                    upgradesOption4ButtonText.text = "Broaden"
                    upgradesOption4ButtonStat1.text = "+1 Max Health"
                    upgradesOption4ButtonStat2.text = "+10% Range"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Boost":
                    upgradesOption4ButtonText.text = "Boost"
                    upgradesOption4ButtonStat1.text = "+1 Max Health"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Blacksmith":
                    upgradesOption4ButtonText.text = "Blacksmith"
                    upgradesOption4ButtonStat1.text = "+1 Damage"
                    upgradesOption4ButtonStat2.text = "+10% Range"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Stoic":
                    upgradesOption4ButtonText.text = "Stoic"
                    upgradesOption4ButtonStat1.text = "+2 Max Health"
                    upgradesOption4ButtonStat2.text = "-10% Hit Speed"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Temper":
                    upgradesOption4ButtonText.text = "Temper"
                    upgradesOption4ButtonStat1.text = "+2 Damage"
                    upgradesOption4ButtonStat2.text = "-1 Max Health"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Inflate":
                    upgradesOption4ButtonText.text = "Inflate"
                    upgradesOption4ButtonStat1.text = "+20% Range"
                    upgradesOption4ButtonStat2.text = "-10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Exercise":
                    upgradesOption4ButtonText.text = "Exercise"
                    upgradesOption4ButtonStat1.text = "+20% Velocity"
                    upgradesOption4ButtonStat2.text = "-10% Range"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Unruly":
                    upgradesOption4ButtonText.text = "Unruly"
                    upgradesOption4ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption4ButtonStat2.text = "-1 Damage"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Toughen":
                    upgradesOption4ButtonText.text = "Toughen"
                    upgradesOption4ButtonStat1.text = "+2 Max Health"
                    upgradesOption4ButtonStat2.text = "+1 Damage"
                    upgradesOption4ButtonStat3.text = "-10% Velocity"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Speedier":
                    upgradesOption4ButtonText.text = "Speedier"
                    upgradesOption4ButtonStat1.text = "+20% Hit Speed"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = "-10% Range"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Embiggen":
                    upgradesOption4ButtonText.text = "Embiggen"
                    upgradesOption4ButtonStat1.text = "+20% Range"
                    upgradesOption4ButtonStat2.text = "+1 Max Health"
                    upgradesOption4ButtonStat3.text = "-1 Damage"
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Smite":
                    upgradesOption4ButtonText.text = "Smite"
                    upgradesOption4ButtonStat1.text = "+3 Damage"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Fortify":
                    upgradesOption4ButtonText.text = "Fortify"
                    upgradesOption4ButtonStat1.text = "+3 Max Health"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Rush":
                    upgradesOption4ButtonText.text = "Rush"
                    upgradesOption4ButtonStat1.text = "+30% Velocity"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Lash":
                    upgradesOption4ButtonText.text = "Lash"
                    upgradesOption4ButtonStat1.text = "+30% Hit Speed"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Bolster":
                    upgradesOption4ButtonText.text = "Bolster"
                    upgradesOption4ButtonStat1.text = "+30% Range"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Dash":
                    upgradesOption4ButtonText.text = "Dash"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+10% Velocity"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Saviour":
                    upgradesOption4ButtonText.text = "Saviour"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+2 Max Health"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Rampage":
                    upgradesOption4ButtonText.text = "Rampage"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+1 Damage"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Burst":
                    upgradesOption4ButtonText.text = "Burst"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+20% Hit Speed"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Pulse":
                    upgradesOption4ButtonText.text = "Pulse"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = "+10% Range"
                    upgradesOption4ButtonStat3.text = ""
                elif masterUpgradeList[floorReward[currentFloor]][randomUpgrade4] == "Super":
                    upgradesOption4ButtonText.text = "Super"
                    upgradesOption4ButtonStat1.text = "+Ability"
                    upgradesOption4ButtonStat2.text = ""
                    upgradesOption4ButtonStat3.text = ""
                upgradesOption4ButtonText.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonText.text)[0], smallFont.size(upgradesOption4ButtonText.text)[1]))
                upgradesOption4ButtonText.rect = upgradesOption4ButtonText.surf.get_rect(center=(upgradesOption4ButtonText.pos[0], upgradesOption4ButtonText.pos[1]))
                upgradesOption4ButtonText.surf = smallFont.render(upgradesOption4ButtonText.text, True, upgradesOption4ButtonText.colour)

                upgradesOption4ButtonStat1.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonStat1.text)[0], smallFont.size(upgradesOption4ButtonStat1.text)[1]))
                upgradesOption4ButtonStat1.rect = upgradesOption4ButtonStat1.surf.get_rect(center=(upgradesOption4ButtonStat1.pos[0], upgradesOption4ButtonStat1.pos[1]))
                upgradesOption4ButtonStat1.surf = smallFont.render(upgradesOption4ButtonStat1.text, True, upgradesOption4ButtonStat1.colour)

                upgradesOption4ButtonStat2.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonStat2.text)[0], smallFont.size(upgradesOption4ButtonStat2.text)[1]))
                upgradesOption4ButtonStat2.rect = upgradesOption4ButtonStat2.surf.get_rect(center=(upgradesOption4ButtonStat2.pos[0], upgradesOption4ButtonStat2.pos[1]))
                upgradesOption4ButtonStat2.surf = smallFont.render(upgradesOption4ButtonStat2.text, True, upgradesOption4ButtonStat2.colour)

                upgradesOption4ButtonStat3.surf = pygame.Surface((smallFont.size(upgradesOption4ButtonStat3.text)[0], smallFont.size(upgradesOption4ButtonStat3.text)[1]))
                upgradesOption4ButtonStat3.rect = upgradesOption4ButtonStat3.surf.get_rect(center=(upgradesOption4ButtonStat3.pos[0], upgradesOption4ButtonStat3.pos[1]))
                upgradesOption4ButtonStat3.surf = smallFont.render(upgradesOption4ButtonStat3.text, True, upgradesOption4ButtonStat3.colour)
#==================================================================================================================================================================================================            

            for entity in upgradeSelectGroup :
                displaySurface.blit(entity.surf, entity.rect)
            currentMenu = "Upgrades"
        
       #I have my code divided into event and state checks because they're run different amounts of times
       #The state checks are run every frame and check for buttons clicked or mouse postions
       #The Event checks only are run once and then only again when needed
       #They provide the more intensive visual code like displaying every object and clearing the screen
        
       #Menu State Checks 
        elif currentMenu == "Title Screen" :
            for button in titleScreenButtonsGroup :
                button.clicked(event)
                
        elif currentMenu == "Save Select" :
            
            #if choice == True :
            #    if saveSelectCopyButton.clicked(event) == True :
            #        choice = False                                                
            #    elif saveSelectDeleteButton.clicked(event) == True :
            #        choice = False
            if saveSelectFile1.clicked(event) == True :
                saveFileSelectedButton = "File 1"
                pygame.event.post(pygame.event.Event(SAVESELECT))
            elif saveSelectFile2.clicked(event) == True :
                saveFileSelectedButton = "File 2"
                pygame.event.post(pygame.event.Event(SAVESELECT))
            elif saveSelectFile3.clicked(event) == True :
                saveFileSelectedButton = "File 3"
                pygame.event.post(pygame.event.Event(SAVESELECT))
            elif (saveFileSelectedButton != "") :
                if saveSelectConfirmButton.clicked(event) :
                    if saveFileSelectedButton == "File 1" :
                        readCSV("GameFile1.csv")
                    elif saveFileSelectedButton == "File 2" :
                        readCSV("GameFile2.csv")
                    elif saveFileSelectedButton == "File 3" :
                        readCSV("GameFile3.csv")
                        
                    saveFileSelectedButton = ""
            #else:
            #    drawOverwriteDecision()
            #    if yesButton.clicked(event) == True :
            #        choice = True
            #        pygame.event.post(pygame.event.Event(SAVESELECT))
            #    elif noButton.clicked(event) == True :
            #        choice = True
            #        pygame.event.post(pygame.event.Event(SAVESELECT))
                
        
        elif currentMenu == "Main Menu" :
            for button in mainMenuButtonsGroup:
                button.clicked(event)
            if mainMenuQuitButton.clicked(event) :
                showQuitMenu = True
                
        elif currentMenu == "Adventure Mode Select" :
            for button in adModeButtonsGroup:
                button.clicked(event)
            if adModeDungeon1.clicked(event) :
                if currentDungeon == 1 :
                    pass
                else:
                    currentFloor = 0
                    player.damage = 1
                    player.Dspeed = 100
                    player.Mspeed = 100
                    player.range = 100
                    player.maxHealth = 3
                    player.health = 3
                    currentDungeon = 1
                    gameMode = "adMode"
                    canDash = True
                    canSaviour = False
                    saviourUsed = False
                    canRampage = False
                    canBurst = False
                    canPulse = False
                    canSuper = False
                    dungeon1Upgrades = [""]
                    dungeon2Upgrades = [""]
                    dungeon3Upgrades = [""]
                    dungeon4Upgrades = [""]
                    dungeon5Upgrades = [""]
            elif adModeDungeon2.clicked(event) :
                currentFloor = 3
                player.damage = 1
                player.Dspeed = 100
                player.Mspeed = 100
                player.range = 100
                player.maxHealth = 3
                player.health = 3
                currentDungeon = 2
                gameMode = "adMode"
                canDash = True
                canSaviour = False
                saviourUsed = False
                canRampage = False
                canBurst = False
                canPulse = False
                canSuper = False
                dungeon1Upgrades = [""]
                dungeon2Upgrades = [""]
                dungeon3Upgrades = [""]
                dungeon4Upgrades = [""]
                dungeon5Upgrades = [""]
            elif adModeDungeon3.clicked(event) :
                currentFloor = 10
                player.damage = 1
                player.Dspeed = 100
                player.Mspeed = 100
                player.range = 100
                player.maxHealth = 3
                player.health = 3
                currentDungeon = 3
                gameMode = "adMode"
                canDash = True
                canSaviour = False
                saviourUsed = False
                canRampage = False
                canBurst = False
                canPulse = False
                canSuper = False
                dungeon1Upgrades = [""]
                dungeon2Upgrades = [""]
                dungeon3Upgrades = [""]
                dungeon4Upgrades = [""]
                dungeon5Upgrades = [""]
            elif adModeDungeon4.clicked(event) :
                currentFloor = 25
                player.damage = 1
                player.Dspeed = 100
                player.Mspeed = 100
                player.range = 100
                player.maxHealth = 3
                player.health = 3
                currentDungeon = 4
                gameMode = "adMode"
                canDash = True
                canSaviour = False
                saviourUsed = False
                canRampage = False
                canBurst = False
                canPulse = False
                canSuper = False
                dungeon1Upgrades = [""]
                dungeon2Upgrades = [""]
                dungeon3Upgrades = [""]
                dungeon4Upgrades = [""]
                dungeon5Upgrades = [""]
            elif adModeDungeon5.clicked(event) :
                currentFloor = 40
                player.damage = 1
                player.Dspeed = 100
                player.Mspeed = 100
                player.range = 100
                player.maxHealth = 3
                player.health = 3
                currentDungeon = 5
                gameMode = "adMode"
                canDash = True
                canSaviour = False
                saviourUsed = False
                canRampage = False
                canBurst = False
                canPulse = False
                canSuper = False
                dungeon1Upgrades = [""]
                dungeon2Upgrades = [""]
                dungeon3Upgrades = [""]
                dungeon4Upgrades = [""]
                dungeon5Upgrades = [""]
                
            if adModeWeaponButton.clicked(event) == True :
                if adModeWeaponButton.filePath == "sword new.png":
                    adModeWeaponButton.filePath = "ShieldTransBorderResized.png"
                    endModeWeaponButton.filePath = "ShieldTransBorderResized.png"
                elif adModeWeaponButton.filePath == "ShieldTransBorderResized.png":
                    adModeWeaponButton.filePath = "sword new.png"
                    endModeWeaponButton.filePath = "sword new.png"
                adModeWeaponButton.surf = pygame.image.load(adModeWeaponButton.filePath)
                endModeWeaponButton.surf = pygame.image.load(endModeWeaponButton.filePath)
                pygame.event.post(pygame.event.Event(ADMODESELECT))
                
            if (event.type == pygame.MOUSEBUTTONDOWN) and (displaySurface.get_at(pygame.mouse.get_pos()) == (0,200,0)) and (adModeDungeon1.rect.x != 52) :
                for entity in adModeSlidingMenuGroup :
                    entity.rect.x += 225
                    entity.pos[0] += 225
                pygame.event.post(pygame.event.Event(ADMODESELECT))
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (displaySurface.get_at(pygame.mouse.get_pos()) == (0,201,0)) and (adModeDungeon5.rect.x != 727 ) :
                for entity in adModeSlidingMenuGroup :
                    entity.rect.x += -225
                    entity.pos[0] += -225
                pygame.event.post(pygame.event.Event(ADMODESELECT))

                
        elif currentMenu == "Endless Mode Select" :
            for button in endModeButtonsGroup:
                button.clicked(event)
            if endModePlayButton.clicked(event) :
                gameMode = "endMode"
                currentFloor = 0
                player.maxHealth = 3
                player.health = 3
                player.damage = 1
                player.Dspeed = 100
                player.Mspeed = 100
                player.range = 100
                canDash = True
                canSaviour = False
                saviourUsed = False
                canRampage = False
                canBurst = False
                canPulse = False
                canSuper = False
            if endModeWeaponButton.clicked(event) == True :
                if adModeWeaponButton.filePath == "sword new.png":
                    adModeWeaponButton.filePath = "ShieldTransBorderResized.png"
                    endModeWeaponButton.filePath = "ShieldTransBorderResized.png"
                elif adModeWeaponButton.filePath == "ShieldTransBorderResized.png":
                    adModeWeaponButton.filePath = "sword new.png"
                    endModeWeaponButton.filePath = "sword new.png"
                adModeWeaponButton.surf = pygame.image.load(adModeWeaponButton.filePath)
                endModeWeaponButton.surf = pygame.image.load(endModeWeaponButton.filePath)
                pygame.event.post(pygame.event.Event(ENDMODESELECT))
                
                
        elif currentMenu == "Settings" :
            for button in settingsButtonsGroup :
                button.clicked(event)
            if settingsSoundButton.clicked(event) :
                if settingsSoundButtonText.text == "Game Volume: Low":
                    settingsSoundButtonText.text = "Game Volume: Medium"
                   
                elif settingsSoundButtonText.text == "Game Volume: Medium":
                    settingsSoundButtonText.text = "Game Volume: High"
                   
                elif settingsSoundButtonText.text == "Game Volume: High":
                    settingsSoundButtonText.text = "Game Volume: Low"
                   
                settingsSoundButtonText.surf = standardFont.render(settingsSoundButtonText.text, True, settingsSoundButtonText.colour)
                pygame.event.post(pygame.event.Event(SETTINGS))
            
            elif settingsGraphicsButton.clicked(event) :
                if settingsGraphicsButtonText.text == "Game Graphics: Low":
                    settingsGraphicsButtonText.text = "Game Graphics: Medium"
                   
                elif settingsGraphicsButtonText.text == "Game Graphics: Medium":
                    settingsGraphicsButtonText.text = "Game Graphics: High"
                    
                elif settingsGraphicsButtonText.text == "Game Graphics: High":
                    settingsGraphicsButtonText.text = "Game Graphics: Low"

                settingsGraphicsButtonText.surf = standardFont.render(settingsGraphicsButtonText.text, True, settingsGraphicsButtonText.colour)
                pygame.event.post(pygame.event.Event(SETTINGS))
                
            elif settingsSaveButton.clicked(event):
                gameData[4][0] = settingsSoundButtonText.text
                gameData[4][1] = settingsGraphicsButtonText.text 
                writeCSV(currentFile)
                
        elif currentMenu == "Controls":
            if controlsBackButton.clicked(event):
                controlsSelectedButton = ""
            elif controlsAttackButton.clicked(event) :
                controlsSelectedButton = "Attack"
                pygame.event.post(pygame.event.Event(CONTROLS))
            elif controlsAction1Button.clicked(event) :
                controlsSelectedButton = "Action 1"
                pygame.event.post(pygame.event.Event(CONTROLS))
            elif controlsAction2Button.clicked(event) :
                controlsSelectedButton = "Action 2"
                pygame.event.post(pygame.event.Event(CONTROLS))
            elif controlsSaveButton.clicked(event) :
                gameData[5][0] = controlsAttackButtonText.text
                gameData[5][1] = controlsAction1ButtonText.text
                gameData[5][2] = controlsAction2ButtonText.text
                writeCSV(currentFile)
            #Coded in order of keyboard inputs then mouse inputs    
             #Coded in order of Attack then Action 1 then Action 2   
            elif (controlsSelectedButton == "Attack") and (event.type == pygame.KEYDOWN): #Checks for Keyboard Inputs
                if pygame.key.name(event.key) == "" or pygame.key.name(event.key) == "escape":
                    pass
                else:
                    if ((pygame.key.name(event.key)[0].upper() + pygame.key.name(event.key)[1:]) == controlsAction1ButtonText.text) or ((pygame.key.name(event.key)[0].upper() + pygame.key.name(event.key)[1:]) == controlsAction2ButtonText.text) :
                        pass
                    else:
                        playerAttackInput = event.key
                        controlsAttackButtonText.text = pygame.key.name(event.key)
                        controlsAttackButtonText.text = (controlsAttackButtonText.text[0]).upper() + controlsAttackButtonText.text[1:]
                        controlsAttackButtonText.surf = pygame.Surface((standardFont.size(controlsAttackButtonText.text)[0],standardFont.size(controlsAttackButtonText.text)[1]))
                        controlsAttackButtonText.rect = controlsAttackButtonText.surf.get_rect(center = (controlsAttackButtonText.pos[0], controlsAttackButtonText.pos[1]))
                        controlsAttackButtonText.surf = standardFont.render(controlsAttackButtonText.text, True, controlsAttackButtonText.colour)
                        pygame.event.post(pygame.event.Event(CONTROLS))
                        controlsSelectedButton = ""
                
            elif (controlsSelectedButton == "Action 1") and (event.type == pygame.KEYDOWN):
                if pygame.key.name(event.key) == "" or pygame.key.name(event.key) == "escape":
                    pass
                else:
                    if ((pygame.key.name(event.key)[0].upper() + pygame.key.name(event.key)[1:]) == controlsAttackButtonText.text) or ((pygame.key.name(event.key)[0].upper() + pygame.key.name(event.key)[1:]) == controlsAction2ButtonText.text) :
                        pass
                    else:
                        playerAction1Input = event.key
                        controlsAction1ButtonText.text = pygame.key.name(event.key)
                        controlsAction1ButtonText.text = (controlsAction1ButtonText.text[0]).upper() + controlsAction1ButtonText.text[1:]
                        controlsAction1ButtonText.surf = pygame.Surface((standardFont.size(controlsAction1ButtonText.text)[0],standardFont.size(controlsAction1ButtonText.text)[1]))
                        controlsAction1ButtonText.rect = controlsAction1ButtonText.surf.get_rect(center = (controlsAction1ButtonText.pos[0], controlsAction1ButtonText.pos[1]))
                        controlsAction1ButtonText.surf = standardFont.render(controlsAction1ButtonText.text, True, controlsAction1ButtonText.colour)
                        pygame.event.post(pygame.event.Event(CONTROLS))
                        controlsSelectedButton = ""
                
            elif (controlsSelectedButton == "Action 2") and (event.type == pygame.KEYDOWN):
                if pygame.key.name(event.key) == "" or pygame.key.name(event.key) == "escape":
                    pass
                else:
                    if ((pygame.key.name(event.key)[0].upper() + pygame.key.name(event.key)[1:]) == controlsAttackButtonText.text) or ((pygame.key.name(event.key)[0].upper() + pygame.key.name(event.key)[1:]) == controlsAction1ButtonText.text) :
                        pass
                    else:
                        playerAction2Input = event.key
                        controlsAction2ButtonText.text = pygame.key.name(event.key)
                        controlsAction2ButtonText.text = (controlsAction2ButtonText.text[0]).upper() + controlsAction2ButtonText.text[1:]
                        controlsAction2ButtonText.surf = pygame.Surface((standardFont.size(controlsAction2ButtonText.text)[0],standardFont.size(controlsAction2ButtonText.text)[1]))
                        controlsAction2ButtonText.rect = controlsAction2ButtonText.surf.get_rect(center = (controlsAction2ButtonText.pos[0], controlsAction2ButtonText.pos[1]))
                        controlsAction2ButtonText.surf = standardFont.render(controlsAction2ButtonText.text, True, controlsAction2ButtonText.colour)
                        pygame.event.post(pygame.event.Event(CONTROLS))
                        controlsSelectedButton = ""
                
                
                
            elif (controlsSelectedButton == "Attack") and (event.type == pygame.MOUSEBUTTONDOWN): #Checks for Mouse Button Inputs
                if event.button == 1 :
                    if (controlsAction1ButtonText.text != "Left click") and (controlsAction2ButtonText.text != "Left click"):
                        playerAttackInput = event.button
                        controlsAttackButtonText.text = "Left click"
                elif event.button == 2 :
                    if (controlsAction1ButtonText.text != "Scroll click") and (controlsAction2ButtonText.text != "Scroll click"):
                        controlsAttackButtonText.text = "Scroll click"
                        playerAttackInput = event.button
                elif event.button == 3 :
                    if (controlsAction1ButtonText.text != "Right click") and (controlsAction2ButtonText.text != "Right click"):
                        controlsAttackButtonText.text = "Right click"
                        playerAttackInput = event.button
                
                controlsAttackButtonText.surf = pygame.Surface((standardFont.size(controlsAttackButtonText.text)[0],standardFont.size(controlsAttackButtonText.text)[1]))
                controlsAttackButtonText.rect = controlsAttackButtonText.surf.get_rect(center = (controlsAttackButtonText.pos[0], controlsAttackButtonText.pos[1]))
                controlsAttackButtonText.surf = standardFont.render(controlsAttackButtonText.text, True, controlsAttackButtonText.colour)
                pygame.event.post(pygame.event.Event(CONTROLS))
                controlsSelectedButton = ""
                
            elif (controlsSelectedButton == "Action 1") and (event.type == pygame.MOUSEBUTTONDOWN):
                if event.button == 1 :
                    if (controlsAttackButtonText.text != "Left click") and (controlsAction2ButtonText.text != "Left click"):
                        controlsAction1ButtonText.text = "Left click"
                        playerAction1Input = event.button
                elif event.button == 2 :
                    if (controlsAttackButtonText.text != "Scroll click") and (controlsAction2ButtonText.text != "Scroll click"):
                        controlsAction1ButtonText.text = "Scroll click"
                        playerAction1Input = event.button
                elif event.button == 3 :
                    if (controlsAttackButtonText.text != "Right click") and (controlsAction2ButtonText.text != "Right click"):
                        controlsAction1ButtonText.text = "Right click"
                        playerAction1Input = event.button
                     
                controlsAction1ButtonText.surf = pygame.Surface((standardFont.size(controlsAction1ButtonText.text)[0],standardFont.size(controlsAction1ButtonText.text)[1]))
                controlsAction1ButtonText.rect = controlsAction1ButtonText.surf.get_rect(center = (controlsAction1ButtonText.pos[0], controlsAction1ButtonText.pos[1]))
                controlsAction1ButtonText.surf = standardFont.render(controlsAction1ButtonText.text, True, controlsAction1ButtonText.colour)
                pygame.event.post(pygame.event.Event(CONTROLS))
                controlsSelectedButton = ""
                
            elif (controlsSelectedButton == "Action 2") and (event.type == pygame.MOUSEBUTTONDOWN):
                if event.button == 1 :
                    if (controlsAttackButtonText.text != "Left click") and (controlsAction1ButtonText.text != "Left click"):
                        controlsAction2ButtonText.text = "Left click"
                        playerAction2Input = event.button
                elif event.button == 2 :
                    if (controlsAttackButtonText.text != "Scroll click") and (controlsAction1ButtonText.text != "Scroll click"):
                        controlsAction2ButtonText.text = "Scroll click"
                        playerAction2Input = event.button
                elif event.button == 3 :
                    if (controlsAttackButtonText.text != "Right click") and (controlsAction1ButtonText.text != "Right click"):
                        controlsAction2ButtonText.text = "Right click"
                        playerAction2Input = event.button
        
                controlsAction2ButtonText.surf = pygame.Surface((standardFont.size(controlsAction2ButtonText.text)[0],standardFont.size(controlsAction2ButtonText.text)[1]))
                controlsAction2ButtonText.rect = controlsAction2ButtonText.surf.get_rect(center = (controlsAction2ButtonText.pos[0], controlsAction2ButtonText.pos[1]))
                controlsAction2ButtonText.surf = standardFont.render(controlsAction2ButtonText.text, True, controlsAction2ButtonText.colour)
                pygame.event.post(pygame.event.Event(CONTROLS))
                controlsSelectedButton = ""     
         
         
        elif currentMenu == "Achievements" :
            if previousMenu == "Adventure Mode Select":
                achievementsBackButtonAdMode.clicked(event)
                
            elif previousMenu == "Endless Mode Select":
                achievementsBackButtonEndMode.clicked(event)
                
            if (event.type == pygame.MOUSEBUTTONDOWN) and (displaySurface.get_at(pygame.mouse.get_pos()) == (0,200,0)) and (achievementsTile1.rect.x != 30) :
                for entity in achievementsGroup :
                    entity.rect.x += 10000
                pygame.event.post(pygame.event.Event(ACHIEVEMENTS))
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (displaySurface.get_at(pygame.mouse.get_pos()) == (0,201,0)) and (achievementsTile43.rect.x != 30 ) :
                for entity in achievementsGroup :
                    entity.rect.x += -10000
                pygame.event.post(pygame.event.Event(ACHIEVEMENTS))
                
                
                
        elif currentMenu == "Gameplay" and showQuitMenu == False: #indented block for events only
            if (((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == playerAction1Input)) or (pygame.key.get_pressed()[playerAction1Input]) ) and (timeSinceAbility1 >= ability1Cooldown) and canDash:
                abilityDash()
                timeSinceAbility1 = 0
            if (pygame.key.get_pressed()[playerAction2Input]) and (timeSinceAbility2 >= ability2Cooldown) :
                if canRampage :
                    abilityRampage()
                if canBurst :
                    abilityBurst()
                if canPulse :
                    abilityPulse()
                timeSinceAbility2 = 0
            playerShield.sizeChange(player)
            playerSword.sizeChange(player)
            if player.health <= 0  and continueWithGameplay == False:
                if gameMode == "adMode":
                    if yesButton.clicked(event) :
                        resetLevel()
                        continueWithGameplay = True

                        if currentDungeon == 1:
                            dungeon1Upgrades = reinsertItems(dungeon1Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                            currentFloor -= 1
                        if currentDungeon == 2:
                            dungeon2Upgrades = reinsertItems(dungeon2Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                            currentFloor -= 1
                            if len(playerChosenUpgrades) != 0:
                                dungeon2Upgrades = reinsertItems(dungeon2Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                currentFloor -= 1 
                        if currentDungeon == 3:
                            dungeon3Upgrades = reinsertItems(dungeon3Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                            currentFloor -= 1 
                            if len(playerChosenUpgrades) != 0:
                                dungeon3Upgrades = reinsertItems(dungeon3Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                currentFloor -= 1 
                                if len(playerChosenUpgrades) != 0:
                                    dungeon3Upgrades = reinsertItems(dungeon3Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                    currentFloor -= 1 
                        if currentDungeon == 4:
                            dungeon4Upgrades = reinsertItems(dungeon4Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                            currentFloor -= 1 
                            if len(playerChosenUpgrades) != 0:
                                dungeon4Upgrades = reinsertItems(dungeon4Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                currentFloor -= 1 
                                if len(playerChosenUpgrades) != 0:
                                    dungeon4Upgrades = reinsertItems(dungeon4Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                    currentFloor -= 1 
                                    if len(playerChosenUpgrades) != 0:
                                        dungeon4Upgrades = reinsertItems(dungeon4Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                        currentFloor -= 1 
                        if currentDungeon == 5:
                            dungeon5Upgrades = reinsertItems(dungeon5Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                            currentFloor -= 1 
                            if len(playerChosenUpgrades) != 0:
                                dungeon5Upgrades = reinsertItems(dungeon5Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                currentFloor -= 1 
                                if len(playerChosenUpgrades) != 0:    
                                    dungeon5Upgrades = reinsertItems(dungeon5Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                    currentFloor -= 1 
                                    if len(playerChosenUpgrades) != 0:    
                                        dungeon5Upgrades = reinsertItems(dungeon5Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                        currentFloor -= 1 
                                        if len(playerChosenUpgrades) != 0:    
                                            dungeon5Upgrades = reinsertItems(dungeon5Upgrades,playerChosenUpgrades[len(playerChosenUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -1], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -2], playerDiscardedUpgrades[len(playerDiscardedUpgrades) -3])
                                            currentFloor -= 1
                                            
                        preRampageDamage = player.damage
                        preBurstDspeed = player.Dspeed
                        prePulseRange = player.range
                        pygame.event.post(pygame.event.Event(UPGRADES))    
                        deactivateRampage()
                        deactivateBurst()
                        deactivatePulse()
                    elif noButton.clicked(event) :
                        resetLevel()
                        pygame.event.post(pygame.event.Event(MAINMENU))
                        continueWithGameplay = True
                        deactivateRampage()
                        deactivateBurst()
                        deactivatePulse()
                elif gameMode == "endMode":
                    if centreNoButton.clicked(event) :
                        if currentFloor + (70 * loopsOfEndless) > int(endModeHighScoreDisplayValueText.text) :
                            endModeHighScoreDisplayValueText.text = str(currentFloor + (70 * loopsOfEndless))
                            endModeHighScoreDisplayValueText.surf = pygame.Surface((standardFont.size(endModeHighScoreDisplayValueText.text)[0],standardFont.size(endModeHighScoreDisplayValueText.text)[1]))
                            endModeHighScoreDisplayValueText.rect = endModeHighScoreDisplayValueText.surf.get_rect(center = (endModeHighScoreDisplayValueText.pos[0], endModeHighScoreDisplayValueText.pos[1]))
                            endModeHighScoreDisplayValueText.surf = standardFont.render(endModeHighScoreDisplayValueText.text, True, endModeHighScoreDisplayValueText.colour)
                            gameData[1][0] = str(currentFloor + (70 * loopsOfEndless))
                            writeCSV(currentFile)
                        resetLevel()
                        pygame.event.post(pygame.event.Event(MAINMENU))
                        continueWithGameplay = True
                        deactivateRampage()
                        deactivateBurst()
                        deactivatePulse()
            elif len(gameplayCollisionsGroup) == 1 and continueWithGameplay == False:
                if yesButton.clicked(event) :
                    deactivateShield()
                    resetLevel()
                    continueWithGameplay = True
                    pygame.event.post(pygame.event.Event(UPGRADES))
                    deactivateRampage()
                    deactivateBurst()
                    deactivatePulse()
                elif noButton.clicked(event) or centreYesButton.clicked(event) :
                    deactivateShield()
                    resetLevel()
                    pygame.event.post(pygame.event.Event(MAINMENU))
                    continueWithGameplay = True
                    deactivateRampage()
                    deactivateBurst()
                    deactivatePulse()
                    
        elif currentMenu == "Upgrades":
            if upgradesOption1Button.clicked(event):
                playerChosenUpgrades.append(upgradesOption1ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption2ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption3ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption4ButtonText.text)
                if upgradesOption1ButtonText.text == "Sharpen":
                    applySharpenUpgrade()
                elif upgradesOption1ButtonText.text == "Resist":
                    applyResistUpgrade()
                elif upgradesOption1ButtonText.text == "Fast":
                    applyFastUpgrade()
                elif upgradesOption1ButtonText.text == "Dextrous":
                    applyDextrousUpgrade()
                elif upgradesOption1ButtonText.text == "Extend":
                    applyExtendUpgrade()
                elif upgradesOption1ButtonText.text == "Honed":
                    applyHonedUpgrade()
                elif upgradesOption1ButtonText.text == "Deft":
                    applyDeftUpgrade()
                elif upgradesOption1ButtonText.text == "Broaden":
                    applyBroadenUpgrade()
                elif upgradesOption1ButtonText.text == "Boost":
                    applyBoostUpgrade()
                elif upgradesOption1ButtonText.text == "Blacksmith":
                    applyBlacksmithUpgrade()
                elif upgradesOption1ButtonText.text == "Stoic":
                    applyStoicUpgrade()
                elif upgradesOption1ButtonText.text == "Temper":
                    applyTemperUpgrade()
                elif upgradesOption1ButtonText.text == "Inflate":
                    applyInflateUpgrade()
                elif upgradesOption1ButtonText.text == "Exercise":
                    applyExerciseUpgrade()
                elif upgradesOption1ButtonText.text == "Unruly":
                    applyUnrulyUpgrade()
                elif upgradesOption1ButtonText.text == "Toughen":
                    applyToughenUpgrade()
                elif upgradesOption1ButtonText.text == "Speedier":
                    applySpeedierUpgrade()
                elif upgradesOption1ButtonText.text == "Embiggen":
                    applyEmbiggenUpgrade()
                elif upgradesOption1ButtonText.text == "Smite":
                    applySmiteUpgrade()
                elif upgradesOption1ButtonText.text == "Fortify":
                    applyFortifyUpgrade()
                elif upgradesOption1ButtonText.text == "Rush":
                    applyRushUpgrade()
                elif upgradesOption1ButtonText.text == "Lash":
                    applyLashUpgrade()
                elif upgradesOption1ButtonText.text == "Bolster":
                    applyBolsterUpgrade()
                elif upgradesOption1ButtonText.text == "Dash":
                    applyDashUpgrade()
                elif upgradesOption1ButtonText.text == "Saviour":
                    applySaviourUpgrade()
                elif upgradesOption1ButtonText.text == "Rampage":
                    applyRampageUpgrade()
                elif upgradesOption1ButtonText.text == "Burst":
                    applyBurstUpgrade()
                elif upgradesOption1ButtonText.text == "Pulse":
                    applyPulseUpgrade()
                elif upgradesOption1ButtonText.text == "Super":
                    applySuperUpgrade()
                resetLevel()
                preRampageDamage = player.damage
                preBurstDspeed = player.Dspeed
                prePulseRange = player.range
                if currentFloor < 69 or currentDungeon == 5 :
                    currentFloor += 1
                else:                  #So if you go past floor 70 in endless
                    if currentDungeon != 5 :
                        currentFloor = 0
                        loopsOfEndless += 1
            elif upgradesOption2Button.clicked(event):
                playerChosenUpgrades.append(upgradesOption2ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption1ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption3ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption4ButtonText.text)
                if upgradesOption2ButtonText.text == "Sharpen":
                    applySharpenUpgrade()
                elif upgradesOption2ButtonText.text == "Resist":
                    applyResistUpgrade()
                elif upgradesOption2ButtonText.text == "Fast":
                    applyFastUpgrade()
                elif upgradesOption2ButtonText.text == "Dextrous":
                    applyDextrousUpgrade()
                elif upgradesOption2ButtonText.text == "Extend":
                    applyExtendUpgrade()
                elif upgradesOption2ButtonText.text == "Honed":
                    applyHonedUpgrade()
                elif upgradesOption2ButtonText.text == "Deft":
                    applyDeftUpgrade()
                elif upgradesOption2ButtonText.text == "Broaden":
                    applyBroadenUpgrade()
                elif upgradesOption2ButtonText.text == "Boost":
                    applyBoostUpgrade()
                elif upgradesOption2ButtonText.text == "Blacksmith":
                    applyBlacksmithUpgrade()
                elif upgradesOption2ButtonText.text == "Stoic":
                    applyStoicUpgrade()
                elif upgradesOption2ButtonText.text == "Temper":
                    applyTemperUpgrade()
                elif upgradesOption2ButtonText.text == "Inflate":
                    applyInflateUpgrade()
                elif upgradesOption2ButtonText.text == "Exercise":
                    applyExerciseUpgrade()
                elif upgradesOption2ButtonText.text == "Unruly":
                    applyUnrulyUpgrade()
                elif upgradesOption2ButtonText.text == "Toughen":
                    applyToughenUpgrade()
                elif upgradesOption2ButtonText.text == "Speedier":
                    applySpeedierUpgrade()
                elif upgradesOption2ButtonText.text == "Embiggen":
                    applyEmbiggenUpgrade()
                elif upgradesOption2ButtonText.text == "Smite":
                    applySmiteUpgrade()
                elif upgradesOption2ButtonText.text == "Fortify":
                    applyFortifyUpgrade()
                elif upgradesOption2ButtonText.text == "Rush":
                    applyRushUpgrade()
                elif upgradesOption2ButtonText.text == "Lash":
                    applyLashUpgrade()
                elif upgradesOption2ButtonText.text == "Bolster":
                    applyBolsterUpgrade()
                elif upgradesOption2ButtonText.text == "Dash":
                    applyDashUpgrade()
                elif upgradesOption2ButtonText.text == "Saviour":
                    applySaviourUpgrade()
                elif upgradesOption2ButtonText.text == "Rampage":
                    applyRampageUpgrade()
                elif upgradesOption2ButtonText.text == "Burst":
                    applyBurstUpgrade()
                elif upgradesOption2ButtonText.text == "Pulse":
                    applyPulseUpgrade()
                elif upgradesOption2ButtonText.text == "Super":
                    applySuperUpgrade()
                resetLevel()
                preRampageDamage = player.damage
                preBurstDspeed = player.Dspeed
                prePulseRange = player.range
                if currentFloor < 69 or currentDungeon == 5 :
                    currentFloor += 1
                else:                  #So if you go past floor 70 in endless
                    if currentDungeon != 5 :
                        currentFloor = 0
                        loopsOfEndless += 1
            elif upgradesOption3Button.clicked(event):
                playerChosenUpgrades.append(upgradesOption3ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption1ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption2ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption4ButtonText.text)
                if upgradesOption3ButtonText.text == "Sharpen":
                    applySharpenUpgrade()
                elif upgradesOption3ButtonText.text == "Resist":
                    applyResistUpgrade()
                elif upgradesOption3ButtonText.text == "Fast":
                    applyFastUpgrade()
                elif upgradesOption3ButtonText.text == "Dextrous":
                    applyDextrousUpgrade()
                elif upgradesOption3ButtonText.text == "Extend":
                    applyExtendUpgrade()
                elif upgradesOption3ButtonText.text == "Honed":
                    applyHonedUpgrade()
                elif upgradesOption3ButtonText.text == "Deft":
                    applyDeftUpgrade()
                elif upgradesOption3ButtonText.text == "Broaden":
                    applyBroadenUpgrade()
                elif upgradesOption3ButtonText.text == "Boost":
                    applyBoostUpgrade()
                elif upgradesOption3ButtonText.text == "Blacksmith":
                    applyBlacksmithUpgrade()
                elif upgradesOption3ButtonText.text == "Stoic":
                    applyStoicUpgrade()
                elif upgradesOption3ButtonText.text == "Temper":
                    applyTemperUpgrade()
                elif upgradesOption3ButtonText.text == "Inflate":
                    applyInflateUpgrade()
                elif upgradesOption3ButtonText.text == "Exercise":
                    applyExerciseUpgrade()
                elif upgradesOption3ButtonText.text == "Unruly":
                    applyUnrulyUpgrade()
                elif upgradesOption3ButtonText.text == "Toughen":
                    applyToughenUpgrade()
                elif upgradesOption3ButtonText.text == "Speedier":
                    applySpeedierUpgrade()
                elif upgradesOption3ButtonText.text == "Embiggen":
                    applyEmbiggenUpgrade()
                elif upgradesOption3ButtonText.text == "Smite":
                    applySmiteUpgrade()
                elif upgradesOption3ButtonText.text == "Fortify":
                    applyFortifyUpgrade()
                elif upgradesOption3ButtonText.text == "Rush":
                    applyRushUpgrade()
                elif upgradesOption3ButtonText.text == "Lash":
                    applyLashUpgrade()
                elif upgradesOption3ButtonText.text == "Bolster":
                    applyBolsterUpgrade()
                elif upgradesOption3ButtonText.text == "Dash":
                    applyDashUpgrade()
                elif upgradesOption3ButtonText.text == "Saviour":
                    applySaviourUpgrade()
                elif upgradesOption3ButtonText.text == "Rampage":
                    applyRampageUpgrade()
                elif upgradesOption3ButtonText.text == "Burst":
                    applyBurstUpgrade()
                elif upgradesOption3ButtonText.text == "Pulse":
                    applyPulseUpgrade()
                elif upgradesOption3ButtonText.text == "Super":
                    applySuperUpgrade()
                resetLevel()
                preRampageDamage = player.damage
                preBurstDspeed = player.Dspeed
                prePulseRange = player.range
                if currentFloor < 69 :
                    currentFloor += 1
                else:                  #So if you go past floor 70 in endless
                    if currentDungeon != 5 or currentDungeon == 5 :
                        currentFloor = 0
                        loopsOfEndless += 1
            elif upgradesOption4Button.clicked(event):
                playerChosenUpgrades.append(upgradesOption4ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption1ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption2ButtonText.text)
                playerDiscardedUpgrades.append(upgradesOption3ButtonText.text)
                if upgradesOption4ButtonText.text == "Sharpen":
                    applySharpenUpgrade()
                elif upgradesOption4ButtonText.text == "Resist":
                    applyResistUpgrade()
                elif upgradesOption4ButtonText.text == "Fast":
                    applyFastUpgrade()
                elif upgradesOption4ButtonText.text == "Dextrous":
                    applyDextrousUpgrade()
                elif upgradesOption4ButtonText.text == "Extend":
                    applyExtendUpgrade()
                elif upgradesOption4ButtonText.text == "Honed":
                    applyHonedUpgrade()
                elif upgradesOption4ButtonText.text == "Deft":
                    applyDeftUpgrade()
                elif upgradesOption4ButtonText.text == "Broaden":
                    applyBroadenUpgrade()
                elif upgradesOption4ButtonText.text == "Boost":
                    applyBoostUpgrade()
                elif upgradesOption4ButtonText.text == "Blacksmith":
                    applyBlacksmithUpgrade()
                elif upgradesOption4ButtonText.text == "Stoic":
                    applyStoicUpgrade()
                elif upgradesOption4ButtonText.text == "Temper":
                    applyTemperUpgrade()
                elif upgradesOption4ButtonText.text == "Inflate":
                    applyInflateUpgrade()
                elif upgradesOption4ButtonText.text == "Exercise":
                    applyExerciseUpgrade()
                elif upgradesOption4ButtonText.text == "Unruly":
                    applyUnrulyUpgrade()
                elif upgradesOption4ButtonText.text == "Toughen":
                    applyToughenUpgrade()
                elif upgradesOption4ButtonText.text == "Speedier":
                    applySpeedierUpgrade()
                elif upgradesOption4ButtonText.text == "Embiggen":
                    applyEmbiggenUpgrade()
                elif upgradesOption4ButtonText.text == "Smite":
                    applySmiteUpgrade()
                elif upgradesOption4ButtonText.text == "Fortify":
                    applyFortifyUpgrade()
                elif upgradesOption4ButtonText.text == "Rush":
                    applyRushUpgrade()
                elif upgradesOption4ButtonText.text == "Lash":
                    applyLashUpgrade()
                elif upgradesOption4ButtonText.text == "Bolster":
                    applyBolsterUpgrade()
                elif upgradesOption4ButtonText.text == "Dash":
                    applyDashUpgrade()
                elif upgradesOption4ButtonText.text == "Saviour":
                    applySaviourUpgrade()
                elif upgradesOption4ButtonText.text == "Rampage":
                    applyRampageUpgrade()
                elif upgradesOption4ButtonText.text == "Burst":
                    applyBurstUpgrade()
                elif upgradesOption4ButtonText.text == "Pulse":
                    applyPulseUpgrade()
                elif upgradesOption4ButtonText.text == "Super":
                    applySuperUpgrade()
                resetLevel()
                preRampageDamage = player.damage
                preBurstDspeed = player.Dspeed
                prePulseRange = player.range
                if currentFloor < 69 or currentDungeon == 5 :
                    currentFloor += 1
                else:                  #So if you go past floor 70 in endless specifically
                    if currentDungeon != 5 :
                        currentFloor = 0
                        loopsOfEndless += 1
            upgradesQuitButton.clicked(event)
                
                
    if currentMenu == "Gameplay" and showQuitMenu == False: #Unindented block for everything that is updated every frame
        if player.health <= 0 :
            if (canSaviour == True) and (saviourUsed == False) :
                abilitySaviour()
            else:
                if gameMode == "adMode":
                    showDeathScreen() #pauses while we wait for a decision
                else:
                    showDungeonLoseScreen()
                
                    
        elif len(gameplayCollisionsGroup) == 1:
            if canSaviour == True :
                saviourUsed = False
            displaySurface.fill((128,0,0))
            
            displaySurface.blit(attackIndicatorWindow.surf,attackIndicatorWindow.rect)
            displaySurface.blit(ability1IndicatorWindow.surf,ability1IndicatorWindow.rect)
            displaySurface.blit(ability2IndicatorWindow.surf,ability2IndicatorWindow.rect)
            
            displaySurface.blit(playerHealthText.surf, playerHealthText.rect)
            displaySurface.blit(player.surf, player.rect)
            if shieldActivated == True :
                displaySurface.blit(playerShield.surf, playerShield.rect)
            if currentFloor in endingFloor and gameMode == "adMode":
                showDungeonWinScreen()
            else:
                showWinScreen()
        else:
            displaySurface.fill((128,0,0))
            
            displaySurface.blit(attackIndicatorWindow.surf,attackIndicatorWindow.rect)
            displaySurface.blit(ability1IndicatorWindow.surf,ability1IndicatorWindow.rect)
            displaySurface.blit(ability2IndicatorWindow.surf,ability2IndicatorWindow.rect)
            
            if (timeSinceAbility1 >= ability1Cooldown):
                ability1IndicatorWindow.surf.fill((0,255,0))
            else:
                ability1IndicatorWindow.surf.fill((255,0,0))
                
            if (timeSinceAbility2 >= ability2Cooldown) and ((canRampage) or (canBurst) or (canPulse)):
                ability2IndicatorWindow.surf.fill((0,255,0))
            else:
                ability2IndicatorWindow.surf.fill((255,0,0))
              
              
            if endModeWeaponButton.filePath == "sword new.png":
                pass  
            elif shieldCount >= 60 and endModeWeaponButton.filePath == "ShieldTransBorderResized.png":
                attackIndicatorWindow.surf.fill((0,255,0))
                if pygame.key.get_pressed()[playerAttackInput] and endModeWeaponButton.filePath == "ShieldTransBorderResized.png" : #I made this unneccisarily confusing
                    attackIndicatorWindow.surf.fill((255,0,0))
                    playerShield.move(player)         #Effectively, shield count is the cooldown for activation
                    activateShield()                    #and shield timer is the cooldown for deactivation
                    shieldCount = 0                    
                    shieldActivated = True
                    shieldActivationLength = 20 * (player.Dspeed/100)
            elif shieldActivated == True :
                shieldActivationLength -= 1
                playerShield.move(player)
                attackIndicatorWindow.surf.fill((255,0,0))
            else:
                shieldCount += 1
                attackIndicatorWindow.surf.fill((255,0,0))
            
            if shieldActivationLength <= 0 :
                deactivateShield()
                shieldActivated = False
                shieldActivationLength = 20 * (player.Dspeed/100)
                
            if endModeWeaponButton.filePath == "ShieldTransBorderResized.png":
                pass
            elif swordCount >= 60 : #swordCount represents the time for sword to be activateable again (60 frames)
                attackIndicatorWindow.surf.fill((0,255,0))
                if pygame.key.get_pressed()[playerAttackInput] and endModeWeaponButton.filePath == "sword new.png" :
                    attackIndicatorWindow.surf.fill((255,0,0))
                    playerSword.move(player)
                    activateSword()                    
                    swordCount = 0                    
                    swordActivated = True
                    swordActivationLength = 45 * (player.Dspeed/100) #swordActivationLength is how long the sword has elft for being activated
            elif swordActivated == True :
                swordActivationLength -= 1
                playerSword.move(player) #.move() also blits for the sword thanks to rotation being so specialised
                attackIndicatorWindow.surf.fill((255,0,0))
            else:
                swordCount += 1
                attackIndicatorWindow.surf.fill((255,0,0))
            
            if swordActivationLength <= 0 :
                deactivateSword()
                swordActivated = False
                swordActivationLength = 45 * (player.Dspeed/100)
               
            timeSinceAbility1 += 1
            timeSinceAbility2 += 1
            
            if timeSinceAbility2 == 60 : #Ability 2 duration is 60 frames
                deactivateRampage()
                deactivateBurst()
                deactivatePulse()

            for i in range(0,len(gameplayMovementGroup)) :
                list(gameplayMovementGroup)[i].move()
                displaySurface.blit(list(gameplayMovementGroup)[i].surf, list(gameplayMovementGroup)[i].rect)
            if shieldActivated == True :
                displaySurface.blit(playerShield.surf, playerShield.rect)
            checkCollide(gameplayCollisionsGroup)
            for i in range(0,len(gameplayMovementGroup)) :
                if (list(gameplayMovementGroup)[i].colour == (0,0,200)) and (canSaviour) and (not saviourUsed) and (list(gameplayMovementGroup)[i].health <= 0) :
                    pass
                elif checkDeath(list(gameplayMovementGroup)[i]) :
                    break
            playerHealthText.text = str(player.health)
            playerHealthText.surf = standardFont.render("Health: " + playerHealthText.text, True, playerHealthText.colour)
            displaySurface.blit(playerHealthText.surf, playerHealthText.rect)   
            
            if playerShield.flag == True :
                playerShield.flag = False
            if player.flag == True :
                player.flag = False
            if playerSword.flag == True:
                swordDamageCooldown +=1
                if swordDamageCooldown >=20:
                    playerSword.flag = False
                    swordDamageCooldown=0
            if continueWithGameplay == True:
                continueWithGameplay = False

    pygame.display.update()
    framePerSec.tick(60)
    
    
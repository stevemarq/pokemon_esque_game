# Mini Project
# Steve Marquez

import os
# change the directory to the one where this code, graphics.py and the Images folder is located at
os.chdir("/Users/stevem/Desktop/mini_project/Images")
from graphics import *
import math, time
import random

#-------------------------------------------------------------------
class SquareButton:

    #Draws the buttons that will be used
    #Got from an example that was done in class
    def __init__(self, win, x1, y1, x2, y2, color, label):
        rect = Rectangle(Point(x1,y1), Point(x2,y2)) 
        rect.setFill(color)
        rect.setOutline(color)
        rect.draw(win)
        centerPoint = Point(x1 + ((x2-x1)/2), y1 + ((y2-y1)/2))
        text = Text(centerPoint, label)
        text.draw(win)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.graphicsObject = rect
        self.color = color

    def undraw(self):
        self.graphicsObject.undraw()

    def press(self):
        self.graphicsObject.setFill("gray")
        time.sleep(0.2)
        self.graphicsObject.setFill(self.color)

    def overlaps(self, point):
        pointX = point.getX()
        pointY = point.getY()
        if (pointX >= self.x1 and pointX <= self.x2 and
            pointY >= self.y1 and pointY <= self.y2):
            return True
        else:
            return False

#------------------------------------------------------------------
# This class is used to define and work out the battle between the two charatcers

class Fight:
    
    def __init__(self, win, name, moves, health, attack, spriteName):
        self.win    = win
        self.name   = name
        self.move  = moves
        self.health = health
        self.attack = attack
        self.sprite = spriteName
        # If player2 is the same as player1
        self.eneSprite = "enemy_" + spriteName
        self.cursed = False
        self.timesCursed = 0

    # Prevents the health counter and health bar show negative numbers
    def cap(self):
        if (self.health < 0):
            self.health = 0
        
    def enemyHealthBars(self):
        startBar = 905
        endBar = startBar - 5
        interval = (self.health * 2)//5
        for i in range (interval):
            healthRecieved = Rectangle(Point(startBar, 78), Point(endBar, 88))
            healthRecieved.setFill("green")
            healthRecieved.setOutline("green")
            healthRecieved.draw(self.win)
            endBar = endBar - 5
        if (self.health < 100):
            damageTaken = Rectangle(Point(705, 78), Point(endBar + 5, 88))
            damageTaken.setFill("red")
            damageTaken.setOutline("red")
            damageTaken.draw(self.win)

    def playerHealthBars(self):
        startBar = 95
        endBar = startBar + 5
        interval = (self.health * 2)//5
        for i in range (interval):
            healthRecieved = Rectangle(Point(startBar, 78), Point(endBar, 88))
            healthRecieved.setFill("green")
            healthRecieved.setOutline("green")
            healthRecieved.draw(self.win)
            startBar = endBar
            endBar = startBar + 5
        if (self.health < 100 ):
            damageTaken = Rectangle(Point(startBar, 78), Point(295, 88))
            damageTaken.setFill("red")
            damageTaken.setOutline("red")
            damageTaken.draw(self.win)

    # Draws basic animation after each move and works out their abilities
    def action(self, moveName, message, opponent, sprite1, sprite2, eneXpos, playerXpos):
        message.setText("{} chose {}".format(self.name, moveName))
        if (self.move[moveName] == "physical"):
            sprite1.move(eneXpos - playerXpos, 0)
            time.sleep(0.5)
            sprite1.move(playerXpos - eneXpos, 0)
            opponent.health = opponent.health - self.attack
        elif (self.move[moveName] == "special"):
            specialOrb = Circle(Point(playerXpos, 380), 25)
            specialOrb.setFill("purple")
            specialOrb.draw(self.win)
            dx = 10
            if (playerXpos > eneXpos):
                dx = dx * -1
            else:
                pass
            for i in range (65):
                specialOrb.move(dx, 0)
            specialOrb.undraw()
            opponent.health = opponent.health - self.attack
        elif (self.move[moveName] == "boost"):
            boostOrb = Circle(Point(playerXpos, 380), 25)
            boostOrb.setFill("orange")
            boostOrb.draw(self.win)
            for j in range (2):
                boostOrb.move(10, 0)
                boostOrb.move(-20, 0)
                boostOrb.move(10, 0)
            boostOrb.undraw()
            self.attack = self.attack + 5
            message.setText("{} gained +5 attack".format(self.name))
            time.sleep(1)
        elif (self.move[moveName] == "dot"):
            time.sleep(0.5)
            opponent.timesCursed = opponent.timesCursed + 1
            message.setText("{} is cursed".format(opponent.name))
            opponent.cursed = True
        elif (self.move[moveName] == "health gain"):
            time.sleep(1)
            # A health cap so that the enemy or player wouldn't abuse the ability
            if (self.health <= 100 and self.health >= 81):
                message.setText("Not so fast buddy")
                time.sleep(0.5)
                message.setText("No need for that much health")
                time.sleep(0.5)
                message.setText("{} gained +{} health back".format(self.name,(100-self.health)))
                self.health = self.health + (100 - self.health)
            else:
                self.health = self.health + 20
                message.setText("{} gained +20 health back".format(self.name))
            healthOrb = Circle(Point(playerXpos, 380), 25)
            healthOrb.setFill("green")
            healthOrb.draw(self.win)
            for k in range (2):
                healthOrb.move(0, 10)
                healthOrb.move(0, -20)
                healthOrb.move(0, 10)
            healthOrb.undraw()
        # Generates a shaking effect on the characters like in the Pokemon games
        if (self.move[moveName] == "physical" or self.move[moveName] == "special" or self.move[moveName] == "dot"):
            for l in range (2):
                sprite2.move(10, 0)
                sprite2.move(-20, 0)
                sprite2.move(10, 0)
        
        
    def gameOver(self, characterSprite, enemySprite, player2):      
        if (player2.health == 0):
            enemySprite.undraw()
            time.sleep(1)
            characterSprite.undraw()
            return True
        elif (self.health == 0):
            characterSprite.undraw()
            time.sleep(1)
            enemySprite.undraw()
            return True
        else:
            return False

    
    def combat(self, player2):
        # Draws the moves, players, health bars, and health and attack counters
        moveNames = list(self.move.keys())
        move1 = SquareButton(self.win, 582, 543, 699, 577, "white", moveNames[0])
        move2 = SquareButton(self.win, 582, 633, 697, 665, "white", moveNames[1])
        move3 = SquareButton(self.win, 843, 543, 958, 577, "white", moveNames[2])
        move4 = SquareButton(self.win, 843, 633, 958, 665, "white", moveNames[3])
        
        message = Text(Point(237, 600), "You chose {}".format(self.name))
        message.setSize(20)
        message.draw(self.win)
        characterSprite = Image(Point(175, 380), self.sprite)
        characterSprite.draw(self.win)
        self.playerHealthBars()
        characterHealthCounter = Text(Point(45, 80), "HP: {}".format(self.health))
        characterHealthCounter.setTextColor("white")
        characterHealthCounter.setSize(20)
        characterHealthCounter.draw(self.win)
        characterDamageCounter = Text(Point(45, 100), "ATK: {}".format(self.attack))
        characterDamageCounter.setTextColor("white")
        characterDamageCounter.setSize(15)
        characterDamageCounter.draw(self.win)
        time.sleep(1)
        
        message.setText("Your opponent is {}".format(player2.name))
        enemySprite = Image(Point(825, 380), player2.eneSprite)
        enemySprite.draw(self.win)
        player2.enemyHealthBars()
        enemyHealthCounter = Text(Point(950, 80), "HP: {}".format(player2.health))
        enemyHealthCounter.setTextColor("white")
        enemyHealthCounter.setSize(20)
        enemyHealthCounter.draw(self.win)
        enemyDamageCounter = Text(Point(950, 100), "ATK: {}".format(player2.attack))
        enemyDamageCounter.setTextColor("white")
        enemyDamageCounter.setSize(15)
        enemyDamageCounter.draw(self.win)

        #player1 makes a move
        while (self.gameOver(characterSprite, enemySprite, player2) == False):
            message.setText("Choose a move")
            moveSelected = False
            while (moveSelected == False):
                p = self.win.getMouse()
                if (move1.overlaps(p)):
                    move1.press()
                    moveSelected = True
                    self.action(moveNames[0], message, player2, characterSprite, enemySprite, 824, 176)
                elif (move2.overlaps(p)):
                    move2.press()
                    moveSelected = True
                    self.action(moveNames[1], message, player2, characterSprite, enemySprite, 824, 176)
                elif (move3.overlaps(p)):
                    move3.press()
                    moveSelected = True
                    self.action(moveNames[2], message, player2, characterSprite, enemySprite, 824, 176)
                elif (move4.overlaps(p)):
                    move4.press()
                    moveSelected = True
                    self.action(moveNames[3], message, player2, characterSprite, enemySprite, 824, 176)
            #Updates: health if a health boost was selected, Attack is damage boost was selected
            self.playerHealthBars()
            characterHealthCounter.setText("HP: {}".format(self.health))
            characterDamageCounter.setText("ATK: {}".format(self.attack))
            #Updates: opponent's health
            player2.cap()
            player2.enemyHealthBars()
            enemyHealthCounter.setText("HP: {}".format(player2.health))
            #Checks if a curse was placed on opponent
            if (player2.cursed == True and player2.health > 0):
                if (player2.timesCursed > 3):
                    player2.timesCursed = 0
                    player2.cursed = False
                    message.setText ("Your opponent is no longer cursed.")
                    time.sleep(0.5)
                else:
                    player2.health = player2.health - (5 * player2.timesCursed)
                    player2.cap()
                    message.setText("Your opponent is cursed. -{} health".format(5 * player2.timesCursed))
                    time.sleep(0.5)    
            player2.enemyHealthBars()
            enemyHealthCounter.setText("HP: {}".format(player2.health))

            #Player2 makes a move if they still have health
            if (player2.health > 0):
                enemyMove = random.choice(list(player2.move.keys()))
                player2.action(enemyMove, message, self, enemySprite, characterSprite, 176, 824)
                enemyDamageCounter.setText("ATK: {}".format(player2.attack))
                self.cap()
                enemyHealthCounter.setText("HP: {}".format(player2.health))
                self.playerHealthBars()
                player2.enemyHealthBars()
            if (self.cursed == True):
                 if (self.timesCursed > 3):
                    self.timesCursed = 0
                    self.cursed = False
                    message.setText ("You are no longer no longer cursed.")
                    time.sleep(0.5)
                 else:
                    self.health = self.health - (5 * self.timesCursed)
                    message.setText("You are cursed. -{} health.".format(5 * self.timesCursed))
                    self.cap()
                    self.playerHealthBars()
                    time.sleep(0.5)
            self.cap()
            characterHealthCounter.setText("HP: {}".format(self.health))
        if (self.health == 0):
            return ("YOUR OPPONENT WON!")
        else:
            return ("YOU WON!")


    
#--------------------------------------------------------------------------------------------------
# This class is about the visuals and flow between "screens' of the game

class Game(GraphWin):

    def __init__(self):
        super().__init__("Monster Mash", 1000, 700)
        self.setBackground("black")



    def main(self):
        startButton = SquareButton(self, 301, 522, 459, 599, "black", "start")
        infoButton  = SquareButton(self, 541, 522, 699, 599, "black", "info")
        mainMenu = Image(Point(500,350), "main_menu.gif")
        mainMenu.draw(self)
        madeSelection = False
        while (madeSelection == False):
            p = self.getMouse()
            if (startButton.overlaps(p) == True):
                mainMenu.undraw()
                madeSelection = True
                self.characterSelect()
            elif (infoButton.overlaps(p) == True):
                # Draws an image with text exlaining the rules
                infoMenu = Image(Point(500,350), "info.gif")
                infoMenu.draw(self)
                self.getMouse()
                # Returns to the menu after a mouse click
                infoMenu.undraw()

        
# When called, it helps initialize a battle with a characters atributes.

    def characters(self, name):
        Dracula = Fight(self, "DRACULA", {"BITE": "physical", "BATS":"special", "MIDNIGHT BOOST":"boost", "BLOOD DRAIN":"dot"}, 100, 5, "dracula.gif")
        Frankenstein = Fight(self,"FRANKENSTEIN", {"PUNCH":"physical", "GRAVE ROT":"dot", "THUNDER":"special", "BULK UP":"health gain"}, 100, 5, "frankenstein.gif")
        Wolfman = Fight(self,"WOLFMAN", {"HOWL":"boost", "SCRATCH":"physical", "BITE":"physical", "TACKLE":"physical"}, 100, 5, "wolfman.gif")
        InvisibleMan = Fight(self,"INVISIBLE MAN", {"PUNCH":"physical", "CHEMICAL BURN":"dot", "DAMAGE BOOST":"boost", "INVISIBLE":"health gain"}, 100, 5, "invisible_man.gif")
        if (name == "Dracula"):
            return (Dracula)
        elif (name == "Frankenstein"):
            return (Frankenstein)
        elif (name == "Wolfman"):
            return (Wolfman)
        elif (name == "Invisible Man"):
            return (InvisibleMan)



    def characterSelect(self):
        dracButton  = SquareButton (self, 51, 222, 208, 299, "black", "Dracula")
        frankButton = SquareButton (self, 301, 362, 459, 439, "black", "Frankenstein")
        wolfButton  = SquareButton (self, 550, 222, 708, 299, "black", "Wolfman")
        inviButton  = SquareButton (self, 800, 362, 958, 439, "black", "Invisisble Man")
        selectionScreen = Image(Point (500, 350), "character_select.gif")
        selectionScreen.draw(self)
        madeSelection = False
        selectedPlayer = ""
        while (madeSelection == False):
            p = self.getMouse()
            if (dracButton.overlaps(p)):
                 selectedPlayer = "Dracula"
                 madeSelection = True
            elif (frankButton.overlaps(p)):
                selectedPlayer = "Frankenstein"
                madeSelection = True
            elif (wolfButton.overlaps(p)):
                selectedPlayer = "Wolfman"
                madeSelection = True
            elif (inviButton.overlaps(p)):
                selectedPlayer = "Invisible Man"
                madeSelection = True
        selectionScreen.undraw()
        # Draws the battle screen and sends out which character was chosen
        self.battle(selectedPlayer)


    def battle(self, player1):
        battleScreen = Image(Point(500, 350), "battle_screen.gif")
        battleScreen.draw(self)
        # Chooses the second player randomly and gets thier attributes
        players = ["Dracula", "Frankenstein", "Wolfman", "Invisible Man"]
        player2 = random.choice(players)
        player1 = self.characters(player1)
        player2 = self.characters(player2)
        # Initiates the battle by calling the funciton combat in the class Fight
        winner = player1.combat(player2)
        battleScreen.undraw()
        self.endscreen(winner)
        

    def endscreen(self, winner):
        mainMenuButton = SquareButton (self, 222, 582, 378, 659, "black", "Main Menu")
        quitButton = SquareButton (self, 422, 582, 578, 659, "black", "Quit")
        charactersButton = SquareButton (self, 620, 582, 778, 659, "black", "Characters")
        gameOverScreen = Image(Point(500,350), "game_over.gif")
        gameOverScreen.draw(self)
        victor = Text(Point(500, 300), winner)
        victor.setSize(30)
        victor.setTextColor("white")
        victor.draw(self)
        madeSelection = False
        # Gives the user a choice to leave, go to the menu, or choose another character
        while (madeSelection == False):
            p = self.getMouse()
            if (mainMenuButton.overlaps(p)):
                madeSelection = True
                gameOverScreen.undraw()
                self.main()
            if (quitButton.overlaps(p)):
                madeSelection = True
                gameOverScreen.undraw()
                self.close()
            if (charactersButton.overlaps(p)):
                madeSelection = True
                gameOverScreen.undraw()
                self.characterSelect()

#-----------------------------

# Initializes the game:
def play():
    game = Game()
    game.main()
    
    
        
    
    
        
    




    
    
    
    
    
    
    





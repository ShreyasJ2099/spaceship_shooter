from cmu_graphics import *
import time

from cmu_graphics.shape_logic import cmu_graphics

Buttons = []

totaltimer = 0

ShopNames = ['Score x2', 'Score x2', 'Score x2', 'Laser +1', 'Laser +1', 'Laser +1', 'Invin. x3', 'Heal + 20', 'Ally']

ShopPriceNames = ['Cost: 10','Cost: 30','Cost: 50','Cost: 25','Cost: 50','Cost: 75','Cost: 70','Cost: 30','Cost: 100']

ShopPrices = [10,30,50,25,50,75,70,30,100]

ShopBought = [0,0,0,0,0,0,0,0,0]

ScoreModifier = 1

LaserCount = 1

AllyExist = False

def CreateShop():
    global ShopBox, Buttons, Button
    ShopBox = Rect(200,200,300,300,align='center',fill='dodgerblue', border='silver', borderWidth=8)
    for i in range(3):
        for j in range(3):
            Button = Group (
                Rect(70 + (j*90), 70 + (i*90), 80, 80, fill='dodgerblue', border='silver', borderWidth = 5),
                Label(ShopNames[(i*3)+j], 110 + (j*90), 110 + (i*90), fill='silver', size=12, italic=True, bold=True, font='monospace'),
                Label(ShopPriceNames[(i*3)+j],110 + (j*90), 135 + (i*90), fill='silver', size=12,bold=True, font='monospace'),
            )
            Buttons.append(Button)
            if ShopBought[Buttons.index(Button)] == 1:
                Button.add(Label('Bought',Button.centerX, Button.centerY, size=20, fill='lawnGreen', bold=True, font='monospace', rotateAngle = 45))

def DeleteShop():
    global ShopBox, Buttons, Button 
    ShopBox.visible = False
    for Button in Buttons:
        Button.visible = False
    Buttons.clear()

# Code
app.background = 'black'
Player = Group (
    Rect(195,200,10,20,fill='gray'),
    # top, right, left
    Polygon(200,190,225,215,175,215, fill='dodgerblue'),
    RegularPolygon(200,200,20,3, fill='dodgerblue'),
    Circle(200,195,6,fill=gradient('gold', 'yellow'))
)

Borders = Group (
    Rect(-50,0,1,500,fill='red'),   
    Rect(449,0,1,500,fill='red'),
    Rect(0,-50,500,1,fill='red'),
    Rect(0,449,500,1,fill='red')
)

HPBack = Group( 
    Rect(8,8,384, 24, fill='gray'),
    Rect(10,10, 380, 20, fill='red')
)

HPFront = Rect(10,10,380, 20, fill='green')
PlayerHealth = 100

IBack = Group (
    Rect(200,370,190,20,fill='gray'),
    Rect(202,372,186,16,fill='salmon')
)
IFront = Rect(202,372,186,16,fill='cyan')

PauseButton = Group (
    Rect(175,380,25,25,fill='dodgerblue', border='silver', borderWidth = 2, align='center'),
    Rect(175,380,3,16,fill='silver', align='center'),
    Rect(175,380,3,16,fill='silver', align='center', rotateAngle = 90)
)

for i in range(20):
    Stars = Group (
        Star(randrange(0,400), randrange(0,400), 4, 5, roundness=75, fill='white')
    )
    Stars.toBack()

vertVelocity = 0
horiVelocity = 0
PlayerScore = 0
PastPlayerScore = -1
Score = Group (
    Label('',0,0)
)

lasers = []

asteroids = []

timer = 0

InvincibleTimer = 0

PlayerInvincible = False

Paused = False

AllyShootTimer = 0

RainbowMode = False

def onKeyHold(keys):
    global vertVelocity, horiVelocity, InvincibleTimer, Player, timer, PlayerInvincible, PlayerScore, PlayerHealth, RainbowMode
    if 'd' in keys and horiVelocity <= 20 and not Paused:
        horiVelocity += 1.5  
    if 'a' in keys and horiVelocity >= -20 and not Paused:
        horiVelocity -= 1.5 
    if 'w' in keys and vertVelocity <= 20 and not Paused:
        vertVelocity += 1.5
    if 's' in keys and vertVelocity >= -20 and not Paused:
        vertVelocity -= 1.5
    if 'c' in keys:
        for Blast in Blasts:
            Blasts.remove(Blast)
            Blast.visible = False
        for Laser in lasers:
            lasers.remove(Laser)
            Laser.visible = False
        for asteroid in asteroids:
            asteroids.remove(asteroid)
            asteroid.visible = False
        for Button in Buttons:
            Buttons.remove(Button)
            Button.visible = False
    if 'space' in keys and InvincibleTimer == 0 and not Paused:
        Player.opacity = 50
        timer = 0
        PlayerInvincible = True
        InvincibleTimer = 10
    if 'o' in keys and 'p' in keys:
        CheatCode = app.getTextInput('Enter the Cheat Code.')
        if CheatCode == 'goldrush':
            PlayerScore = 1000
        elif CheatCode == 'heal':
            PlayerHealth = 100
        elif CheatCode == 'rainbow':
            RainbowMode = not RainbowMode
            if RainbowMode == False:
                x, y = Player.centerX, Player.centerY
                Player.visible = False
                Player = Group (
                    Rect(195,200,10,20,fill='gray'),
                    # top, right, left
                    Polygon(200,190,225,215,175,215, fill='dodgerblue'),
                    RegularPolygon(200,200,20,3, fill='dodgerblue'),
                    Circle(200,195,6,fill=gradient('gold', 'yellow'))
                )
                Player.centerX, Player.centerY = x, y
        elif CheatCode == 'invincible':
            Player.opacity = 50
            PlayerInvincible = True
            timer = -100000000000000

Blasts = []
Blast = Rect(0,0,401,4)
Blasts.append(Blast)

IModifier = 1
AsteroidX = 0
AsteroidY = 0

r = 0
Colors = ['red','orangeRed','tomato','orange','lemonChiffon','peachPuff','yellow','greenYellow','paleGreen','green','darkCyan','dodgerblue','blue','navy','indigo','darkMagenta','purple','deepPink','paleVioletRed','pink','lavenderBlush']

def onStep():
    global vertVelocity, horiVelocity, lasers, asteroids, PlayerScore, totaltimer, PastPlayerScore, Score, PlayerHealth, timer, Blast, InvincibleTimer, PlayerInvincible, IFront, IBack, Paused, IModifier, AllyExist, Ally, AllyShootTimer, AsteroidX, AsteroidY, RainbowMode, r, Colors
    # timer update
    if not Paused:
        timer += 0.03
        AllyShootTimer += 0.03
        totaltimer += 0.03
    # Invincible timer update
    if not Paused:  
        InvincibleTimer -= 0.03
    if InvincibleTimer < 0:
        InvincibleTimer = 0
    # Health Bar
    HPBack.toFront()
    HPFront.toFront()
    if PlayerHealth > 0:
        HPFront.width = 3.8 * PlayerHealth
    else:
        HPFront.width = 0.01
        Rect(0,0,400,400, fill='slateGray', opacity=90)
        Rect(100,100,200,200,fill=gradient('darkBlue','blue', start='left'),border='silver',borderWidth=4)
        Label('GAME OVER', 200,185, size=30,bold=True, fill='white')
        Label('Score: ' + str(PlayerScore), 200,215, size=30,bold=True, fill='white')
        Label('Time: ' + str(pythonRound(totaltimer, 2)), 200, 245, size=15,bold=True, fill='white')
        app.stop()
    # Space Physics
    if not Paused:    
        Player.centerX += horiVelocity
        Player.centerY -= vertVelocity
    if vertVelocity > 0 and not Paused:
        vertVelocity -= 1
    elif vertVelocity < 0 and not Paused:
        vertVelocity += 1
    if horiVelocity > 0 and not Paused:
        horiVelocity -= 1
    elif horiVelocity < 0 and not Paused:
        horiVelocity += 1
    # Edge Tracking
    if Player.centerX > 400 and not Paused:
        Player.centerX = 0
    elif Player.centerX < 0 and not Paused:
        Player.centerX = 400
    elif Player.centerY > 400 and not Paused:
        Player.centerY = 0
    elif Player.centerY < 0 and not Paused:
        Player.centerY = 400
    # Laser Movement
    if not Paused:    
        for Laser in lasers:
            x, y = getPointInDir(Laser.centerX, Laser.centerY, Laser.rotateAngle, 16)
            Laser.centerX = x
            Laser.centerY = y
    #Laser Delete
    for Laser in lasers:    
        if Laser.hitsShape(Borders) == True and not Paused:
            lasers.remove(Laser)
            Laser.clear()

    #Create Asteroids
    if randrange(1,75) == 1 and not Paused:
        randnum = randrange(1,4)
        if randnum == 1:
            asteroid = Group(
                Circle(0,randnum * 100, 35, fill=gradient('slateGray','silver')),
                Circle(10, randnum * 100 + 10, 10, fill=gradient('slateGray','darkGray',start='left')),
                Circle(-10, randnum * 100 - 20, 10, fill=gradient('slateGray','darkGray',start='left')),
                Circle(0, randnum * 100 + 20, 10, fill=gradient('slateGray','darkGray',start='left'))

            )
        elif randnum == 2:
            asteroid = Group(
                Circle(400, randnum * 100, 35, fill=gradient('slateGray','silver')),
                Circle(410, randnum * 100 + 10, 10, fill=gradient('slateGray','darkGray',start='left')),
                Circle(390, randnum * 100 - 20, 10, fill=gradient('slateGray','darkGray',start='left')),
                Circle(400, randnum * 100 + 20, 10, fill=gradient('slateGray','darkGray',start='left'))
            )
        elif randnum == 3:
            asteroid = Group(
                Circle(randnum * 100,0, 35, fill=gradient('slateGray','silver')),
                Circle(randnum * 100 + 10, 10,10,fill=gradient('slateGray','darkGray',start='left')),
                Circle(randnum * 100 -20, -10,10,fill=gradient('slateGray','darkGray',start='left')),
                Circle(randnum * 100 + 20, 0,10,fill=gradient('slateGray','darkGray',start='left'))
            )    
        elif randnum == 4:
            asteroid = Group(
                Circle(randnum * 100,400, 35, fill=gradient('slateGray','silver')),
                Circle(randnum * 100 + 10, 410, 10, fill=gradient('slateGray','darkGray',start='left')),
                Circle(randnum * 100 - 20, 390, 10, fill=gradient('slateGray','darkGray',start='left')),
                Circle(randnum * 100 + 20, 400, 10, fill=gradient('slateGray','darkGray',start='left'))
            )
        asteroids.append(asteroid)
        if randnum == 1:
            asteroid.rotateAngle = randrange(45,135)
        elif randnum == 2:
            asteroid.rotateAngle = randrange(225,315)
        elif randnum == 3:
            asteroid.rotateAngle = randrange(135,225)
        elif randnum == 4:
            asteroid.rotateAngle = randrange(45,315)
    # Asteroids Movement
    if not Paused:
        for asteroid in asteroids:
            x1,y1 = getPointInDir(asteroid.centerX,asteroid.centerY, asteroid.rotateAngle, 6)
            asteroid.centerX = x1
            asteroid.centerY = y1
            if asteroid.centerX == 0 or asteroid.centerX == 400:
                asteroid.clear()
            elif asteroid.centerY == 0 or asteroid.centerY == 400:
                asteroid.clear()
    # Asteroids Delete
    for asteroid in asteroids:
        if asteroid.hitsShape(Borders) == True:
            asteroids.remove(asteroid)
            asteroid.clear()
    # Asteroids Collision
    for Laser in lasers:
        if PlayerScore != PastPlayerScore:
            break
        for asteroid in asteroids:
            if (asteroid.hitsShape(Laser) == True):
                asteroid.clear()
                Laser.clear()
                PlayerScore += 1 * ScoreModifier
                break
    # Player Overlap With Asteroid Damage    
    if not Paused:    
        for asteroid in asteroids:
            if (asteroid.hitsShape(Player) == True) and not PlayerInvincible:
                asteroid.visible = False
                asteroid.clear()
                PlayerHealth -= 20 # Damage per Asteroid
                if not PlayerHealth == 0:
                    Flash = Group (
                        Rect(0,0,400,400,fill='red',opacity=35)    
                    )
                    time.sleep(0.1)
                    Flash.clear()
                break
    #Score Update
    if PlayerScore != PastPlayerScore:
        Score.clear()
        Score = Group (
            Label(PlayerScore, 10,380, size=30,font='monospace', fill='silver', bold=True, align='left')
        )    
        PastPlayerScore = PlayerScore
    # Create Blast
    if randrange(0,200) == 0 and not Paused:
        varY = randrange(0,400)
        Blast = Rect(0,varY,1,20, fill='chartreuse', align='center')
        Blasts.append(Blast)
    for Blast in Blasts:    
        if Blast.width < 400 and not Paused:
            Blast.width += 50
        if Blast.width > 400 and not Paused:
            Blast.height -= 2
            Blast.centerY += 1
        if Blast.height == 2 and not Paused:
            Blast.visible = False
            Blasts.remove(Blast)
    # Player Hit Blasts
    for Blast in Blasts:
        if Blast.hitsShape(Player) and not PlayerInvincible and not Paused:
            PlayerHealth -= 10
            if not PlayerHealth == 0:
                Flash = Group (
                    Rect(0,0,400,400,fill='red',opacity=35)    
                )
                time.sleep(0.1)
                Flash.clear()
            Blast.visible = False
            Blasts.remove(Blast)
    # Player Opacity Update
    if not Paused:    
        if timer < (2 * IModifier):
            Player.opacity = 50
            PlayerInvincible = True
        else:
            Player.opacity = 100
            PlayerInvincible = False
    #Invincibility Bar
    if PlayerInvincible:
        InvincibleTimer = 9.99
    IBack.toFront()
    IFront.toFront()
    if InvincibleTimer > 0 and InvincibleTimer < 10:
        IFront.width = 186 * ((10 - InvincibleTimer)/10)
    elif InvincibleTimer >= 10:
        IFront.width = 186
    else:
        IFront.width = 186
    # To front
    PauseButton.toFront()
    # Asteroid Sense
    if AllyExist and not Paused: 
        pastAX = AsteroidX
        pastAY = AsteroidY
        for asteroid in asteroids:
            if distance(asteroid.centerX, asteroid.centerY, Player.centerX, Player.centerY) <= 150:
                AsteroidX = asteroid.centerX
                AsteroidY = asteroid.centerY
        if pastAX == AsteroidX and pastAY == AsteroidY:
            AsteroidX = 0
            AsteroidY = 0
    # Ally Movement
    if AllyExist and Paused == False:
        if AsteroidX != 0 and AsteroidY != 0:
            Ally.rotateAngle = angleTo(Ally.centerX, Ally.centerY, AsteroidX, AsteroidY)
        else:
            Ally.rotateAngle = Player.rotateAngle + 180
        Ally.centerX, Ally.centerY = getPointInDir(Player.centerX, Player.centerY, Ally.rotateAngle, 40)
        # Ally Shoot
        if AsteroidX != 0 and AsteroidY != 0 and AllyShootTimer >= 2:
            Laser = Group ( 
                Line(Ally.centerX, Ally.centerY - 10, Ally.centerX, Ally.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Ally.rotateAngle
            Laser.toBack()
            lasers.append(Laser)
            AllyShootTimer = 0
        # Rainbow Mode?
    if RainbowMode and not Paused:
        Player.fill = Colors[r]
        if not PlayerInvincible:    
            Player.opacity = 80
        else:
            Player.opacity = 50
        for Laser in lasers:
            Laser.fill = Colors[r]
        r += 1
        if r > len(Colors) - 1:
            r = 0

def onMouseMove(mouseX, mouseY):
    if not Paused:
        Player.rotateAngle = angleTo(Player.centerX, Player.centerY, mouseX, mouseY)
    for Button in Buttons:
        if Button.contains(mouseX, mouseY):
            Button.opacity = 100
        else:
            Button.opacity = 50

def onMousePress(mouseX, mouseY):
    global lasers, PauseButton, Paused, PlayerScore, ScoreModifier, LaserCount, PlayerHealth, IModifier, AllyExist, Ally
    if PauseButton.contains(mouseX, mouseY):
        if Paused == True:
            PauseButton.visible = False
            PauseButton = Group (
                Rect(175,380,25,25,fill='dodgerblue', border='silver', borderWidth = 2, align='center'),
                Rect(175,380,3,16,fill='silver', align='center'),
                Rect(175,380,3,16,fill='silver', align='center', rotateAngle = 90)
            )
            Paused = False
            DeleteShop()
        elif Paused == False:
            PauseButton.visible = False
            PauseButton = Group (
                Rect(175,380,25,25,fill='dodgerblue', border='silver', borderWidth = 2, align='center'),
                Rect(175,380,3,16,fill='silver', align='center'),
                Rect(175,380,3,16,fill='silver', align='center', rotateAngle = 90)
            )

            Paused = True
            CreateShop()
    elif not Paused:    
        if LaserCount == 1:
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle
            Laser.toBack()
            lasers.append(Laser)
        elif LaserCount == 2:
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle - 10
            Laser.toBack()
            lasers.append(Laser)
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle + 10
            Laser.toBack()
            lasers.append(Laser)
        elif LaserCount == 3:
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle - 20
            Laser.toBack()
            lasers.append(Laser)
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle
            Laser.toBack()
            lasers.append(Laser)
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle + 20
            Laser.toBack()
            lasers.append(Laser)
        elif LaserCount == 4:
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle - 30
            Laser.toBack()
            lasers.append(Laser)
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle - 10
            Laser.toBack()
            lasers.append(Laser)
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle + 10
            Laser.toBack()
            lasers.append(Laser)
            Laser = Group ( 
                Line(Player.centerX, Player.centerY - 10, Player.centerX, Player.centerY + 10, lineWidth=5, fill='chartreuse'),
            )
            Laser.rotateAngle = Player.rotateAngle + 30
            Laser.toBack()
            lasers.append(Laser)

    # Buy Item
    for Button in Buttons:
        if Button.contains(mouseX, mouseY):
            if ShopPrices[Buttons.index(Button)] <= PlayerScore and ShopBought[Buttons.index(Button)] == 0:
                PlayerScore -= ShopPrices[Buttons.index(Button)]
                if Buttons.index(Button) != 7:    
                    ShopBought[Buttons.index(Button)] = 1
                    Button.add(Label('Bought',Button.centerX, Button.centerY, size=20, fill='lawnGreen', bold=True, font='monospace', rotateAngle = 45))
                # Check Button Properties
                if Buttons.index(Button) == 0 or Buttons.index(Button) == 1 or Buttons.index(Button) == 2:
                    ScoreModifier += 1
                elif Buttons.index(Button) == 3 or Buttons.index(Button) == 4 or Buttons.index(Button) == 5:
                    LaserCount += 1
                elif Buttons.index(Button) == 7:
                    if PlayerHealth <= 80:
                        PlayerHealth += 20
                    else:
                        PlayerHealth = 100
                elif Buttons.index(Button) == 6:
                    IModifier += 2
                elif Buttons.index(Button) == 8:
                    # Create Ally
                    Ally = Circle(500, 500, 13, fill='silver', border='gray', borderWidth=3)
                    AllyExist = True
            else:
                NoBuy = Rect(Button.centerX, Button.centerY, 80, 80, align='center', fill='red', opacity = 40)
                Button.add(NoBuy)
                time.sleep(0.1)
                Button.remove(NoBuy)

cmu_graphics.run()

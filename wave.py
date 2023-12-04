"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# TAWIAH SAMUEL ASARE sat242, SERGIO LOPEZ GARCIA sal292
# 01/12/2023
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _direction: the direction of the aliens
    # Invariant: _direction is a string of the form 'left' or 'right'
    #
    # Attribute _firerate: the number of steps until the aliens fire
    # Invariant: _firerate is a random int in the range 1..BOLT_RATE
    #
    # Attribute _firestep: the number of frames after the last fire
    # Invariant: _firestep: is an int in the range 1..self._firerate
    #
    # Attribute _livestext: the label for how many lives are left
    # Invariant: _livestext: is a GLabel object
    #
    # Attribute _livescont: the counter for how many lives are left
    # Invariant: _livescont: is a GLabel object


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAliensLeft(self):
        """
        Returns the number of aliens left in the wave.
        """
        cont = 0
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    cont+= 1
        return cont

    def setAliens(self):
        """
        Procedure to set the aliens in a wave. It creates a 2d list with alien
        objects and stores the list in the attribute _aliens.
        """
        # Initial Parameters
        img = 0
        img_cont = 0
        aliens = []
        y= GAME_HEIGHT-(ALIEN_HEIGHT//2)-(ALIEN_HEIGHT
        +ALIEN_V_SEP)*(ALIEN_ROWS-1) - ALIEN_CEILING
        # Create table
        for row in range(ALIEN_ROWS):
            rows = []
            x = ALIEN_H_SEP + (ALIEN_WIDTH//2)
            for col in range(ALIENS_IN_ROW):
                rows.append(Alien(x, y, ALIEN_IMAGES[img]))
                x += ALIEN_H_SEP+ALIEN_WIDTH
            aliens.append(rows)
            y += ALIEN_V_SEP+ALIEN_HEIGHT
            img_cont = img_cont + 0.5
            img = int(img_cont) % len(ALIEN_IMAGES)
        # Assign parameter
        self._aliens = aliens


    def setShip(self):
        """
        Procedure to initialize the ship. It creates a Ship object and stores
        it in the attribute _ship.
        """
        self._ship = Ship(GAME_WIDTH//2, SHIP_BOTTOM,
        SHIP_WIDTH, SHIP_HEIGHT, SHIP_IMAGE)

    def getShip(self):
        """
        Returns the player's ship as a Ship object or None.
        """
        return self._ship


    def setDline(self):
        """
        Procedure to set the defense line. It creates a GPath object and stores
        it in the attribute _dline. If an alien crosses this line, then the
        player loses.
        """
        self._dline = GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
        linewidth=2, linecolor='white')

    def getLives(self):
        """
        Returns the number of lives the player has left.
        """
        return self._lives


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a wave.
        """
        self.setAliens()
        self.setShip()
        self.setDline()
        self._time = 0
        self._direction = 'right'
        self._bolts = []
        self._firerate = random.randint(1, BOLT_RATE)
        self._firestep = 0
        self._lives = SHIP_LIVES
        self._livestext = GLabel(text='Lives:', font_size=60,
        font_name="Arcade.ttf",x=(2/3)*GAME_WIDTH, y=GAME_HEIGHT-30,
        linecolor = 'dark green', fillcolor='black')
        self._livescont = GLabel(text=str(self._lives), font_size=60,
        font_name="Arcade.ttf",x=(2/3)*GAME_WIDTH+100, y=GAME_HEIGHT-30,
        linecolor = 'green', fillcolor='black')

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Updates the wave based on the input received, time passed, and winning
        or losing conditions.
        """
        assert isinstance(input, GInput)
        assert isinstance(dt, int) or isinstance(dt, float)

        if input.is_key_down('left'):
            self._ship.move_left()
        if input.is_key_down('right'):
            self._ship.move_right()
        if input.is_key_pressed('up'):
            if self.no_player_bolts():
                x = self._ship.getX()
                self._bolts.append(Bolt(x, SHIP_HEIGHT, BOLT_SPEED))

        self.control_alien_bolts()

        self.control_player_bolts()

        self._time += dt
        if self._time >= ALIEN_SPEED:
            self.move_aliens()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Displays the wave objects every frame.
        """
        # Display score and lives message
        self._livestext.draw(view)
        self._livescont.draw(view)
        # Draw the aliens
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        # Draw the ship
        if self._ship is not None:
            self._ship.draw(view)
        # Draw the defense line
        self._dline.draw(view)
        # Draw the bolts
        for bolt in self._bolts:
            bolt.draw(view)


    # HELPER METHODS FOR COLLISION DETECTION
    def move_aliens(self):
        """
        Procedure to control alien movement and check for crossing the defensive
        line.
        """
        if self._direction == 'right':
            self.walk_right()
        else:
            self.walk_left()
        self._time = 0
        self._firestep += 1
        if self.bottommost_alien()-ALIEN_HEIGHT//2<=DEFENSE_LINE:
            self._ship = None
            self._lives = 0

    def control_alien_bolts(self):
        """
        Procedure to control the alien firing bolts.
        """
        # Alien bolts
        if self._firestep >= self._firerate:
            # Pick a random alien
            alien = self.pick_rand_alien()
            # Get the coordinates of alien and fire
            x = alien.getX()
            y = alien.getY()
            self._bolts.append(Bolt(x, y, -BOLT_SPEED))
            # Reinitialize attribute values
            self._firestep = 0
            self._firerate = random.randint(1, BOLT_RATE)

    def control_player_bolts(self):
        """
        Procedure to handle player bolts and their collision.
        """
        # Player and alien bolts
        for bolt in self._bolts:
            # Move up or down
            bolt.setHeight(bolt.getHeight()+bolt.getVelocity())
            # Remove if out of bounds
            if (bolt.getVelocity()==BOLT_SPEED and
            bolt.getHeight()+BOLT_WIDTH//2 >= GAME_HEIGHT):
                self._bolts.remove(bolt)
            elif (bolt.getVelocity()==-BOLT_SPEED and
            bolt.getHeight()-BOLT_WIDTH//2 <= 0):
                self._bolts.remove(bolt)
            # Check colision with aliens
            for row in range(len(self._aliens)):
                for idx in range(len(self._aliens[row])):
                    if (self._aliens[row][idx] is not None and
                    self._aliens[row][idx].collides(bolt)):
                        self._aliens[row][idx] = None
                        self._bolts.remove(bolt)
            # Check colision with ship
            if self._ship is not None:
                if self._ship.collides(bolt):
                    self._lives -= 1
                    self._livescont = GLabel(text=str(self._lives), font_size=60,
                    font_name="Arcade.ttf",x=(2/3)*GAME_WIDTH+100, y=GAME_HEIGHT-30,
                    linecolor = 'green', fillcolor='black')
                    self._ship = None
                    # Eliminate all the bolts
                    # self._bolts.remove(bolt)
                    self._bolts = []

    def rightmost_alien(self):
        """
        Returns the X-coordinate of the rightmost alien alive in the wave.
        """
        for c in range(len(self._aliens[0])-1,-1,-1):
            for r in range(len(self._aliens)):
                if self._aliens[r][c] is not None:
                    return self._aliens[r][c].getX()

    def leftmost_alien(self):
        """
        Returns the X-coordinate of the leftmost alien alive in the wave.
        """
        for c in range(len(self._aliens[0])):
            for r in range(len(self._aliens)):
                if self._aliens[r][c] is not None:
                    return self._aliens[r][c].getX()

    def bottommost_alien(self):
        """
        Returns the Y-coordinate of the bottommost alien alive in the wave.
        """
        for r in range(len(self._aliens)):
            for c in range(len(self._aliens[0])):
                if self._aliens[r][c] is not None:
                    return self._aliens[r][c].getY()

    def walk_right(self):
        """
        Procedure to move all the aliens one step right or one step down if they
        get to the right border.
        """
        border = self.rightmost_alien()
        # Move down
        if border >= GAME_WIDTH-ALIEN_H_SEP-ALIEN_WIDTH//2:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.setY(alien.getY()-ALIEN_V_WALK)
            self._direction = 'left'
        # Move right
        else:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.setX(alien.getX()+ALIEN_H_WALK)

    def walk_left(self):
        """
        Procedure to move all the aliens one step left or one step down if they
        get to the left border.
        """
        border = self.leftmost_alien()
        # x = self._aliens[0][0].getX()
        if border <= ALIEN_H_SEP+ALIEN_WIDTH//2:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.setY(alien.getY()-ALIEN_V_WALK)
            self._direction = 'right'
        else:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.setX(alien.getX()-ALIEN_H_WALK)

    def no_player_bolts(self):
        """
        Returns True if there are no player bolts currently fired. The player
        can only have one bolt at a time on screen.
        """
        for bolt in self._bolts:
            if bolt._velocity > 0:
                return False
        return True

    def pick_rand_alien(self):
        """
        Returns a random alien from the wave.
        """
        # Convert table into 1d list without None
        aliens = []
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    aliens.append(alien)
        return random.choice(aliens)

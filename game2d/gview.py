"""
The view and input classes for 2D game support.

These class are both 'singletons'.  That means they are included with :class:`GameApp`
and you should never try to create new versions of these classes.  Instead, you should
read the documentation on how to use the provided objects.

Author: Walker M. White (wmw2)
Date:   August 1, 2017 (Python 3 version)
"""
# Basic Kivy Modules
from kivy.graphics import *
from kivy.graphics.instructions import *
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp

from introcs.geom import Point2


class GInput(object):
    """
    A class representing an input handler

    An input handler receives mouse and keyboard information, and makes it available
    to the user.  To access mouse information, simply access the attribute ``touch``.
    To access keyboard information, use the method :meth:`is_key_down`.

    **You should never construct an object of this class**.  Creating a new instance
    of this class will not properly hook it up to the keyboard and mouse.  Instead,
    you should only use the one provided in the `input` attribute of :class:`GameApp`.
    See the documentation of that class for more information.
    """

    # MUTABLE ATTRIBUTES
    @property
    def touch_enabled(self):
        """
        Whether the touch (mouse) interface is currently enabled.

        Setting this value to False will disable all mouse clicks or drags. The value is
        True by default.

        **Invariant**: Must be a bool
        """
        return self._touch_enabled

    @touch_enabled.setter
    def touch_enabled(self,value):
        assert type(value) == bool, 'value %s is not a bool' % repr(value)
        if value and not self._touch_enabled:
            self._enable_touch()
        elif not value and self._touch_enabled:
            self._disable_touch()
        self._touch_enabled = value

    @property
    def keyboard_enabled(self):
        """
        Whether the keyboard interface is currently enabled.

        Setting this value to False will disable all key presses. The value is
        True by default.

        **Invariant**: Must be a bool
        """
        return self._keyboard_enabled

    @keyboard_enabled.setter
    def keyboard_enabled(self,value):
        assert type(value) == bool, 'value %s is not a bool' % repr(value)
        if value and not self._keyboard_enabled:
            self._enable_keyboard()
        elif not value and self._keyboard_enabled:
            self._disable_keyboard()
        self._keyboard_enabled = value


    # IMMUTABLE ATTRIBUTES
    @property
    def touch(self):
        """
        The current (x,y) coordinate of the mouse, if pressed.

        This method only returns coordinates if the mouse button is pressed. If the mouse
        button is not pressed it returns None. The origin (0,0) corresponds to the bottom
        left corner of the application window.

        There is currently no way to get the location of the mouse when the button is not
        pressed.  This a limitation of Kivy.

        **Immutable**: This value cannot be altered.

        **Invariant**: Must be either a :class:`Point2` or None (if there is no touch).
        """
        if self._touch is None:
            return None

        return Point2(self._touch.x/dp(1),self._touch.y/dp(1))

    @property
    def key_count(self):
        """
        The number of keys currently held down.

        This attribute is a quick way to check whether the user has pressed any keys.

        **Immutable**: This value cannot be altered.

        **Invariant**: Must be an int > 0."""
        return self._keycount

    @property
    def keys(self):
        """
        The list of keys that are currently held down.

        Using this attribute is much slower than the method :meth:`is_key_down`.  You
        should use that method when you want to test a specific key. This attribute is
        primarily for debugging.

        **Immutable**: This value cannot be altered.

        **Invariant**: Must be a list of strings (possibly empty)
        """
        return tuple(k for (k,v) in self._keystate.items() if v)


    # BUILT-IN METHODS
    def __init__(self):
        """
        Creates a new input handler

        This constructor does very little.  It does not hook up the handler to the
        mouse or keyboard.  That functionality happens behind the scenes with hidden
        methods.  You should only use  use the object provided in the ``input`` attribute
        of :class:`GameApp`. See the documentation of that class for more information.
        """
        self._view  = None
        self._touch = None
        self._keyboard = None

        self._touch_enabled = True
        self._keyboard_enabled = True

        self._keystate = {}
        self._keypress = {}
        self._keyrelease = {}
        self._keycount = 0
        
        self._touchpress = 0
        self._touchrelease = 0


    # PUBLIC METHODS
    def is_key_down(self,key):
        """
        Checks whether the key is currently held down.

        A key is down so long as the user has it pressed down. A key can be down for
        multiple animation frames.

        The key is a string describing the key pressed.  For example, to determine
        whether the right-arrow key is down, use the method call::

            input.is_key_down('right')

        Similarly the method call::

            input.is_key_down('w')

        will indicate whether the W key is down. If key is the empty string '',
        then this method will check if any key is down.

        For a complete list of key names, see the
        `Kivy documentation <http://kivy.org/docs/_modules/kivy/core/window.html>`_.

        :param key: the key to test
        :type key:  ``str``

        :return: True if ``key`` is currently held down
        :rtype:  ``bool``
        """
        if key != '':
            return key in self._keystate and self._keystate[key]
        return self._keycount > 0

    def is_key_pressed(self,key):
        """
        Returns whether the key was just pressed.

        A key is pressed if it is down this current animation frame, but was not down
        a previous animation frame.

        The key is a string describing the key pressed.  For example, to determine
        whether the right-arrow key is pressed, use the method call::

            input.is_key_pressed('right')

        Similarly the method call::

            input.is_key_pressed('w')

        will indicate whether the W key is pressed. If key is the empty string '',
        then this method will check if any key is pressed.

        For a complete list of key names, see the
        `Kivy documentation <http://kivy.org/docs/_modules/kivy/core/window.html>`_.

        :param key: the key to test
        :type key:  ``str``

        :return: True if ``key`` is currently held down
        :rtype:  ``bool``
        """
        if key != '':
            return key in self._keypress
        return len(self._keypress) > 0

    def is_key_released(self,key):
        """
        Returns whether the key was just released.

        A key is released if it is up this current animation frame, but was down a
        previous animation frame.

        The key is a string describing the key released.  For example, to determine
        whether the right-arrow key is released, use the method call::

            input.is_key_released('right')

        Similarly the method call::

            input.is_key_released('w')

        will indicate whether the W key is released. If key is the empty string '',
        then this method will check if any key is released.

        For a complete list of key names, see the
        `Kivy documentation <http://kivy.org/docs/_modules/kivy/core/window.html>`_.

        :param key: the key to test
        :type key:  ``str``

        :return: True if ``key`` is currently held down
        :rtype:  ``bool``
        """
        if key != '':
            return key in self._keyrelease
        return len(self._keyrelease) > 0

    def is_touch_down(self):
        """
        Returns whether the mouse is currently held down.

        If this method returns True, the attribute `touch` is guaranteed to not be
        None.

        :return: True if the mouse is currently held down; False otherwise
        :rtype:  ``bool``
        """
        return not self._touch is None

    def is_touch_pressed(self):
        """
        Returns whether the mouse is was just pressed.

        The difference between a touch and a press is that a press means that the 
        mouse is down this animation frame, but was not down the previous animation
        frame.

        If this method returns True, the attribute `touch` is guaranteed to not be
        None.

        :return: True if the mouse is currently held down; False otherwise
        :rtype:  ``bool``
        """
        return self._touchpress > 0

    def is_touch_released(self):
        """
        Returns whether the mouse is was just released.

        A release means that the mouse is not down this animation frame, but was down
        the previous animation frame.

        If this method returns True, the attribute `touch` is guaranteed to be None.

        :return: True if the mouse is currently held down; False otherwise
        :rtype:  ``bool``
        """
        return self._touchrelease > 0


    # HIDDEN METHODS
    def _prestep(self):
        """
        The step to perform before the update step.  
        
        This method 'dirties' the inputs so we know what presses and releases are read.
        """
        for k in self._keypress:
            self._keypress[k] = False
        for k in self._keyrelease:
            self._keyrelease[k] = False
        if self._touchpress > 0:
            self._touchpress -= 1
        if self._touchrelease > 0:
            self._touchrelease -= 1

    def _poststep(self):
        """
        The step to perform after the update step.  
        
        This method deletes any read presses and releases.
        """
        keylist = list(self._keypress.keys())
        for k in keylist:
            if not self._keypress[k]:
                del self._keypress[k]
        
        keylist = list(self._keyrelease.keys())
        for k in keylist:
            if not self._keyrelease[k]:
                del self._keyrelease[k]
        
        if self._touchpress == 1:
            self._touchpress = 0
        if self._touchrelease == 1:
            self._touchrelease = 0

    def _register(self,view):
        """
        Registers the view with this input handler; activating it.

        The input handler can only have one view at a time.  If there is an active
        view, it will unregister it first before registering the new one.

        :param view: the view to register.
        :type view:  ``GView``
        """
        self._view = view
        if self.touch_enabled:
            self._enable_touch()
        if self.keyboard_enabled:
            self._enable_keyboard()

    def _enable_touch(self):
        """
        Enables touch events for this input handler
        """
        if self._view is None:
            return
        self._view.bind(on_touch_down=self._capture_touch)
        self._view.bind(on_touch_move=self._capture_touch)
        self._view.bind(on_touch_up=self._release_touch)

    def _disable_touch(self):
        """
        Disables touch events for this input handler
        """
        if self._view is None:
            return
        self._view.unbind(on_touch_down=self._capture_touch)
        self._view.unbind(on_touch_move=self._capture_touch)
        self._view.unbind(on_touch_up=self._release_touch)
        self._touch = None

    def _enable_keyboard(self):
        """
        Enables keyboard events for this input handler
        """
        if self._view is None:
            return
        from kivy.core.window import Window
        self._keyboard = Window.request_keyboard(self._disable_keyboard, self._view, 'text')
        self._keyboard.bind(on_key_down=self._capture_key)
        self._keyboard.bind(on_key_up=self._release_key)

    def _disable_keyboard(self):
        """
        Disables keyboard events for this input handler
        """
        if self._view is None:
            return
        self._keyboard.unbind(on_key_down=self._capture_key)
        self._keyboard.unbind(on_key_up=self._release_key)
        self._keyboard = None
        self._keystate = {}
        self._keycount = 0

    def _capture_key(self, keyboard, keycode, text, modifiers):
        """
        Captures a simple keypress and adds it to the key dictionary.

        :param keyboard: reference to the keyboard
        :type keyboard:  ``kivy.core.window.Keyboard``

        :param keycode: the key pressed as a pair of int (keycode) and a name
        :type keycode:  (``int``, ``str``)

        :param text: the text associated with the key
        :type text:  ``str``

        :param modifiers: the modifiers associated with the press
        :type modifiers:  list of key codes
        """
        k = keycode[1]
        # Need to handle the case where a release was dropped
        if not k in self._keystate or not self._keystate[k]:
            self._keycount += 1
            self._keypress[k] = True
        self._keystate[k] = True
        return True

    def _release_key(self, keyboard, keycode):
        """
        Releases a simple keypress and removes it from the key dictionary.

        :param keyboard: reference to the keyboard
        :type keyboard:  ``kivy.core.window.Keyboard``

        :param keycode: the key released as a pair of int (keycode) and a name
        :type keycode:  (``int``, ``str``)
        """
        self._keystate[keycode[1]] = False
        self._keyrelease[keycode[1]] = True
        self._keycount -= 1
        return True

    def _capture_touch(self,view,touch):
        """
        Captures the current mouse position if button is pressed.

        :param view: reference to the view window
        :type view:  :class:`GView`

        :param touch: the information about the mouse press
        :type touch:  ``kivy.input.motionevent.TouchEvent``
        """
        if not self._touch:
            self._touchpress = 2
        self._touch = touch
        
        #self._touch.grab(self)

    def _release_touch(self,view,touch):
        """
        Releases a the current mouse position from memory.

        :param view: reference to the view window
        :type view:  :class:`GView`

        :param touch: the information about the mouse release
        :type touch:  ``kivy.input.motionevent.TouchEvent``
        """
        if self._touch:
            self._touchrelease = 2
        self._touch = None


# #mark -
class GView(FloatLayout):
    """
    A class representing a drawing window for a :class:`GameApp` application.

    This is the class that you will use to draw shapes to the screen.  Simply pass your
    :class:`GObject` instances to the :meth:`draw` method.  You must do this every
    animation frame, as the game is constantly clearing the window.

    **You should never construct an object of this class**.  Creating a new instance
    of this class will not properly display it on the screen.  Instead, you should
    only use the one provided in the `view` attribute of :class:`GameApp`.
    See the documentation of that class for more information.
    """

    # BUILT-IN METHODS
    def __init__(self):
        """
        Creates a new view for display

        This constructor does very little.  It does not hook up the view to the game
        window.  That functionality happens behind the scenes with hidden methods.
        You should only use use the object provided in the `view` attribute of
        :class:`GameApp`. See the documentation of that class for more information.
        """
        FloatLayout.__init__(self)
        self._frame = InstructionGroup()
        self.bind(pos=self._reset)
        self.bind(size=self._reset)
        self._reset()
        self._contents = set()


    # PUBLIC METHODS
    def draw(self,cmd):
        """
        Draws the given Kivy graphics command to this view.

        You should never call this method, since you do not understand raw Kivy graphics
        commands.  Instead, you should use the `draw` method in :class:`GObject` instead.

        :param cmd: the command to draw
        :type cmd:  A Kivy graphics command
        """
        if not cmd in self._contents:
            self._frame.add(cmd)
            self._contents.add(cmd)

    def clear(self):
        """
        Clears the contents of the view.

        This method is called for you automatically at the start of the animation
        frame.  That way, you are not drawing images on top of one another.
        """
        self._frame.clear()
        self._contents.clear()

    # HIDDEN METHODS
    def _reset(self,obj=None,value=None):
        """
        Resets the view canvas in response to a resizing event
        """
        self.canvas.clear()
        self.canvas.add(Color(1,1,1))
        self.canvas.add(Rectangle(pos=self.pos,size=self.size))
        # Work-around for Retina Macs
        self.canvas.add(Scale(dp(1),dp(1),dp(1)))
        self.canvas.add(self._frame)

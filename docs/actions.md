# Actions

### button(button1 [, button2 = None, minustrigger = -16383, plustrigger = 16383 ])
- For button, simply maps to 'button1' press.
- For stick or pad, when it is moved over 'minustrigger', 'button1' is pressed;
  When it is moved back, 'button1' is released. Similary, 'button2' is pressed
  and released when stick (or finger on pad) moves over 'plustrigger' value
- For trigger, when trigger value goes over 'plustrigger', 'button2' is pressed;
  then, when trigger value goes over 'minustrigger', 'button2' is released and
  replaced with 'button1'. Whatever button was emulated by trigger, it is
  released when trigger is released.
  
  Note that 'button2' is always optional.


### mouse(axis [, speed = 1, acceleration = 0 ])
Controls mouse movement or scroll wheel.

- For stick, lets cursor or mouse wheel to be controlled by stick tilt.
- For pad, does same thing as 'trackball'. You can set pad to move mouse only
  in one axis using this.
- For wheel controlled by pad, emulates finger scroll.
- For button, pressing button maps to single movement over mouse axis or
  single step on scroll wheel.


### trackpad([ speed = 1 ])
Available only for pads. Acts as trackpad - sliding finger over the pad moves the mouse.


### trackball([ speed = 1 ])
Available only for pads. Acts as trackball.


#### axis(id [, min = -32767, max = 32767 ])
- For button, pressing button maps to moving axis full way to 'max'.
  Releasing button returns emulated axis back to 'min'.
- For stick or pad, simply maps real axis to emulated
- For trigger, maps trigger position to to emulated axis. Note that default
  trigger position is not in middle, but in minimal possible value.


#### dpad(up, down, left, right)
Emulates dpad. Touchpad is divided into 4 triangular parts and when user touches
touchped, action is executed depending on finger position.
Available only for pads and sticks; for stick, works by translating
stick position, what probably doesn't yields expected results.


#### dpad8(up, down, left, right, upleft, upright, downleft, downright)
Same as dpad, with more directions.


### macro(key1, key2... [, pause])
Available only for buttons. Emulates multiple keyboard (or button) presses.
Pause, if used, has to be int or floating number and specifies delay between
key being pressed and released.


### profile(name)
Loads another profile

### shell(command)
Executes command on background

# Modifiers:

#### click(action)
Used to create action that occurs only if pad or stick is pressed.
For example, `click(dpad(...))` set to pad will create dpad that activates
buttons only when pressed.

#### mode(button1, action1, [button2, action2... buttonN, actionN] [, default] )
Defines mode shifting. If physical buttonX is pressed, actionX is executed.
Optional default action is executed if none from specified buttons is pressed.


# Shortcuts:
#### raxis(id)
Shortcut for `axis(id, 32767, -32767)`, that is call to axis with min/max values
reversed. Effectively inverted axis mapping.

#### hatup(id)
Shortcut for `axis(id, 0, 32767)`, emulates moving hat up or pressing 'up'
button on dpad.

#### hatdown(id)
Shortcut for `axis(id, 0, -32767)`, emulates moving hat down or pressing 'down'
button on dpad.

#### hatleft(id), hadright(id)
Same thing as hatup/hatdown, as vertical hat movement and left/right dpad
buttons are same events on another axis


# Examples:
Emulate key and button presses based on stick position
```
"stick" : {
	"X"		: { "action" : "pad(Keys.BTN_X, Keys.BTN_B)" },
	"Y"		: { "action" : "key(Keys.KEY_A, Keys.KEY_B)" },
```


Emulate left/right stick movement with X and B buttons
```
"buttons" : {
	"B"      : { "action" : "axis(Axes.ABS_X, 0, 32767)" },
	"X"      : { "action" : "axis(Axes.ABS_X, 0, -32767)" },
```

Emulate dpad on left touchpad, but act only when dpad is pressed
```
"left_pad" : {
	"action" : "click( dpad('hatup(Axes.ABS_HAT0Y)', 'hatdown(Axes.ABS_HAT0Y)', 'hatleft(Axes.ABS_HAT0X)', 'hatright(Axes.ABS_HAT0X)' ) )"
}
```

Emulate button A when left trigger is half-pressed and button B when
it is pressed fully
```
"triggers" : {
	"LEFT"  : { "action" : "pad(Keys.BTN_A, Keys.BTN_B)" },
```
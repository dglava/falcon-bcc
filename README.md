# Falcon-BCC

Falcon-BCC is an utility for Falcon BMS which randomizes switches in
the F16 cockpit. It's supposed to make cold-starts a bit more interesting,
by requiring more attention and not relying on the switches being always
in the same state. It's probably unrealistic, since the plane would be
prepared by the ground crew, hence the name - Bad Crew Chief.

It's a hacky solution. It works by sending key-presses to Falcon BMS which
are assigned to all the various switches and knobs.

### How to use
* Run the **falcon-bcc.py** file with Python.  
* Once in-game, randomize the cockpit by moving the Mode knob on the CMDS
panel to STBY.

It will only randomize the cockpit once. Subsequent toggling of the CMDS
panel knob to STBY won't have any effect. A sound effect is played
during the randomizing for better feedback when it's done.

### Dependencies
Just the Python standard library.

### Tip for Usage
For ultimate convenience, as with my other [utility which displays briefings on a smartphone](https://github.com/dglava/falcon-briefing),
it is recommended to add it to a startup script, which would start it
together with Falcon BMS.

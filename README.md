# Falcon-BCC

Falcon-BCC is an utility for Falcon BMS which randomizes switches in
the F16 cockpit. It's supposed to make cold-starts a bit more interesting,
by requiring more attention and not relying on the switches being always
in the same state. It's probably unrealistic, since the plane would be
prepared by the ground crew, hence the name (Bad Crew Chief).

It's a very hacky solution. It works by sending key-presses to Falcon BMS
of the switches and knobs, but a random number of times, bringing them
into a different state. It reads the keyfile to figure out which keyboard
keys "to press". For it to work, you need to have the REQUIRED_CALLBACKS
mentioned in the file mapped. Otherwise it won't work.

It has to be manually triggered using the CMDS Panel. I experimented with
automatic triggering upon entering the cockpit, but it seems fragile, since
the Falcon BMS shared memory reports entering the cockpit (the 3D world)
too soon. Adding a delay might be a solution, but I settled for manually
triggering it by toggling something in the cockpit. It might change
in the future.

### How to use
* Edit **falcon-bcc.py** and replace `KEYFILE` with the location of your keyfile.  
* You should also make sure that all the required callbacks are mapped
to something in your keyfile. Check the falcon-bcc.py file and `REQUIRED_CALLBACKS` 
* Then run the **falcon-bcc.py** file with Python.  
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

You can also compile it into a standalone EXE with
[PyInstaller](https://www.pyinstaller.org/). I might post pre-compiled
versions in this repository (note the warning related to PyInstaller
executables [here](https://github.com/dglava/falcon-briefing#download))

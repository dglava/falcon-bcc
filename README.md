# Falcon-BCC

Falcon-BCC is an utility for Falcon BMS which randomizes switches in
the F16 cockpit. It's supposed to make cold-starts a bit more interesting,
by requiring more attention and not relying on the switches being always
in the same state. It's probably unrealistic, since the plane would be
prepared by the ground crew, hence the name (Bad Crew Chief).

### How to use
* Edit **falcon-bcc.py** and replace `KEYFILE` with the location of your keyfile.  
* You should also make sure that all the required callbacks are mapped
to something in your keyfile. Check the falcon-bcc.py file and `REQUIRED_CALLBACKS` 
* Then run the **falcon-bcc.py** file with Python.  

### Dependencies
Python standard library.

### Tip for Usage
For ultimate convenience, as with my other [utility which displays briefings on a smartphone](https://github.com/dglava/falcon-briefing),
it is recommended to add it to a startup script, which would start it
together with Falcon BMS.

You can also compile it into a standalone EXE with
[PyInstaller](https://www.pyinstaller.org/). I might post pre-compiled
versions in this repository (note the warning related to PyInstaller
executables [here](https://github.com/dglava/falcon-briefing#download))

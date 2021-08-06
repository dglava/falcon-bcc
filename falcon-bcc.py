#!/usr/bin/python

# falcon-bcc
# Copyright 2021 Dino Duratović

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Contains source code licensed under different licenses; marked appropriately
# with comments

import sys
import ctypes
import ctypes.wintypes
import time
import random

KEYFILE = "location of your keyfile"
REFRESH_FREQUENCY = 2
REQUIRED_CALLBACKS = [
    "SimProbeHeatOn", "SimProbeHeatOff", "SimProbeHeatTest",
    "SimFuelPumpOff", "SimFuelPumpNorm", "SimFuelPumpAft", "SimFuelPumpFwd",
    "SimIFFMasterOff", "SimIFFMasterStby", "SimIFFMasterLow", "SimIFFMasterNorm", "SimIFFMasterEmerg",
    "SimBupUhfOff", "SimBupUhfMain", "SimBupUhfBoth",
    "SimBupUhfPreset", "SimBupUhfGuard", "SimBupUhfManual",
    "SimEWSModeOff", "SimEWSModeStby", "SimEWSModeMan", "SimEWSModeSemi", "SimEWSModeAuto", "SimEWSModeByp",
    "SimEWSProgOne", "SimEWSProgOne", "SimEWSProgThree", "SimEWSProgFour",
    "SimRALTSTDBY", "SimRALTON", "SimRALTOFF",
    "SimAirSourceOff", "SimAirSourceNorm", "SimAirSourceDump", "SimAirSourceRam",
    "SimINSOff", "SimINSNorm", "SimINSNav", "SimINSInFlt",

    "SimEpuToggle",
    "SimLandingLightCycle",
    "SimParkingBrakeCycle",
    "SimRightAPSwitch",
    "SimLeftAPSwitch",
    "SimStepMasterArm",
    "SimStepHSIMode",
    "SimRFSwitch",
    "SimAntennaSelectCycle",
    "SimAntiIceCycle",
    "SimHUDVelocity",
    "SimHUDRadar",
    "SimHUDBrightness",
    "SimReticleSwitch",
    "SimHUDDED",

    "SimDigitalBUP",
    "SimAltFlaps",
    "SimManualFlyup",
    "SimLEFLockSwitch",
    "SimTrimAPDisc",
    "SimToggleMasterFuel",
    "SimToggleAuxComMaster",
    "SimExtlPower",
    "SimExtlAntiColl",
    "SimExtlSteady",
    "SimExtlWing",
    "SimECMPower",
    "SimEngCont",
    "SimMPOToggle",
    "SimEWSRWRPower",
    "SimEWSJammerPower",
    "SimEWSMwsPower",
    "SimEWSChaffPower",
    "SimEWSFlarePower",
    "SimEWSO1Power",
    "SimEWSO2Power",
    "SimEwsJett",
    "SimGndJettEnable",
    "SimCATSwitch",
    "SimBrakeChannelToggle",
    "SimHookToggle",
    "SimLaserArmToggle",
    "SimExtFuelTrans",
    "SimLeftHptPower",
    "SimRightHptPower",
    "SimFCRPower",
    "SimSMSPower",
    "SimFCCPower",
    "SimMFDPower",
    "SimUFCPower",
    "SimGPSPower",
    "SimDLPower",
    "SimMAPPower"
]

# falcon bms shared memory reader; see https://github.com/nmeier/simscript
# <--- start license: MIT License Copyright (c) 2021 Nils Meier
FILE_MAP_COPY = 0x0001
FILE_MAP_WRITE = 0x0002
FILE_MAP_READ = 0x0004
FILE_MAP_ALL_ACCESS = 0x0008

class FLIGHTDATA(ctypes.Structure):
    _fields_ = (
        ("x", ctypes.wintypes.FLOAT),
        ("y", ctypes.wintypes.FLOAT),
        ("z", ctypes.wintypes.FLOAT),
        ("xDot", ctypes.wintypes.FLOAT),
        ("yDot", ctypes.wintypes.FLOAT),
        ("zDot", ctypes.wintypes.FLOAT),
        ("alpha", ctypes.wintypes.FLOAT),
        ("beta", ctypes.wintypes.FLOAT),
        ("gamma", ctypes.wintypes.FLOAT),
        ("pitch", ctypes.wintypes.FLOAT),
        ("roll", ctypes.wintypes.FLOAT),
        ("yaw", ctypes.wintypes.FLOAT),
        ("mach", ctypes.wintypes.FLOAT),
        ("kias", ctypes.wintypes.FLOAT),
        ("vt", ctypes.wintypes.FLOAT),
        ("gs", ctypes.wintypes.FLOAT),
        ("windOffset", ctypes.wintypes.FLOAT),
        ("nozzlePos", ctypes.wintypes.FLOAT),
        ("internalFuel", ctypes.wintypes.FLOAT),
        ("externalFuel", ctypes.wintypes.FLOAT),
        ("fuelFlow", ctypes.wintypes.FLOAT),
        ("rpm", ctypes.wintypes.FLOAT),
        ("ftit", ctypes.wintypes.FLOAT),
        ("gearPos", ctypes.wintypes.FLOAT),
        ("speedBrake", ctypes.wintypes.FLOAT),
        ("epuFuel", ctypes.wintypes.FLOAT),
        ("oilPressure", ctypes.wintypes.FLOAT),
        ("lightBits", ctypes.wintypes.INT),
        ("headPitch", ctypes.wintypes.FLOAT),
        ("headRoll", ctypes.wintypes.FLOAT),
        ("headYaw", ctypes.wintypes.FLOAT),

        ("lightBits2", ctypes.wintypes.INT),
        ("lightBits3", ctypes.wintypes.INT),
        ("ChaffCount", ctypes.wintypes.FLOAT),
        ("FlareCount", ctypes.wintypes.FLOAT),
        ("NoseGearPos", ctypes.wintypes.FLOAT),
        ("LeftGearPos", ctypes.wintypes.FLOAT),
        ("RightGearPos", ctypes.wintypes.FLOAT),
        ("AdiIlsHorPos", ctypes.wintypes.FLOAT),
        ("AdiIlsVerPos", ctypes.wintypes.FLOAT),
        ("courseState", ctypes.wintypes.INT),
        ("headingState", ctypes.wintypes.INT),
        ("totalStates", ctypes.wintypes.INT),
        ("courseDeviation", ctypes.wintypes.FLOAT),
        ("desiredCourse", ctypes.wintypes.FLOAT),
        ("distanceToBeacon", ctypes.wintypes.FLOAT),
        ("bearingToBeacon", ctypes.wintypes.FLOAT),
        ("currentHeading", ctypes.wintypes.FLOAT),
        ("desiredHeading", ctypes.wintypes.FLOAT),
        ("deviationLimit", ctypes.wintypes.FLOAT),
        ("halfDeviationLimit", ctypes.wintypes.FLOAT),
        ("localizerCourse", ctypes.wintypes.FLOAT),
        ("airbaseX", ctypes.wintypes.FLOAT),
        ("airbaseY", ctypes.wintypes.FLOAT),
        ("totalValues", ctypes.wintypes.FLOAT),
        ("TrimPitch", ctypes.wintypes.FLOAT),
        ("TrimRoll", ctypes.wintypes.FLOAT),
        ("TrimYaw", ctypes.wintypes.FLOAT),
        ("hsiBits", ctypes.wintypes.INT),
        ("DEDLines", (ctypes.c_char * 26) * 5),
        ("Invert", (ctypes.c_char * 26) * 5),
        ("PFLLines", (ctypes.c_char * 26) * 5),
        ("PFLInvert", (ctypes.c_char * 26) * 5),
        ("UFCTChan", ctypes.wintypes.INT),
        ("AUXTChan", ctypes.wintypes.INT),
        ("RwrObjectCount", ctypes.wintypes.INT),
        ("RWRsymbol", ctypes.wintypes.INT * 40),
        ("bearing", ctypes.wintypes.FLOAT * 40),
        ("missileActivity", ctypes.wintypes.ULONG * 40),
        ("missileLaunch", ctypes.wintypes.ULONG * 40),
        ("selected", ctypes.wintypes.ULONG * 40),
        ("lethality", ctypes.wintypes.FLOAT * 40),
        ("newDetection", ctypes.wintypes.ULONG * 40),
        ("fwd", ctypes.wintypes.FLOAT),
        ("aft", ctypes.wintypes.FLOAT),
        ("total", ctypes.wintypes.FLOAT),
        ("VersionNum", ctypes.wintypes.INT),
        ("headX", ctypes.wintypes.FLOAT),
        ("headY", ctypes.wintypes.FLOAT),
        ("headZ", ctypes.wintypes.FLOAT),
        ("MainPower", ctypes.wintypes.INT),
    )

class FLIGHTDATA2(ctypes.Structure):
    _fields_ = (
        ("nozzlePos2", ctypes.wintypes.FLOAT),
        ("rpm2", ctypes.wintypes.FLOAT),
        ("ftit2", ctypes.wintypes.FLOAT),
        ("oilPressure2", ctypes.wintypes.FLOAT),
        ("navMode", ctypes.wintypes.BYTE),
        ("AAUZ", ctypes.wintypes.FLOAT),
        ("tacanInfo", ctypes.wintypes.CHAR * 2),

        ("AltCalReading", ctypes.wintypes.INT),
        ("altBits", ctypes.wintypes.INT),
        ("powerBits", ctypes.wintypes.INT),
        ("blinkBits", ctypes.wintypes.INT),

        ("cmdsMode", ctypes.wintypes.INT),
        ("BupUhfPreset", ctypes.wintypes.INT),

        ("BupUhfFreq", ctypes.wintypes.INT),
        ("cabinAlt", ctypes.wintypes.FLOAT),
        ("hydPressureA", ctypes.wintypes.FLOAT),
        ("hydPressureB", ctypes.wintypes.FLOAT),
        ("currentTime", ctypes.wintypes.INT),
        ("vehicleACD", ctypes.wintypes.SHORT),
        ("VersionNum", ctypes.wintypes.INT),

        ("fuelFlow2", ctypes.wintypes.FLOAT),

        ("RwrInfo", ctypes.wintypes.CHAR * 512),
        ("lefPos", ctypes.wintypes.FLOAT),
        ("tefPos", ctypes.wintypes.FLOAT),

        ("vtolPos", ctypes.wintypes.FLOAT),

        ("pilotsOnline", ctypes.wintypes.CHAR),
        ("pilotsCallsign", ctypes.wintypes.CHAR * 32 * 12),
        ("pilotsStatus", ctypes.wintypes.CHAR * 32),

        ("bumpIntensity", ctypes.wintypes.FLOAT),

        ("latitude", ctypes.wintypes.FLOAT),
        ("longitude", ctypes.wintypes.FLOAT),

        ("RTT_size", ctypes.wintypes.USHORT * 2),
        ("RTT_area", ctypes.wintypes.USHORT * 7 * 4),

        ("iffBackupMode1Digit1", ctypes.wintypes.CHAR),
        ("iffBackupMode1Digit2", ctypes.wintypes.CHAR),
        ("iffBackupMode3Digit1", ctypes.wintypes.CHAR),
        ("iffBackupMode3Digit2", ctypes.wintypes.CHAR),

        ("instrLight", ctypes.wintypes.CHAR),

        ("bettyBits", ctypes.wintypes.UINT),
        ("miscBits", ctypes.wintypes.UINT),
        ("RALT", ctypes.wintypes.FLOAT),
        ("bingoFuel", ctypes.wintypes.FLOAT),
        ("caraAlow", ctypes.wintypes.FLOAT),
        ("bullseyeX", ctypes.wintypes.FLOAT),
        ("bullseyeY", ctypes.wintypes.FLOAT),
        ("BMSVersionMajor", ctypes.wintypes.INT),
        ("BMSVersionMinor", ctypes.wintypes.INT),
        ("BMSVersionMicro", ctypes.wintypes.INT),
        ("BMSBuildNumber", ctypes.wintypes.INT),
        ("StringAreaSize", ctypes.wintypes.UINT),
        ("StringAreaTime", ctypes.wintypes.UINT),
        ("DrawingAreaSize", ctypes.wintypes.UINT),

        ("turnRate", ctypes.wintypes.FLOAT),
)

class INTELLIVIBEDATA(ctypes.Structure):
    _fields_ = (
        ("AAMissileFired", ctypes.wintypes.BYTE),
        ("AGMissileFired", ctypes.wintypes.BYTE),
        ("BombDropped", ctypes.wintypes.BYTE),
        ("FlareDropped", ctypes.wintypes.BYTE),
        ("ChaffDropped", ctypes.wintypes.BYTE),
        ("BulletsFired", ctypes.wintypes.BYTE),
        ("CollisionCounter", ctypes.wintypes.INT),
        ("IsFiringGun", ctypes.wintypes.BOOLEAN),
        ("IsEndFlight", ctypes.wintypes.BOOLEAN),
        ("IsEjecting", ctypes.wintypes.BOOLEAN),
        ("In3D", ctypes.wintypes.BOOLEAN),
        ("IsPaused", ctypes.wintypes.BOOLEAN),
        ("IsFrozen", ctypes.wintypes.BOOLEAN),
        ("IsOverG", ctypes.wintypes.BOOLEAN),
        ("IsOnGround", ctypes.wintypes.BOOLEAN),
        ("IsExitGame", ctypes.wintypes.BOOLEAN),
        ("Gforce", ctypes.wintypes.FLOAT),
        ("eyex", ctypes.wintypes.FLOAT),
        ("eyey", ctypes.wintypes.FLOAT),
        ("eyez", ctypes.wintypes.FLOAT),
        ("lastdamage", ctypes.wintypes.INT),
        ("damageforce", ctypes.wintypes.FLOAT),
        ("whendamage", ctypes.wintypes.INT)
)

_pFlightData = None
_pFlightData2 = None
_pIntellivibeData = None

def getFlightData():
    global _pFlightData
    if _pFlightData == None:
        handle = ctypes.windll.kernel32.OpenFileMappingA(FILE_MAP_READ|FILE_MAP_WRITE, False, "FalconSharedMemoryArea".encode())
        if handle:
            ctypes.windll.kernel32.MapViewOfFile.restype = ctypes.POINTER(FLIGHTDATA)
            _pFlightData = ctypes.windll.kernel32.MapViewOfFile(handle, FILE_MAP_READ|FILE_MAP_WRITE, 0, 0, 0)
    if _pFlightData == None:
        raise EnvironmentError("can't access falcon shared memory area")
    return _pFlightData.contents

def getFlightData2():
    global _pFlightData2
    if _pFlightData2 == None:
        handle = ctypes.windll.kernel32.OpenFileMappingA(FILE_MAP_READ|FILE_MAP_WRITE, False, "FalconSharedMemoryArea2".encode())
        if handle:
            ctypes.windll.kernel32.MapViewOfFile.restype = ctypes.POINTER(FLIGHTDATA2)
            _pFlightData2 = ctypes.windll.kernel32.MapViewOfFile(handle, FILE_MAP_READ|FILE_MAP_WRITE, 0, 0, 0)
    if not _pFlightData2:
        raise EnvironmentError("can't access falcon shared memory area")
    return _pFlightData2.contents

def getIntellivibeData():
    global _pIntellivibeData
    if _pIntellivibeData == None:
        handle = ctypes.windll.kernel32.OpenFileMappingA(FILE_MAP_READ|FILE_MAP_WRITE, False, "FalconIntellivibeSharedMemoryArea".encode())
        if handle:
            ctypes.windll.kernel32.MapViewOfFile.restype = ctypes.POINTER(INTELLIVIBEDATA)
            _pIntellivibeData = ctypes.windll.kernel32.MapViewOfFile(handle, FILE_MAP_READ|FILE_MAP_WRITE, 0, 0, 0)
    if not _pIntellivibeData:
        raise EnvironmentError("can't access falcon shared memory area")
    return _pIntellivibeData.contents
#  end MIT license --->

# generating keyboard events; see https://stackoverflow.com/a/23468236
# <--- start license: Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
# end CC BY-SA 3.0 license--->

def send_key(keycode, modifier):
    if modifier == "0":
        PressKey(keycode)
        ReleaseKey(keycode)
    elif modifier == "1":
        PressKey(0x2a)
        PressKey(keycode)
        ReleaseKey(keycode)
        ReleaseKey(0x2a)
    elif modifier == "2":
        PressKey(0x1d)
        PressKey(keycode)
        ReleaseKey(keycode)
        ReleaseKey(0x1d)
    elif modifier == "3":
        PressKey(0x1d)
        PressKey(0x2a)
        PressKey(keycode)
        ReleaseKey(keycode)
        ReleaseKey(0x2a)
        ReleaseKey(0x1d)
    elif modifier == "4":
        PressKey(0x38 + 2048)
        PressKey(keycode)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
    elif modifier == "5":
        PressKey(0x38 + 2048)
        PressKey(0x2a)
        PressKey(keycode)
        ReleaseKey(keycode)
        ReleaseKey(0x2a)
        ReleaseKey(0x38 + 2048)
    elif modifier == "6":
        PressKey(0x1d)
        PressKey(0x38 + 2048)
        PressKey(keycode)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
        ReleaseKey(0x1d)
    elif modifier == "7":
        PressKey(0x1d)
        PressKey(0x2a)
        PressKey(0x38 + 2048)
        PressKey(keycode)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
        ReleaseKey(0x2a)
        ReleaseKey(0x1d)

def get_keyfile_content(keyfile):
    keyfile_content = []
    keyfile_file = open(keyfile, "r")
    for line in keyfile_file:
        if line.startswith("#") or line.startswith("SimDoNothing"):
            continue
        try:
            if line.split(" ")[3].upper() != "0XFFFFFFFF":
                keyfile_content.append(line.strip().split(" ")[:8])
        except IndexError:
            pass
    return keyfile_content

def check_required_callbacks(keyfile_content):
    for line in keyfile_content:
        if line[0] in REQUIRED_CALLBACKS and line[3].upper() == "0XFFFFFFFF":
            print("Not all callbacks assigned.")
            print("See README for needed callbacks in the keyfile.")
            input("Press ENTER to exit")
            sys.exit(1)

def randomize_cockpit(keyfile_content):
	# randomizes the cockpit by simply triggering each callback a random
	# number of times.
	# switches and dials that can't be cycled (for example the air source)
    # would always get set to the state that's placed last in the keyfile.
    # that's why the shuffle is needed to make them random as well.
    random.shuffle(keyfile_content)
    for line in keyfile_content:
        if line[0] in REQUIRED_CALLBACKS:
            for rep in range(0, random.randint(1,6)):
                toggle_callback(line)

def toggle_callback(keyfile_line):
    send_key(int(keyfile_line[3], 16), keyfile_line[4])
	# adds slight delay, had issues without it
    time.sleep(0.01)

def main():
    keyfile_content = get_keyfile_content(KEYFILE)
    check_required_callbacks(keyfile_content)

    cockpit_randomized = 0

    while True:
        try:
            in_3d = getIntellivibeData().In3D
            on_ground = getIntellivibeData().IsOnGround
            end_flight = getIntellivibeData().IsEndFlight
            main_power = getFlightData().MainPower
            cmds_mode = getFlightData2().cmdsMode
        except:
            continue

        if in_3d and on_ground and not main_power and not cockpit_randomized and cmds_mode == 1:
            randomize_cockpit(keyfile_content)
            cockpit_randomized = 1
        elif cockpit_randomized and end_flight and not in_3d:
            cockpit_randomized = 0

        time.sleep(REFRESH_FREQUENCY)

main()

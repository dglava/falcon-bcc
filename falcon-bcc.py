#!/usr/bin/python

# Falcon-BCC
# Copyright 2021-2024 Dino Duratović

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
import struct
import time
import random
import winsound
from enum import IntEnum
import mmap
import itertools
import shutil

REFRESH_FREQUENCY = 2

REQUIRED_CALLBACKS = [
    "SimProbeHeatOn", "SimProbeHeatOff", "SimProbeHeatTest",
    "SimDigitalBUP", "SimAltFlaps", "SimManualFlyup", "SimLEFLockSwitch",
    "SimTrimAPDisc",
    "SimToggleMasterFuel", "SimFuelPumpOff", "SimFuelPumpNorm", "SimFuelPumpAft", "SimFuelPumpFwd", "SimFuelDoorToggle",
    "SimIFFMasterOff", "SimIFFMasterStby", "SimIFFMasterLow", "SimIFFMasterNorm", "SimIFFMasterEmerg", "SimToggleAuxComMaster",
    "SimIFFMode4ReplyCycle", "SimIFFMode4MonitorToggle", "SimToggleAuxComAATR", "SimIFFEnableCycle",
    "SimExtlAntiColl", "SimAntiColModeOff", "SimAntiColMode1", "SimAntiColMode2", "SimAntiColMode3", "SimAntiColMode4", "SimAntiColModeA"
    "SimAntiColModeB", "SimAntiColModeC", "SimExtlSteady", "SimWingLightCycle", "SimFuselageLightCycle", "SimExtlPower", "SimStepAARLightsUp", "SimStepAARLightsDown",
    "SimEpuToggle",
    "SimAVTRSwitch",
    "SimEcmPower", "SimXMit1", "SimXMit2", "SimXMit3",
    "SimEngCont",
    "SimAud1Com1", "SimAud1Com2",
    "SimMPOToggle",
    "SimBupUhfOff", "SimBupUhfMain", "SimBupUhfBoth", "SimBupUhfManual", "SimBupUhfPreset", "SimBupUhfGuard",
    "SimSeatArm",
    "SimEWSRWRPower", "SimEWSJammerPower", "SimEWSMwsPower", "SimEWSO1Power", "SimEWSO2Power", "SimEWSChaffPower", "SimEWSFlarePower", "SimEWSDispPower",
    "SimEwsJett", "SimEWSProgOne", "SimEWSProgTwo", "SimEWSProgThree", "SimEWSProgFour", "SimEWSModeOff", "SimEWSModeStby", "SimEWSModeMan",
    "SimEWSModeSemi", "SimEWSModeAuto", "SimEWSModeByp",
    "SimGndJettEnable", "SimBrakeChannelToggle", "SimParkingBrakeCycle", "SimCATSwitch", "SimLandingLightCycle",
    "SimRFSwitch", "SimLaserArmToggle", "SimStepMasterArm", "SimLeftAPSwitch", "SimRightAPSwitch",
    "SimDriftCO",
    "SimStepHSIMode",
    "SimFuelSwitchTest", "SimFuelSwitchNorm", "SimFuelSwitchResv", "SimFuelSwitchWingInt", "SimFuelSwitchWingExt", "SimFuelSwitchCenterExt", "SimExtFuelTrans",
    "SimLeftHptPower", "SimRightHptPower", "SimFCRPower", "SimRALTON", "SimRALTSTDBY", "SimRALTOFF",
    "SimHUDScales", "SimScalesVVVAH", "SimHUDFPM", "SimHUDDED", "SimReticleSwitch", "SimHUDVelocity", "SimHUDRadar", "SimHUDBrightness",
    "SimInstrumentLight", "SimDedBrightness", "SimInteriorLight",
    "SimAirSourceOff", "SimAirSourceNorm", "SimAirSourceDump", "SimAirSourceRam",
    "SimInhibitVMS",
    "SimAntiIceCycle", "SimAntennaSelectCycle",
    "SimINSOff", "SimINSNorm", "SimINSNav", "SimINSInFlt", "SimFCCPower", "SimSMSPower", "SimMFDPower", "SimUFCPower", "SimGPSPower",
    "SimDLPower", "SimMIDSLVTOff", "SimMIDSLVTOn", "SimMAPPower",
]

KEYBOARD_SCANCODES = [
    "0X2", #1
    "0X3", #2
    "0X4", #3
    "0X5", #4
    "0X6", #5
    "0X7", #6
    "0X8", #7
    "0X9", #8
    "0XA", #9
    "0XB", #0
    "0XC", #Dash(Minus) / Underscore
    "0XD", #Equals / Plus
    "0XE", #Backspace
    "0X16", #U
    "0X17", #I
    "0X18", #O
    "0X19", #P
    "0X1A", #Left Brace
    "0X1B", #Right Brace
    "0X1E", #A
    "0X1F", #S
    "0X20", #D
    "0X22", #G
    "0X23", #H
    "0X24", #J
    "0X25", #K
    "0X26", #L
    "0X27", #Semicolon / Colon
    "0X28", #Apostrophe / Doublequote
    "0X29", #Backquote / Tilde
    "0X2B", #Backslash / Pipe
    "0X2C", #Z
    "0X2D", #X
    "0X2E", #C
    "0X2F", #V
    "0X30", #B
    "0X31", #N
    "0X32", #M
    "0X33", #Comma / Left Bracket
    "0X34", #Period / Right Bracket
    "0X35", #Slash / Question Mark
    "0X37", #Keypad Asterisk
    "0X39", #Spacebar
    "0X3A", #Caps Lock
    "0X3B", #F1
    "0X3C", #F2
    "0X3D", #F3
    "0X3E", #F4
    "0X3F", #F5
    "0X40", #F6
    "0X41", #F7
    "0X42", #F8
    "0X43", #F9
    "0X44", #F10
    "0X46", #Scroll Lock
    "0X47", #Keypad 7
    "0X48", #Keypad 8
    "0X49", #Keypad 9
    "0X4A", #Keypad Dash(Minus)
    "0X4B", #Keypad 4
    "0X4C", #Keypad 5
    "0X4D", #Keypad 6
    "0X4E", #Keypad Plus
    "0X4F", #Keypad 1
    "0X50", #Keypad 2
    "0X51", #Keypad 3
    "0X52", #Keypad 0
    "0X57", #F11
    "0X58", #F12
    "0X9C", #Keypad Enter
    "0XB5", #Keypad Slash(Divide)
    "0XC7", #Home
    "0XC8", #Up Arrow
    "0XC9", #PgUp
    "0XCB", #Left Arrow
    "0XCD", #Right Arrow
    "0XCF", #End
    "0XD0", #Down Arrow
    "0XD1", #PgDown
    "0XD2", #Insert
]

class FlightData(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("xDot", ctypes.c_float),
        ("yDot", ctypes.c_float),
        ("zDot", ctypes.c_float),
        ("alpha", ctypes.c_float),
        ("beta", ctypes.c_float),
        ("gamma", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float),
        ("yaw", ctypes.c_float),
        ("mach", ctypes.c_float),
        ("kias", ctypes.c_float),
        ("vt", ctypes.c_float),
        ("gs", ctypes.c_float),
        ("windOffset", ctypes.c_float),
        ("nozzlePos", ctypes.c_float),
        ("internalFuel", ctypes.c_float),
        ("externalFuel", ctypes.c_float),
        ("fuelFlow", ctypes.c_float),
        ("rpm", ctypes.c_float),
        ("ftit", ctypes.c_float),
        ("gearPos", ctypes.c_float),
        ("speedBrake", ctypes.c_float),
        ("epuFuel", ctypes.c_float),
        ("oilPressure", ctypes.c_float),
        ("lightBits", ctypes.c_uint),
        ("headPitch", ctypes.c_float),
        ("headRoll", ctypes.c_float),
        ("headYaw", ctypes.c_float),
        ("lightBits2", ctypes.c_uint),
        ("lightBits3", ctypes.c_uint),
        ("ChaffCount", ctypes.c_float),
        ("FlareCount", ctypes.c_float),
        ("NoseGearPos", ctypes.c_float),
        ("LeftGearPos", ctypes.c_float),
        ("RightGearPos", ctypes.c_float),
        ("AdiIlsHorPos", ctypes.c_float),
        ("AdiIlsVerPos", ctypes.c_float),
        ("courseState", ctypes.c_int),
        ("headingState", ctypes.c_int),
        ("totalStates", ctypes.c_int),
        ("courseDeviation", ctypes.c_float),
        ("desiredCourse", ctypes.c_float),
        ("distanceToBeacon", ctypes.c_float),
        ("bearingToBeacon", ctypes.c_float),
        ("currentHeading", ctypes.c_float),
        ("desiredHeading", ctypes.c_float),
        ("deviationLimit", ctypes.c_float),
        ("halfDeviationLimit", ctypes.c_float),
        ("localizerCourse", ctypes.c_float),
        ("airbaseX", ctypes.c_float),
        ("airbaseY", ctypes.c_float),
        ("totalValues", ctypes.c_float),
        ("TrimPitch", ctypes.c_float),
        ("TrimRoll", ctypes.c_float),
        ("TrimYaw", ctypes.c_float),
        ("hsiBits", ctypes.c_uint),
        ("DEDLines", ctypes.c_char * 5 * 26),
        ("Invert", ctypes.c_char * 5 * 26),
        ("PFLLines", ctypes.c_char * 5 * 26),
        ("PFLInvert", ctypes.c_char * 5 * 26),
        ("UFCTChan", ctypes.c_int),
        ("AUXTChan", ctypes.c_int),
        ("RwrObjectCount", ctypes.c_int),
        ("RWRsymbol", ctypes.c_int * 40),
        ("bearing", ctypes.c_float * 40),
        ("missileActivity", ctypes.c_ulong * 40),
        ("missileLaunch", ctypes.c_ulong * 40),
        ("selected", ctypes.c_ulong * 40),
        ("lethality", ctypes.c_float * 40),
        ("newDetection", ctypes.c_ulong * 40),
        ("fwd", ctypes.c_float),
        ("aft", ctypes.c_float),
        ("total", ctypes.c_float),
        ("VersionNum", ctypes.c_int),
        ("headX", ctypes.c_float),
        ("headY", ctypes.c_float),
        ("headZ", ctypes.c_float),
        ("MainPower", ctypes.c_int),
        ]

class FlightData2(ctypes.Structure):
    _fields_ = [
        ("nozzlePos2", ctypes.c_float),
        ("rpm2", ctypes.c_float),
        ("ftit2", ctypes.c_float),
        ("oilPressure2", ctypes.c_float),
        ("navMode", ctypes.c_byte),
        ("AAUZ", ctypes.c_float),
        ("tacanInfo", ctypes.c_char * 2),
        ("AltCalReading", ctypes.c_int),
        ("altBits", ctypes.c_uint),
        ("powerBits", ctypes.c_uint),
        ("blinkBits", ctypes.c_uint),
        ("cmdsMode", ctypes.c_int),
        ("uhf_panel_preset", ctypes.c_int),
        ("uhf_panel_frequency", ctypes.c_int),
        ("cabinAlt", ctypes.c_float),
        ("hydPressureA", ctypes.c_float),
        ("hydPressureB", ctypes.c_float),
        ("currentTime", ctypes.c_int),
        ("vehicleACD", ctypes.c_short),
        ("VersionNum", ctypes.c_int),
        ("fuelFlow2", ctypes.c_float),
        ("RwrInfo", ctypes.c_char * 512),
        ("lefPos", ctypes.c_float),
        ("tefPos", ctypes.c_float),
        ("vtolPos", ctypes.c_float),
        ("pilotsOnline", ctypes.c_char),
        ("pilotsCallsign", (ctypes.c_char * 12) * 32),
        ("pilotsStatus", ctypes.c_char * 32),
        ("bumpIntensity", ctypes.c_float),
        ("latitude", ctypes.c_float),
        ("longitude", ctypes.c_float),
        ("RTT_size", ctypes.c_ushort * 2),
        ("RTT_area", (ctypes.c_ushort * 7) * 4),
        ("iffBackupMode1Digit1", ctypes.c_char),
        ("iffBackupMode1Digit2", ctypes.c_char),
        ("iffBackupMode3ADigit1", ctypes.c_char),
        ("iffBackupMode3ADigit2", ctypes.c_char),
        ("instrLight", ctypes.c_char),
        ("bettyBits", ctypes.c_uint),
        ("miscBits", ctypes.c_uint),
        ("RALT", ctypes.c_float),
        ("bingoFuel", ctypes.c_float),
        ("caraAlow", ctypes.c_float),
        ("bullseyeX", ctypes.c_float),
        ("bullseyeY", ctypes.c_float),
        ("BMSVersionMajor", ctypes.c_int),
        ("BMSVersionMinor", ctypes.c_int),
        ("BMSVersionMicro", ctypes.c_int),
        ("BMSBuildNumber", ctypes.c_int),
        ("StringAreaSize", ctypes.c_uint),
        ("StringAreaTime", ctypes.c_uint),
        ("DrawingAreaSize", ctypes.c_uint),
        ("turnRate", ctypes.c_float),
        ("floodConsole", ctypes.c_char),
        ("magDeviationSystem", ctypes.c_float),
        ("magDeviationReal", ctypes.c_float),
        ("ecmBits", ctypes.c_uint * 5),
        ("ecmOper", ctypes.c_char),
        ("RWRjammingStatus", ctypes.c_char * 40),
        ("radio2_preset", ctypes.c_int),
        ("radio2_frequency", ctypes.c_int),
        ("iffTransponderActiveCode1", ctypes.c_char),
        ("iffTransponderActiveCode2", ctypes.c_short),
        ("iffTransponderActiveCode3A", ctypes.c_short),
        ("iffTransponderActiveCodeC", ctypes.c_short),
        ("iffTransponderActiveCode4", ctypes.c_short),
        ]

class IntellivibeData(ctypes.Structure):
    _fields_ = [
        ("AAMissileFired", ctypes.c_ubyte),
        ("AGMissileFired", ctypes.c_ubyte),
        ("BombDropped", ctypes.c_ubyte),
        ("FlareDropped", ctypes.c_ubyte),
        ("ChaffDropped", ctypes.c_ubyte),
        ("BulletsFired", ctypes.c_ubyte),
        ("CollisionCounter", ctypes.c_int),
        ("IsFiringGun", ctypes.c_bool),
        ("IsEndFlight", ctypes.c_bool),
        ("IsEjecting", ctypes.c_bool),
        ("In3D", ctypes.c_bool),
        ("IsPaused", ctypes.c_bool),
        ("IsFrozen", ctypes.c_bool),
        ("IsOverG", ctypes.c_bool),
        ("IsOnGround", ctypes.c_bool),
        ("IsExitGame", ctypes.c_bool),
        ("Gforce", ctypes.c_float),
        ("eyex", ctypes.c_float),
        ("eyey", ctypes.c_float),
        ("eyez", ctypes.c_float),
        ("lastdamage", ctypes.c_int),
        ("damageforce", ctypes.c_float),
        ("whendamage", ctypes.c_uint),
        ]

class Strings():
    pass

def read_shared_memory(shared_mem_class):
    """Falcon BMS shared memory reader.

    There are 2 different routines: one for the strings (info about
    various directories) and one for all other data (FlightData, FlightData2,
    IntellivibeData). The latter ones are returned as a ctypes structure
    with every available field exposed by the shared memory.
    For the former one, the Strings, it returns a list with every directory.
    """
    shared_mem = shared_mem_class.__name__
    shared_mem_names = {
        "FlightData": "FalconSharedMemoryArea",
        "FlightData2": "FalconSharedMemoryArea2",
        "IntellivibeData": "FalconIntellivibeSharedMemoryArea",
        "Strings": "FalconSharedMemoryAreaString"
    }
    shared_mem_sizes = {
        "FlightData": ctypes.sizeof(FlightData),
        "FlightData2": ctypes.sizeof(FlightData2),
        "IntellivibeData": ctypes.sizeof(IntellivibeData),
        "Strings": 1024 * 1024
    }

    try:
        shm = mmap.mmap(-1, shared_mem_sizes[shared_mem], shared_mem_names[shared_mem], access=mmap.ACCESS_READ)
        if shared_mem != "Strings":
            buffer = shm.read(shared_mem_sizes[shared_mem])
            data = shared_mem_class.from_buffer_copy(buffer)
            shm.close()
            return data
        else:
            version_num = struct.unpack('I', shm.read(4))[0]
            num_strings = struct.unpack('I', shm.read(4))[0]
            data_size = struct.unpack('I', shm.read(4))[0]
            strings_list = []
            for _ in range(num_strings):
                str_id = struct.unpack('I', shm.read(4))[0]
                str_length = struct.unpack('I', shm.read(4))[0]
                str_data = shm.read(str_length + 1).decode('utf-8').rstrip('\x00')
                strings_list.append(str_data)
            return strings_list
    except Exception as e:
        notify("Error reading shared memory '{name}': {e}".format(shared_mem, e))
        return None

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

def send_key(key, modifier):
    # TODO: look into this some more
    # the key is passed as a hex string, but it expects an int
    keycode = int(key, 16)
    # without a delay, it seems to fail when a bunch of modifiers are pressed
    # TODO: fix the ugly delays for complex modifier buttons
    # complex modifier combons (ctrl+alt+shift) seemed to have issues
    delay = 0.01
    if modifier == "0":
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
    elif modifier == "1":
        PressKey(0x2a)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x2a)
    elif modifier == "2":
        PressKey(0x1d)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x1d)
    elif modifier == "3":
        PressKey(0x1d)
        time.sleep(delay)
        PressKey(0x2a)
        time.sleep(delay)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x2a)
        ReleaseKey(0x1d)
    elif modifier == "4":
        PressKey(0x38 + 2048)
        time.sleep(delay)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
# Alt+Shift modifier removed; see get_unused_keys()
#    elif modifier == "5":
#        PressKey(0x38 + 2048)
#        time.sleep(delay)
#        PressKey(0x2a)
#        PressKey(keycode)
#        time.sleep(delay)
#        ReleaseKey(keycode)
#        ReleaseKey(0x2a)
#        ReleaseKey(0x38 + 2048)
    elif modifier == "6":
        PressKey(0x1d)
        time.sleep(delay)
        PressKey(0x38 + 2048)
        time.sleep(delay)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
        ReleaseKey(0x1d)
    elif modifier == "7":
        PressKey(0x1d)
        time.sleep(delay)
        PressKey(0x2a)
        time.sleep(delay)
        PressKey(0x38 + 2048)
        time.sleep(delay)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
        ReleaseKey(0x2a)
        ReleaseKey(0x1d)

def notify(message):
    """Prefix every printed message."""
    print("[Falcon-BCC]: {}".format(message))

def get_keyfile_path():
    """Get the keyfile path from the shared memory.

    Returns a string with the path to the keyfile."""
    shared_mem_strings = read_shared_memory(Strings)
    notify("Using keyfile: {}".format(shared_mem_strings[1]))
    return shared_mem_strings[1]

def get_keyfile_content(keyfile_path):
    """Get the keyfile content from the keyfile path.

    Returns a list of lists with each element holding one line of the keyfile."""
    fajl = open(keyfile_path, "r")
    lines = []
    for line in fajl:
        # keep the whitespace
        if line == "\n":
            lines.append([line])
        else:
            lines.append(line.split())
    return lines

def get_filtered_keyfile(keyfile_content):
    """Filters the keyfile content.

    Removes commented out lines, lines which are not callbacks (SimDoNothing), empty
    lines and DirectX button assigment lines and joins the UI description into a single string.
    Returns a list of lists with each element holding one line of the keyfile."""
    filtered_keyfile = []
    for line in keyfile_content:
        if line[0].startswith("#") or line[0] == "SimDoNothing" or line[0] == "\n" or len(line) == 7:
            continue
        else:
            # joins every element after the 8th into a string (UI description)
            line[8:] = [" ".join(line[8:])]
            # use all caps in the hex codes to avoid duplicate issues
            line[3] = line[3].upper()
            filtered_keyfile.append(line)
    return filtered_keyfile

def get_assigned_callbacks(keyfile_content):
    """Get the assigned callbacks from the keyfile content.

    Returns a list with only the callbacks which are assigned to a key."""
    assigned_callbacks = []
    for line in keyfile_content:
        if line[3].upper() != "0XFFFFFFFF":
            assigned_callbacks.append(line[0])
    return assigned_callbacks

def get_unassigned_callbacks(assigned_callbacks):
    """Get callbacks which aren't assigned yet

    Compares the callbacks which have been assigned to the required
    callbacks and returns a list with callbacks that aren't assigned."""
    unassigned_callbacks = []
    for callback in REQUIRED_CALLBACKS:
        if callback not in assigned_callbacks:
            unassigned_callbacks.append(callback)
    return unassigned_callbacks

def get_used_keys(keyfile_filtered):
    """Get assigned keyboard keys

    The assigned keys are the 3rd and 4th element of a line in a keyfile.
    The first is the keycode and the second one the modifier.
    Returns a list of tuples containing the keycode and modifier."""
    used_keys = []
    for line in keyfile_filtered:
        used_keys.append((line[3], line[4]))
    return used_keys

def get_unused_keys(used_keys):
    """Get unused keyboard keys

    Checks all the possible keyboard key combinations with the modifiers
    and removes those already in use in the keyfile.
    Returns a list of tuples containing the unused keycode and modifier."""
    # Remove Alt+Shift ("5") the default language switcher shortcut (makes the pop appear)
    modifiers = ["0", "1", "2", "3", "4", "6", "7"]

    all_possible_keys = itertools.product(KEYBOARD_SCANCODES, modifiers)
    unused_keys_set = set(all_possible_keys) - set(used_keys)
    unused_keys_list = sorted(list(unused_keys_set), key=lambda x: x[1])
    if len(unused_keys_list) < len(REQUIRED_CALLBACKS):
        notify("Warning: not enough unused keys to assign all the required callbacks")
        sys.exit(1)
    return unused_keys_list

def assign_unused_callbacks(unassigned_callbacks, unused_keys):
    """Assign unused callbacks to unused keys

    Goes through every unassigned callback and assigns it to an unused key.
    Returns a list of properly formatted Falcon BMS keyfile lines."""
    new_assigned_lines = []
    # TODO: modify to keep the sound ID (2nd part of the line, currently always -1)
    callback_template = '{} -1 0 {} {} 0 0 1 "GeneratedByFalcon-BCC"'
    for cb in unassigned_callbacks:
        key, mod = unused_keys.pop(0)
        new_callback = callback_template.format(cb, key, mod)
        new_callback_line = new_callback.split()
        new_assigned_lines.append(new_callback_line)
    return new_assigned_lines

def backup_keyfile(original_keyfile_path):
    """Back the original keyfile up by copying it to a .bak file."""
    backup_keyfile_path = "{}.bak".format(original_keyfile_path)
    shutil.copy2(original_keyfile_path, backup_keyfile_path)
    notify("Original Keyfile backed up to: {}".format(backup_keyfile_path))

def write_new_keyfile(original_keyfile_content, new_callbacks_content, keyfile_path):
    """Create the new keyfile.

    It comments out the original callback line for the new callbacks we added to keep
    the file integrity. It also keeps newlines as per the original file."""
    single_new_callbacks = [x[0] for x in new_callbacks_content]

    with open(keyfile_path, "w") as keyfile:
        for line in original_keyfile_content:
            if line[0] in single_new_callbacks:
                # comments out the assigned callbacks; we will add them below
                keyfile.write("#{}\n".format(" ".join(line)))
            elif line[0] == "\n":
                keyfile.write("\n")
            else:
                keyfile.write("{}\n".format(" ".join(line)))

        keyfile.write("\n### Generated by Falcon-BCC ###\n")
        for line in new_callbacks_content:
            joined_line = " ".join(line)
            keyfile.write("{}\n".format(joined_line))
    notify("All required callbacks added to Keyfile: {}".format(keyfile_path))

def falcon_running():
    """Return True if Falcon BMS is running

    It checks whether it's running by trying to read the shared memory.
    """
    shared_mem_strings = read_shared_memory(Strings)
    if shared_mem_strings and shared_mem_strings[1]:
        return True

def process_keyfile():
    """Process the keyfile

    The routine for the keyfile part: gets its path and reads the keyfile, filters
    only the useful lines out, gets all the assigned and unassigned callbacks and
    finally writes it to our keyfile if necessary.
    Returns a string with the path of the used keyfile."""
    keyfile_path = get_keyfile_path()
    keyfile_content = get_keyfile_content(keyfile_path)
    filtered_keyfile = get_filtered_keyfile(keyfile_content)
    assigned_callbacks = get_assigned_callbacks(filtered_keyfile)
    unassigned_callbacks = get_unassigned_callbacks(assigned_callbacks)
    if unassigned_callbacks:
        used_keys = get_used_keys(filtered_keyfile)
        unused_keys = get_unused_keys(used_keys)
        new_callbacks_content = assign_unused_callbacks(unassigned_callbacks, unused_keys)
        backup_keyfile(keyfile_path)
        write_new_keyfile(keyfile_content, new_callbacks_content, keyfile_path)
    else:
        notify("Keyfile verified: all required callbacks assigned.")
    return keyfile_path, keyfile_content

def randomize_cockpit(keyfile_content):
    """Randomize the cockpit

    Randomizes the cockpit by simply triggering each callback a random number of times.
    Switches and dials that can't be cycled (for example the air source) would always
    get set to the state that's placed last in the keyfile. That's why the shuffle is
    needed to make them random as well.
    """
    winsound.PlaySound("Notification.Proximity", winsound.SND_ALIAS | winsound.SND_LOOP | winsound.SND_ASYNC)
    random.shuffle(keyfile_content)
    # TODO: use cached callbacks from somewhere else, don't go through whole keyfile again
    for line in keyfile_content:
        if line[0] in REQUIRED_CALLBACKS:
            for rep in range(0, random.randint(1,6)):
                send_key(line[3], line[4])
    winsound.PlaySound(None, winsound.SND_FILENAME)
    notify("Cockpit randomized!")

def main():
    """Main function

    It waits for Falcon BMS to start, processes the keyfile, and then enters the main
    loop where it randomizes the cockpit and listens for the end of the flight.
    The criteria for an eligible randomization are that we're in 3D, the plane is on
    the ground, main power is not on, the cockpit isn't already randomized and the CMDS
    mode is in STDBY (1)."""
    notify("Waiting for Falcon BMS to start")
    while not falcon_running():
        time.sleep(REFRESH_FREQUENCY)

    keyfile_path, keyfile_content = process_keyfile()
    cockpit_randomized = 0
    notify("Ready: Move the CMDS knob to STBY to start randomizing")

    while falcon_running():
        fd = read_shared_memory(FlightData)
        fd2 = read_shared_memory(FlightData2)
        ivd = read_shared_memory(IntellivibeData)
        strd = read_shared_memory(Strings)

        if strd[1] != keyfile_path:
            notify("\tKeyfile changed, reprocessing...")
            keyfile_path, keyfile_content = process_keyfile()
            notify("Ready: Move the CMDS knob to STBY to start randomizing")

        in_3d = ivd.In3D
        on_ground = ivd.IsOnGround
        end_flight = ivd.IsEndFlight
        main_power = fd.MainPower
        cmds_mode = fd2.cmdsMode
        if in_3d and on_ground and not main_power and not cockpit_randomized and cmds_mode == 1:
            randomize_cockpit(keyfile_content)
            cockpit_randomized = 1
        elif cockpit_randomized and end_flight and not in_3d:
            notify("Left 3D, cockpit randomization rearmed")
            cockpit_randomized = 0
        time.sleep(REFRESH_FREQUENCY)
    notify("Falcon BMS not running. Exiting")

main()

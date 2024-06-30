#!/usr/bin/python

# Falcon-BCC
# Copyright 2021-2023 Dino Duratović

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
import struct
import time
import random
import winsound
import os.path
from enum import IntEnum
import mmap

KEYFILE = r"C:\Falcon BMS\User\Config\your.key"
REQUIRED_CALLBACKS = [
    "SimProbeHeatOn", "SimProbeHeatOff", "SimProbeHeatTest",
    "SimFuelPumpOff", "SimFuelPumpNorm", "SimFuelPumpAft", "SimFuelPumpFwd",
    "SimIFFMasterOff", "SimIFFMasterStby", "SimIFFMasterLow", "SimIFFMasterNorm", "SimIFFMasterEmerg",
    "SimBupUhfOff", "SimBupUhfMain", "SimBupUhfBoth",
    "SimBupUhfPreset", "SimBupUhfGuard", "SimBupUhfManual",
    "SimEWSModeOff", "SimEWSModeStby", "SimEWSModeMan", "SimEWSModeSemi", "SimEWSModeAuto", "SimEWSModeByp",
    "SimEWSProgOne", "SimEWSProgTwo", "SimEWSProgThree", "SimEWSProgFour",
    "SimRALTSTDBY", "SimRALTON", "SimRALTOFF",
    "SimAirSourceOff", "SimAirSourceNorm", "SimAirSourceDump", "SimAirSourceRam",
    "SimINSOff", "SimINSNorm", "SimINSNav",
    "SimFuelSwitchTest", "SimFuelSwitchNorm", "SimFuelSwitchResv", "SimFuelSwitchWingInt", "SimFuelSwitchWingExt", "SimFuelSwitchCenterExt",
    "SimExtlAntiColl",
    "SimAntiColModeOff", "SimAntiColMode1", "SimAntiColMode2", "SimAntiColMode3", "SimAntiColMode4", "SimAntiColModeA", "SimAntiColModeB", "SimAntiColModeC",
    "SimExtlSteady",
    "SimWingLightCycle",
    "SimFuselageLightCycle",
    "SimExtlPower",
    "SimExtlMasterOff", "SimExtlMasterCovertAll", "SimExtlMasterCovertAC", "SimExtlMasterCovertForm", "SimExtlMasterNorm",
    "SimEcmPowerOn","SimEcmPowerOff",
    "SimXMTASPISToggle",

    "SimEpuToggle",
    "SimLandingLightCycle",
    "SimParkingBrakeCycle",
    "SimLeftAPSwitch",
    "SimStepMasterArm",
    "SimDriftCO",
    "SimStepHSIMode",
    "SimRFSwitch",
    "SimAntennaSelectCycle",
    "SimAntiIceCycle",
    "SimHUDVelocity",
    "SimHUDRadar",
    "SimHUDBrightness",
    "SimReticleSwitch",
    "SimHUDDED",
    "SimAud1Com1",
    "SimAud1Com2",
    "SimDigitalBUP",
    "SimAltFlaps",
    "SimManualFlyup",
    "SimLEFLockSwitch",
    "SimTrimAPDisc",
    "SimToggleMasterFuel",
    "SimToggleAuxComMaster",
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
    "SimMAPPower",
    "SimInhibitVMS"
]

BEEP = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + r"\beep.wav"
REFRESH_FREQUENCY = 2

FLIGHT_DATA_SHARED_MEMORY_NAME = "FalconSharedMemoryArea"
FLIGHT_DATA2_SHARED_MEMORY_NAME = "FalconSharedMemoryArea2"
INTELLIVIBE_SHARED_MEMORY_NAME = "FalconIntellivibeSharedMemoryArea"
STRING_SHARED_MEMORY_NAME = "FalconSharedMemoryAreaString"
STRINGDATA_AREA_SIZE_MAX = 1024 * 1024

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

class StringIdentifier(IntEnum):
    BmsExe = 0
    KeyFile = 1
    BmsBasedir = 2
    BmsBinDirectory = 3
    BmsDataDirectory = 4
    BmsUIArtDirectory = 5
    BmsUserDirectory = 6
    BmsAcmiDirectory = 7
    BmsBriefingsDirectory = 8
    BmsConfigDirectory = 9
    BmsLogsDirectory = 10
    BmsPatchDirectory = 11
    BmsPictureDirectory = 12
    ThrName = 13
    ThrCampaigndir = 14
    ThrTerraindir = 15
    ThrArtdir = 16
    ThrMoviedir = 17
    ThrUisounddir = 18
    ThrObjectdir = 19
    Thr3ddatadir = 20
    ThrMisctexdir = 21
    ThrSounddir = 22
    ThrTacrefdir = 23
    ThrSplashdir = 24
    ThrCockpitdir = 25
    ThrSimdatadir = 26
    ThrSubtitlesdir = 27
    ThrTacrefpicsdir = 28
    AcName = 29
    AcNCTR = 30
    ButtonsFile = 31
    CockpitFile = 32
    NavPoint = 33
    ThrTerrdatadir = 34

def read_shared_memory(name, size, data_class=None):
    try:
        shm = mmap.mmap(-1, size, name, access=mmap.ACCESS_READ)
        if data_class:
            buffer = shm.read(size)
            data = data_class.from_buffer_copy(buffer)
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

                identifier = StringIdentifier(str_id).name
                strings_list.append((identifier, str_data))
            return strings_list
    except Exception as e:
        print(f"Error reading shared memory '{name}': {e}")
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

def send_key(keycode, modifier):
    # without a delay, it seems to fail when a bunch of modifiers are pressed
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
        PressKey(0x2a)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x2a)
        ReleaseKey(0x1d)
    elif modifier == "4":
        PressKey(0x38 + 2048)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
    elif modifier == "5":
        PressKey(0x38 + 2048)
        PressKey(0x2a)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x2a)
        ReleaseKey(0x38 + 2048)
    elif modifier == "6":
        PressKey(0x1d)
        PressKey(0x38 + 2048)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
        ReleaseKey(0x1d)
    elif modifier == "7":
        PressKey(0x1d)
        PressKey(0x2a)
        PressKey(0x38 + 2048)
        PressKey(keycode)
        time.sleep(delay)
        ReleaseKey(keycode)
        ReleaseKey(0x38 + 2048)
        ReleaseKey(0x2a)
        ReleaseKey(0x1d)

def get_keyfile_content(keyfile):
    keyfile_content = []
    assigned_callbacks = []
    try:
        keyfile_file = open(keyfile, "r")
    except:
        print("Keyfile not found. Check config")
        input("Press ENTER to exit")
        sys.exit(1)

    for line in keyfile_file:
        if line.startswith("#") or line.startswith("SimDoNothing"):
            continue
        try:
            if line.split(" ")[3].upper() != "0XFFFFFFFF":
                keyfile_content.append(line.strip().split(" ")[:8])
                assigned_callbacks.append(line.strip().split(" ")[0])
        except IndexError:
            pass
    return keyfile_content, assigned_callbacks

def check_required_callbacks(assigned_callbacks):
    # check if every callback from REQUIRED_CALLBACKS is assigned in the keyfile
    if not all(callback in assigned_callbacks for callback in REQUIRED_CALLBACKS):
        missing_callbacks = []
        for cb in REQUIRED_CALLBACKS:
            if cb not in assigned_callbacks:
                missing_callbacks.append(cb)

        print("Not all callbacks from the REQUIRED_CALLBACKS assigned in keyfile.")
        print("Please edit your keyfile and assign keyboard keys to them.")
        print("\tMissing calbacks: {}".format(missing_callbacks))
        input("\nPress ENTER to exit")
        sys.exit(1)

def randomize_cockpit(keyfile_content):
    # randomizes the cockpit by simply triggering each callback a random
    # number of times.
    # switches and dials that can't be cycled (for example the air source)
    # would always get set to the state that's placed last in the keyfile.
    # that's why the shuffle is needed to make them random as well.
    winsound.PlaySound(BEEP, winsound.SND_LOOP | winsound.SND_ASYNC)
    random.shuffle(keyfile_content)
    for line in keyfile_content:
        if line[0] in REQUIRED_CALLBACKS:
            for rep in range(0, random.randint(1,6)):
                toggle_callback(line)
    winsound.PlaySound(None, winsound.SND_FILENAME)
    print("Randomized cockpit!")

def toggle_callback(keyfile_line):
    send_key(int(keyfile_line[3], 16), keyfile_line[4])

def main():
    keyfile_content, assigned_callbacks = get_keyfile_content(KEYFILE)
    check_required_callbacks(assigned_callbacks)

    cockpit_randomized = 0

    print("Waiting to randomize cockpit...")
    while True:
        try:
            fd = read_shared_memory(FLIGHT_DATA_SHARED_MEMORY_NAME, ctypes.sizeof(FlightData), FlightData)
            fd2 = read_shared_memory(FLIGHT_DATA2_SHARED_MEMORY_NAME, ctypes.sizeof(FlightData2), FlightData2)
            ivd = read_shared_memory(INTELLIVIBE_SHARED_MEMORY_NAME, ctypes.sizeof(IntellivibeData), IntellivibeData)

            in_3d = ivd.In3D
            on_ground = ivd.IsOnGround
            end_flight = ivd.IsEndFlight
            main_power = fd.MainPower
            cmds_mode = fd2.cmdsMode
        except:
            continue

        if in_3d and on_ground and not main_power and not cockpit_randomized and cmds_mode == 1:
            randomize_cockpit(keyfile_content)
            cockpit_randomized = 1
        elif cockpit_randomized and end_flight and not in_3d:
            cockpit_randomized = 0

        time.sleep(REFRESH_FREQUENCY)

main()

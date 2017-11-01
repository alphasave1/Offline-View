# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: ./res_mods\0.9.12\scripts\client\gui\mods\observer_utils\__init__.py
# Compiled at: 2015-11-17 03:50:54
import BigWorld
import ArenaType
import Event
import GUI
import game
import constants
from AvatarInputHandler import cameras
from ProjectileMover import collideDynamicAndStatic
from gui.Scaleform.Battle import Battle
from gui.app_loader import states
from gui.app_loader.loader import g_appLoader
from account_helpers.settings_core.IntUserSettings import IntUserSettings
from gui.battle_control.ChatCommandsController import ChatCommandsController
IS_DEV = False
IS_PHYSICS = False
IS_GUN_ROTATOR = False
IS_AVATAR_MODE = IS_PHYSICS or IS_GUN_ROTATOR
g_handleKeyEvent = Event.Event()
BigWorld_player = BigWorld.player

def LOG_DEBUG(msg):
    if IS_DEV:
        LOG_NOTE('[DEBUG] ' + msg)


def LOG_NOTE(msg):
    LOG_MSG('[OBSERVER] ' + msg)


def LOG_MSG(msg):
    print msg


class ObserverDP(object):
    vehicles = property(lambda self: self.__vehicles, lambda self, value: self.__set_attr('vehicles', value))
    vehicle = property(lambda self: self.__vehicle, lambda self, value: self.__set_attr('vehicle', value))
    vehicleCondition = property(lambda self: self.__vehicleCondition, lambda self, value: self.__set_attr('vehicleConditions', value))
    arenaData = property(lambda self: self.__arenaData, lambda self, value: self.__set_attr('arenaData', value))

    def __init__(self):
        self.onUpdateValue = Event.Event()
        self.__vehicles = {'ussr:R04_T-34': 'T-34'}
        self.__vehicle = 'ussr:R04_T-34'
        self.__vehicleCondition = 1
        self.__arenaData = ()

    def __set_attr(self, name, value):
        LOG_DEBUG('onUpdateValue(): name=%s | value=%s' % (name, value))
        setattr(self, '_ObserverDP__' + name, value)
        self.onUpdateValue(name, value)


g_observerDP = ObserverDP()
states_isBattleReplayPlaying_old = states._isBattleReplayPlaying
states._isBattleReplayPlaying = lambda : isFakeAvatar() or states_isBattleReplayPlaying_old()
IntUserSettings_getCache_old = IntUserSettings.getCache

def IntUserSettings_getCache(self, callback=None):
    return callback(-1, None) if isFakeAvatar() else IntUserSettings_getCache_old(self, callback)


IntUserSettings.getCache = IntUserSettings_getCache
ChatCommandsController_sendChatCommand_old = ChatCommandsController._ChatCommandsController__sendChatCommand
ChatCommandsController._ChatCommandsController__sendChatCommand = lambda self, command: isFakeAvatar() or ChatCommandsController_sendChatCommand_old(self, command)
if IS_DEV:
    BigWorld_serverTime_old = BigWorld.serverTime

    def BigWorld_serverTime():
        if isFakeAvatar():
            return BigWorld.time()
        else:
            return BigWorld_serverTime_old()


    BigWorld.serverTime = BigWorld_serverTime
game_handleKeyEvent_old = game.handleKeyEvent

def game_handleKeyEvent(event):
    global g_handleKeyEvent
    if isFakeAvatar():
        g_handleKeyEvent(event)
    return game_handleKeyEvent_old(event)


game.handleKeyEvent = game_handleKeyEvent

def getCursorWorldPos():
    x, y = GUI.mcursor().position
    dir, start = cameras.getWorldRayAndPoint(x, y)
    end = start + dir.scale(100000.0)
    return collideDynamicAndStatic(start, end, (), 0)


def create_arenaTypeID(arenaType=None, spaceName=None):
    if arenaType:
        arenaTypeID = arenaType.id
        LOG_DEBUG('arenaType present (arenaTypeID:%s)' % arenaTypeID)
    elif spaceName in ArenaType.g_geometryNamesToIDs:
        arenaTypeID = ArenaType.g_geometryNamesToIDs[spaceName]
        LOG_DEBUG('spaceName found (spaceName:%s, arenaTypeID:%s)' % (spaceName, arenaTypeID))
    else:
        arenaTypeID = ArenaType.g_geometryNamesToIDs['00_tank_tutorial']
        LOG_DEBUG('spaceName not found, use default (spaceName:00_tank_tutorial, arenaTypeID:%s)' % arenaTypeID)
    return arenaTypeID


def getFullBonusType():
    bonusType = 576460752303423487L
    guiType = max(constants.ARENA_BONUS_TYPE.RANGE) + 1
    if bonusType not in constants.ARENA_BONUS_TYPE_CAPS._typeToCaps:
        constants.ARENA_BONUS_TYPE_CAPS._typeToCaps[guiType] = bonusType
        LOG_DEBUG('Full bonus type (guiType:%s, bonusType:%s)' % (guiType, bonusType))
    return guiType


def isFakeAvatar():
    return isinstance(BigWorld.player(), FakeAvatar.FakeAvatar)


def offline_launch():
    LOG_DEBUG('offline_launch')
    BigWorld.clearEntitiesAndSpaces()
    avatar = FakeAvatar.FakeAvatar(BigWorld.createSpace())
    BigWorld.player = lambda : avatar
    avatar.vehiclesMgr.createObserver()
    avatar.onBecomePlayer()


def offline_stop():
    LOG_DEBUG('offline_stop')
    BigWorld.clearEntitiesAndSpaces()
    BigWorld.player = BigWorld_player
    g_appLoader.goToLoginByRQ()


Battle_afterCreate_old = Battle.afterCreate

def Battle_afterCreate(self):
    Battle_afterCreate_old(self)
    if isFakeAvatar():
        setattr(self.movie, '_global.wg_isReplayPlaying', True)


Battle.afterCreate = Battle_afterCreate

class FakeEvents:

    class FakeEvent:

        def __init__(self, name='FakeEvent', isMuted=False, instName='FakeEvents'):
            self.__name = name
            self.__isMuted = isMuted
            self.__instName = instName

        def __call__(self, *args, **kwargs):
            if not self.__isMuted:
                LOG_DEBUG('%s.%s ( %s, %s )' % (self.__instName,
                 self.__name,
                 args,
                 kwargs))

    def __init__(self, name='FakeEvents', isMuted=False):
        self.__isMuted = isMuted
        self.__name = name

    def __getattr__(self, name):
        return FakeEvents.FakeEvent(name=name, isMuted=self.__isMuted, instName=self.__name)


import FakeAvatar
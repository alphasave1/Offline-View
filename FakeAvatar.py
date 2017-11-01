# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: ./res_mods\0.9.12\scripts\client\gui\mods\observer_utils\FakeAvatar.py
# Compiled at: 2015-11-17 04:25:53
import BigWorld
import Math, math
import VehicleGunRotator
import Keys
import constants
import CommandMapping
import AvatarInputHandler
import AvatarPositionControl
import SoundGroups
import MusicController
import TriggersManager
import ArenaType
import game
import BattleReplay
import Event
from debug_utils import *
from functools import partial
from ClientArena import ClientArena
from helpers import DecalMap, EdgeDetectColorController, bound_effects
from account_helpers.settings_core import IntUserSettings
from PlayerEvents import g_playerEvents
from battleground import gas_attack
from gui import IngameSoundNotifications
from gui.app_loader.loader import g_appLoader
from gui.battle_control import g_sessionProvider, event_dispatcher as gui_event_dispatcher
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
from gui.battle_control.BattleSessionProvider import BattleSessionProviderStartCtx
from gui.mods.observer_utils import g_observerDP, g_handleKeyEvent
from gui.mods.observer_utils import WorldTimer, VehiclesManager, VehicleBattleSelector, FakeEvents
from gui.mods.observer_utils import LOG_DEBUG, IS_AVATAR_MODE, IS_GUN_ROTATOR, IS_PHYSICS, offline_stop, getCursorWorldPos, getFullBonusType, create_arenaTypeID

class FakeAvatar:
    getOwnVehicleSpeeds = lambda self, getInstantaneous=False: (0.0, 0.0)
    getOwnVehicleShotDispersionAngle = lambda self, turretRotationSpeed, withShot=0: 0
    enableOwnVehicleAutorotation = lambda self, enable: g_sessionProvider.invalidateVehicleState(VEHICLE_VIEW_STATE.AUTO_ROTATION, enable)
    if IS_AVATAR_MODE:
        getOwnVehiclePosition = lambda self: Math.Matrix(self.getOwnVehicleMatrix()).translation
        position = property(lambda self: self.vehicle.position)
    else:
        getOwnVehiclePosition = lambda self: Math.Matrix(BigWorld.camera().invViewMatrix).translation
        position = property(lambda self: BigWorld.camera().position)
    isForcedGuiControlMode = lambda self: self.__isForcedGuiControlMode
    getVehicleAttached = lambda self: BigWorld.entity(self.playerVehicleID)
    vehicleTypeDescriptor = property(lambda self: self.vehicle.typeDescriptor)
    vehicle = property(lambda self: self.getVehicleAttached())
    handleKey = FakeEvents.FakeEvent(name='autoAim', isMuted=True, instName='FakeAvatar')
    autoAim = FakeEvents.FakeEvent(name='autoAim', isMuted=True, instName='FakeAvatar')
    addModel = FakeEvents.FakeEvent(name='addModel', isMuted=True, instName='FakeAvatar')
    delModel = FakeEvents.FakeEvent(name='delModel', isMuted=True, instName='FakeAvatar')
    cancelWaitingForShot = FakeEvents.FakeEvent(name='cancelWaitingForShot', isMuted=True, instName='FakeAvatar')
    shoot = FakeEvents.FakeEvent(name='shoot', isMuted=True, instName='FakeAvatar')
    handleVehicleCollidedVehicle = FakeEvents.FakeEvent(name='handleVehicleCollidedVehicle', isMuted=True, instName='FakeAvatar')
    targetBlur = FakeEvents.FakeEvent(name='targetBlur', isMuted=True, instName='FakeAvatar')
    cell = FakeEvents(name='FakeAvatar.cell', isMuted=True)
    base = FakeEvents(name='FakeAvatar.base', isMuted=False)

    def __init__(self, spaceID):
        LOG_DEBUG('FakeAvatar.__init__(%s)' % spaceID)
        self.spaceID = spaceID
        self.onVehicleLeaveWorld = Event.Event()
        self.onVehicleEnterWorld = Event.Event()
        self.onGunShotChanged = Event.Event()
        self.positionControl = AvatarPositionControl.AvatarPositionControl(self)
        self.spaceName = g_observerDP.arenaData[0]
        self.arenaTypeID = create_arenaTypeID(g_observerDP.arenaData[1], self.spaceName)
        self.arenaGuiType = constants.ARENA_GUI_TYPE.RANDOM
        self.arenaVisibilityMask = ArenaType.getVisibilityMask(self.arenaTypeID >> 16)
        self.arena = ClientArena(self.spaceID, self.arenaTypeID, getFullBonusType(), self.arenaGuiType, {}, None)
        self.team = 1
        self.name = 'offline'
        self.isOnArena = self.isVehicleAlive = True
        self.hitTesters = set()
        self.playerVehicleID = 0
        self.isWaitingForShot = False
        self.terrainEffects = bound_effects.StaticSceneBoundEffects()
        self.spaceInitiaized = False
        self.filter = BigWorld.AvatarFilter()
        self.autoAimVehicle = None
        self.intUserSettings = IntUserSettings.IntUserSettings()
        self.matrix = Math.Matrix()
        self.target = None
        self.consistentMatrices = AvatarPositionControl.ConsistentMatrices()
        self.soundNotifications = IngameSoundNotifications.IngameSoundNotifications()
        self.complexSoundNotifications = IngameSoundNotifications.ComplexSoundNotifications(self.soundNotifications)
        self.__isForcedGuiControlMode = False
        self.__isGuiVisible = True
        self.__isModMenuVisible = False
        self.__isSpaceLoaded = False
        self.vehiclesMgr = VehiclesManager.VehiclesManager(self)
        self.worldTime = WorldTimer.WorldTimer(self)
        self.__aimingInfo = [0.0,
         0.0,
         1.0,
         0.0,
         0.0,
         0.0,
         1.0]
        self.isGunLocked = False
        self.__ownVehicleMProv = Math.WGAdaptiveMatrixProvider()
        self.deviceStates = {}
        self.physics = None
        return

    def onBecomePlayer(self):
        global g_handleKeyEvent
        g_handleKeyEvent += self.handleKeyEvent
        MusicController.g_musicController.stopAmbient()
        gas_attack.initAttackManager(self.arena)
        g_sessionProvider.start(BattleSessionProviderStartCtx(avatar=self, arena=self.arena, replayCtrl=BattleReplay.g_replayCtrl, gasAttackMgr=gas_attack.gasAttackManager()))
        g_playerEvents.onAvatarBecomePlayer()

    def leaveArena(self):
        global g_handleKeyEvent
        g_handleKeyEvent -= self.handleKeyEvent
        BigWorld.worldDrawEnabled(False)
        MusicController.g_musicController.onLeaveArena()
        self.inputHandler.destroy()
        self.gunRotator.destroy()
        self.arena.destroy()
        self.positionControl.destroy()
        BigWorld.wg_clearDecals()
        offline_stop()

    def getOwnVehicleMatrix(self):
        vehicle = self.vehicle
        if vehicle is not None:
            m = Math.Matrix()
            m.setRotateYPR((vehicle.roll, vehicle.pitch, vehicle.yaw))
            m.translation = vehicle.position
            self.__ownVehicleMProv.setStaticTransform(m)
        return self.__ownVehicleMProv

    def handleKeyEvent(self, event):
        try:
            isDown, key, mods, isRepeat = game.convertKeyEvent(event)
            cmdMap = CommandMapping.g_instance
            cursorWorldPos = getCursorWorldPos()
            if isDown or isRepeat:
                if cmdMap.isFiredList((CommandMapping.CMD_MINIMAP_SIZE_DOWN, CommandMapping.CMD_MINIMAP_SIZE_UP, CommandMapping.CMD_MINIMAP_VISIBLE), key):
                    gui_event_dispatcher.setMinimapCmd(key)
                if not self.__isForcedGuiControlMode and cmdMap.isFired(CommandMapping.CMD_TOGGLE_GUI, key):
                    self.__setVisibleGUI(not self.__isGuiVisible)
                if key == Keys.KEY_U:
                    self.vehiclesMgr.updateVehicleState(VehiclesManager.STATE_EFFECTS.DESTORY, None if mods == 2 else self.vehiclesMgr.curVehicle)
                if key == Keys.KEY_NUMPADSTAR:
                    self.vehiclesMgr.deleteVehicle(None if mods == 2 else self.vehiclesMgr.curVehicleID)
                shot_key = Keys.KEY_LEFTMOUSE if IS_AVATAR_MODE else Keys.KEY_RIGHTMOUSE
                if key == shot_key:
                    self.vehiclesMgr.showShooting(None if mods == 2 and not IS_AVATAR_MODE else self.vehiclesMgr.curVehicle)
                teleport_key = Keys.KEY_RIGHTMOUSE if IS_AVATAR_MODE else Keys.KEY_LEFTMOUSE
                if key == teleport_key:
                    if not self.vehiclesMgr.pickVehicleFromCursor():
                        if cursorWorldPos is not None:
                            self.vehiclesMgr.teleport(cursorWorldPos[0], angles=(BigWorld.camera().direction.yaw, 0, 0))
                if key == Keys.KEY_NUMPAD1:
                    self.vehiclesMgr.resetFilter(None if mods == 2 else self.vehiclesMgr.curVehicle)
                if key == Keys.KEY_Z and cursorWorldPos is not None:
                    self.vehiclesMgr.createVehicle(cursorWorldPos[0], (0, 0, BigWorld.camera().direction.yaw))
                if not IS_AVATAR_MODE and key == Keys.KEY_N and mods == 2:
                    self.resetCamera()
                if key == Keys.KEY_NUMPADMINUS:
                    self.worldTime.decrement()
                if key == Keys.KEY_ADD:
                    self.worldTime.increment()
                if key == Keys.KEY_NUMPADENTER:
                    self.worldTime.reset()
                if key == Keys.KEY_G:
                    self.__isModMenuVisible = not self.__isModMenuVisible
                    VehicleBattleSelector.g_instance.setVisible(self.__isModMenuVisible)
                if IS_PHYSICS and cmdMap.isFired(CommandMapping.CMD_STOP_UNTIL_FIRE, key) and isDown:
                    self.physics.onVehicleStop()
        except:
            LOG_CURRENT_EXCEPTION()

        return

    def __setVisibleGUI(self, bool):
        self.__isGuiVisible = bool
        gui_event_dispatcher.setGUIVisibility(bool)
        BigWorld.wg_enableTreeTransparency(bool)
        if self.vehiclesMgr.curVehicleID > 0:
            if bool:
                VehiclesManager.VehiclesManager.addVehicleEdge(self.vehiclesMgr.curVehicleID)
            else:
                VehiclesManager.VehiclesManager.removeVehicleEdge(self.vehiclesMgr.curVehicleID)
        self.inputHandler.setGUIVisible(bool)

    def setForcedGuiControlMode(self, value, stopVehicle=True, enableAiming=True):
        if self.inputHandler is not None:
            if self.__isForcedGuiControlMode ^ value:
                self.inputHandler.detachCursor(value, enableAiming)
            self.__isForcedGuiControlMode = value
        return

    def initSpace(self):
        LOG_DEBUG('FakeAvatar.initSpace()')
        if not self.spaceInitiaized:
            BigWorld.enableLoadingTimer(True)
            BigWorld.worldDrawEnabled(False)
            BigWorld.addSpaceGeometryMapping(self.spaceID, None, 'spaces/%s' % self.spaceName)
            BigWorld.cameraSpaceID(self.spaceID)
            BigWorld.wg_setSpaceItemsVisibilityMask(self.spaceID, self.arenaVisibilityMask)
            self.inputHandler = AvatarInputHandler.AvatarInputHandler()
            self.gunRotator = VehicleGunRotator.VehicleGunRotator(self)
            self.spaceInitiaized = True
        return

    def vehicle_onLeaveWorld(self, vehicle):
        LOG_DEBUG('FakeAvatar.vehicle_onLeaveWorld(%s)' % vehicle.id)
        if vehicle.isStarted:
            self.onVehicleLeaveWorld(vehicle)
            vehicle.stopVisual()
            model = vehicle.model
            vehicle.model = None
        return

    def vehicle_onEnterWorld(self, vehicle):
        LOG_DEBUG('FakeAvatar.vehicle_onEnterWorld(%s)' % vehicle.id)
        vehicle.isPlayer = True
        if not isinstance(vehicle.filter, BigWorld.WGVehicleFilter):
            vehicle.filter = BigWorld.WGVehicleFilter()
        if self.playerVehicleID == vehicle.id:
            g_sessionProvider.setPlayerVehicle(vehicle.id, vehicle.typeDescriptor)
            g_appLoader.startBattle()
        if IS_AVATAR_MODE or self.playerVehicleID != vehicle.id:
            self.vehiclesMgr.vehicles.append(vehicle.id)
            if self.__isSpaceLoaded:
                vehicle.startVisual()
                self.vehiclesMgr.selectVehicle()
        if self.__isSpaceLoaded:
            self.onVehicleEnterWorld(vehicle)

    def onSpaceLoaded(self):
        LOG_DEBUG('FakeAvatar.onSpaceLoaded()')
        EdgeDetectColorController.g_instance.updateColors()
        DecalMap.g_instance.initGroups(1.0)
        SoundGroups.g_instance.enableArenaSounds(True)
        SoundGroups.g_instance.applyPreferences()
        MusicController.g_musicController.onEnterArena()
        TriggersManager.g_manager.enable(True)
        BigWorld.wg_setUmbraEnabled(self.arena.arenaType.umbraEnabled)
        BigWorld.wg_enableTreeHiding(False)
        BigWorld.worldDrawEnabled(True)
        BigWorld.wg_setAmbientReverb(self.arena.arenaType.defaultReverbPreset)
        BigWorld.wg_setWaterTexScale(self.arena.arenaType.waterTexScale)
        BigWorld.wg_setWaterFreqX(self.arena.arenaType.waterFreqX)
        BigWorld.wg_setWaterFreqZ(self.arena.arenaType.waterFreqZ)
        BigWorld.enableLoadingTimer(False)
        BigWorld.callback(10.0, partial(BigWorld.pauseDRRAutoscaling, False))
        self.inputHandler.start()
        self.inputHandler.setReloading(-1)
        self.arena.onPeriodChange(constants.ARENA_PERIOD.BATTLE, 0, 0)
        self.worldTime.reset()
        self.resetCamera()
        g_appLoader.showBattle()
        self.__isSpaceLoaded = True
        for vehicleID in self.vehiclesMgr.vehicles:
            vehicle = BigWorld.entity(vehicleID)
            if vehicle and not self.vehicle.isStarted:
                vehicle.startVisual()
                self.vehiclesMgr.vehicles.append(vehicle.id)
                self.vehiclesMgr.selectVehicle()
                self.onVehicleEnterWorld(vehicle)

        if IS_PHYSICS:
            import VehiclePhysics
            self.physics = VehiclePhysics.VehiclePhysics(self.vehicle, self.vehicle.vPhysics)
            self.physics.start()

    def resetCamera(self):
        LOG_DEBUG('FakeAvatar.resetCamera()')
        if IS_AVATAR_MODE:
            self.inputHandler.onControlModeChanged('arcade')
            if IS_GUN_ROTATOR:
                self.gunRotator.update(0, 0, self.vehicleTypeDescriptor.turret['rotationSpeed'], self.vehicleTypeDescriptor.gun['rotationSpeed'])
        else:
            self.gunRotator.stop()
            self.inputHandler.onControlModeChanged('video')
            self.alignToLand()

    def alignToLand(self):
        cam = self.inputHandler.ctrl._cam
        cam._VideoCamera__alignerToLand.enable(self.position, False)
        cam._VideoCamera__update()
        cam._VideoCamera__alignerToLand.disable()
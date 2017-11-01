# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: ./res_mods\0.9.12\scripts\client\gui\mods\observer_utils\ObserverWindow.py
# Compiled at: 2015-11-17 04:26:12
import BigWorld, ResMgr
import ArenaType, constants
from helpers import i18n
from debug_utils import LOG_ERROR, LOG_CURRENT_EXCEPTION
from items.vehicles import g_list, VehicleDescr, getVehicleTypeCompactDescr
from gui.shared import events, EVENT_BUS_SCOPE
from gui.shared.gui_items import ItemsCollection, Vehicle
from gui.shared.gui_items.Vehicle import Vehicle as VehicleItem
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.Scaleform.daapi.view.lobby.trainings import formatters
from gui.Scaleform.daapi.view.lobby.MinimapLobby import MinimapLobby
from gui.Scaleform.daapi.view.lobby.cyberSport.VehicleSelectorPopup import VehicleSelectorPopup
from gui.Scaleform.daapi.view.lobby.trainings.TrainingSettingsWindow import TrainingSettingsWindow
from gui.Scaleform.genConsts.CYBER_SPORT_ALIASES import CYBER_SPORT_ALIASES
from gui.Scaleform.genConsts.PREBATTLE_ALIASES import PREBATTLE_ALIASES
from gui.app_loader.loader import g_appLoader
from gui.mods import observer_utils
from gui.mods.modsListAPI import g_modsListApi
from gui.LobbyContext import g_lobbyContext
g_lobbyContext.setServerSettings({'roamingSettings': [0,
                     0,
                     [],
                     []]})

def getVehicles():
    res = ItemsCollection()
    ids = g_list._VehicleList__ids
    for value in ids.values():
        vID = getVehicleTypeCompactDescr(VehicleDescr(typeID=value).makeCompactDescr())
        item = VehicleItem(typeCompDescr=vID)
        item.isObserverMod = True
        res[vID] = item

    return res


_VEHICLES = getVehicles()

def isObserverMod(object):
    return getattr(object, 'isObserverMod', False)


def init():
    OBSERVER_ALIAS = 'ObserverWindow'
    settings = ViewSettings(OBSERVER_ALIAS, ObserverWindow, '../../scripts/client/gui/mods/observer_utils/flash/ObserverWindow.swf', ViewTypes.WINDOW, None, ScopeTemplates.DEFAULT_SCOPE)
    g_entitiesFactories.addSettings(settings)
    VehicleItem_isReadyToFight = VehicleItem.isReadyToFight.fget
    VehicleItem.isReadyToFight = property(lambda self: isObserverMod(self) or VehicleItem_isReadyToFight(self))
    mod_name = '\xce\xf4\xf4\xeb\xe0\xe9\xed \xef\xf0\xee\xf1\xec\xee\xf2\xf0 \xea\xe0\xf0\xf2' if constants.DEFAULT_LANGUAGE == 'ru' else 'Offline map viewer'
    g_modsListApi.addMod(id='mod_observer', name=mod_name, description=mod_name, icon='', enabled=True, login=True, lobby=False, callback=lambda : g_appLoader.getApp().loadView(OBSERVER_ALIAS, OBSERVER_ALIAS))
    return


class ObserverWindow(AbstractWindowView):

    def showSelectMap(self):
        g_appLoader.getApp().fireEvent(events.LoadViewEvent(PREBATTLE_ALIASES.TRAINING_SETTINGS_WINDOW_PY, ctx={'isCreateRequest': True,
         'isObserverMod': True}), scope=EVENT_BUS_SCOPE.LOBBY)

    def showSelectVehicles(self):
        g_appLoader.getApp().fireEvent(events.LoadViewEvent(CYBER_SPORT_ALIASES.VEHICLE_SELECTOR_POPUP_PY, ctx={'isMultiSelect': True,
         'infoText': None,
         'componentsOffset': 0,
         'selectedVehicles': None,
         'section': 'cs_intro_view_vehicle',
         'levelsRange': range(1, 11),
         'vehicleTypes': Vehicle.VEHICLE_CLASS_NAME.ALL(),
         'isObserverMod': True}), scope=EVENT_BUS_SCOPE.LOBBY)
        return

    def startLoading(self):
        observer_utils.offline_launch()

    def __update(self, name, value):
        if name == 'arenaData':
            self.as_setLoadingEnabledS(value is not None)
            arenaName = 'Unselected'
            spaceName = '00_tank_tutorial'
            if value is not None:
                arenas = ArenasCache()
                arenaTypeID = value[2]
                spaceName = value[0]
                if arenaTypeID in arenas.hangarsData.keys():
                    arenaName = arenas.hangarsData[arenaTypeID]['label']
                else:
                    arenaName = ArenaType.g_cache[arenaTypeID].name
            self.as_setArenaS(arenaName, spaceName)
        return

    def as_setArenaS(self, arenaName, spaceName):
        return self.flashObject.as_setArena(arenaName, '../maps/icons/map/stats/%s.png' % spaceName) if self._isDAAPIInited() else None

    def as_setLoadingEnabledS(self, isEnabled):
        return self.flashObject.as_setLoadingEnabled(isEnabled) if self._isDAAPIInited() else None

    def _populate(self):
        super(AbstractWindowView, self)._populate()
        observer_utils.g_observerDP.onUpdateValue += self.__update

    def onWindowClose(self):
        observer_utils.g_observerDP.onUpdateValue -= self.__update
        self.destroy()

    def onTryClosing(self):
        return True


class ArenasCache:

    def __init__(self):
        self.__cache = []
        self.__hangarsData = {}
        maps = []
        for arenaTypeID, arenaType in ArenaType.g_cache.iteritems():
            try:
                nameSuffix = '' if arenaType.gameplayName == 'ctf' else i18n.makeString('#arenas:type/%s/name' % arenaType.gameplayName)
                self.__cache.append({'label': '%s - %s' % (arenaType.name, nameSuffix) if len(nameSuffix) else arenaType.name,
                 'name': arenaType.name,
                 'arenaType': nameSuffix,
                 'key': arenaTypeID,
                 'size': arenaType.maxPlayersInTeam,
                 'time': arenaType.roundLength / 60,
                 'description': '',
                 'icon': formatters.getMapIconPath(arenaType)})
                if arenaType.geometryName not in maps:
                    maps.append(arenaType.geometryName)
            except Exception:
                LOG_ERROR('There is error while reading arenas cache', arenaTypeID, arenaType)
                LOG_CURRENT_EXCEPTION()
                continue

        id = -1
        for folderName, _ in ResMgr.openSection('spaces').items():
            if folderName not in maps:
                map_data = {'label': '[?] %s' % folderName,
                 'name': folderName,
                 'arenaType': '?',
                 'key': id,
                 'size': 0,
                 'time': 0,
                 'description': '',
                 'icon': None}
                settingsXml = ResMgr.openSection('spaces/' + folderName + '/space.settings/hangarSettings')
                if settingsXml is not None:
                    map_data['arenaType'] = 'HANGAR'
                    map_data['label'] = '[HANGAR] %s' % folderName
                self.__cache.append(map_data)
                self.__hangarsData[id] = map_data
                id = id - 1

        self.__cache = sorted(self.__cache, key=lambda x: (x['label'].lower(), x['name'].lower()))
        return

    @property
    def hangarsData(self):
        return self.__hangarsData

    @property
    def cache(self):
        return self.__cache


MinimapLobby_setArena_old = MinimapLobby.setArena

def MinimapLobby_setArena(self, arenaTypeID):
    if arenaTypeID < 0:
        arenaTypeID = ArenaType.g_geometryNamesToIDs['00_tank_tutorial']
    return MinimapLobby_setArena_old(self, arenaTypeID)


MinimapLobby.setArena = MinimapLobby_setArena
TrainingSettingsWindow_init_old = TrainingSettingsWindow.__init__

def TrainingSettingsWindow_init(self, ctx=None):
    TrainingSettingsWindow_init_old(self, ctx)
    self.isObserverMod = ctx.get('isObserverMod', False)
    if isObserverMod(self):
        self._TrainingSettingsWindow__arenasCache = ArenasCache()


TrainingSettingsWindow.__init__ = TrainingSettingsWindow_init
TrainingSettingsWindow_updateTrainingRoom_old = TrainingSettingsWindow.updateTrainingRoom

def TrainingSettingsWindow_updateTrainingRoom(self, arenaTypeID, roundLength, isPrivate, comment):
    if isObserverMod(self):
        arena = None
        spaceName = None
        cache = self._TrainingSettingsWindow__arenasCache
        arenaTypeID = int(arenaTypeID)
        if arenaTypeID in cache.hangarsData.keys():
            spaceName = cache.hangarsData[arenaTypeID]['name']
        else:
            arena = ArenaType.g_cache[arenaTypeID]
            spaceName = arena.geometryName
        observer_utils.g_observerDP.arenaData = (spaceName, arena, arenaTypeID)
        self.onWindowClose()
    else:
        TrainingSettingsWindow_updateTrainingRoom_old(self, arenaTypeID, roundLength, isPrivate, comment)
    return


TrainingSettingsWindow.updateTrainingRoom = TrainingSettingsWindow_updateTrainingRoom
VehicleSelectorPopup_init_old = VehicleSelectorPopup.__init__

def VehicleSelectorPopup_init(self, ctx=None):
    VehicleSelectorPopup_init_old(self, ctx)
    self.isObserverMod = ctx.get('isObserverMod', False)


VehicleSelectorPopup.__init__ = VehicleSelectorPopup_init
VehicleSelectorPopup_updateData_old = VehicleSelectorPopup.updateData

def VehicleSelectorPopup_updateData(self):
    if isObserverMod(self):
        vehicleVOs = self._updateData(_VEHICLES, self._VehicleSelectorPopup__levelsRange, self._VehicleSelectorPopup__vehicleTypes)
        self.as_setListDataS(vehicleVOs, None)
    else:
        return VehicleSelectorPopup_updateData_old(self)
    return


VehicleSelectorPopup.updateData = VehicleSelectorPopup_updateData
VehicleSelectorPopup_onSelectVehicles_old = VehicleSelectorPopup.onSelectVehicles

def VehicleSelectorPopup_onSelectVehicles(self, items):
    if isObserverMod(self):
        self.fireEvent(events.CSVehicleSelectEvent(events.CSVehicleSelectEvent.VEHICLE_SELECTED, items))
        selectedVehicles = {}
        for vID in items:
            veh = VehicleItem(typeCompDescr=int(vID))
            selectedVehicles[veh.name] = veh.shortUserName

        observer_utils.g_observerDP.vehicles = selectedVehicles
        observer_utils.g_observerDP.vehicle = selectedVehicles.keys()[-1]
        self.onWindowClose()
    else:
        return VehicleSelectorPopup_onSelectVehicles_old(self, items)


VehicleSelectorPopup.onSelectVehicles = VehicleSelectorPopup_onSelectVehicles
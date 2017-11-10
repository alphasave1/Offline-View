from debug_utils import LOG_CURRENT_EXCEPTION
import game
import Keys
import BigWorld
from helpers import dependency
from gui.shared import personality as gui_personality
from skeletons.connection_mgr import IConnectionManager
from helpers import OfflineMode
from gui.Scaleform.framework import g_entitiesFactories, ViewSettings
from gui.Scaleform.framework import ViewTypes, ScopeTemplates
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.app_loader import g_appLoader
from gui.Scaleform.framework.managers.loaders import ViewLoadParams
from gui.modsListApi import g_modsListApi

spaceName=''

def init():
    manager = dependency.instance(IConnectionManager)
    manager.onConnected+=onConnected
    manager.onDisconnected+=onDisconnected
    global enableHandleKeyEvent
    enableHandleKeyEvent=True
    g_modsListApi.addModification(id='DropDown',name='DropDown',description='DropDownMenu Test Program.',enabled=True,callback=lambda: g_appLoader.getDefLobbyApp().loadView(ViewLoadParams(_alias, None)),login=True,lobby=False,icon='')


class TestWindow(AbstractWindowView):

    def __init__(self):
        super(TestWindow, self).__init__()

    def py_log(self,mapName):
        print mapName

    def _populate(self):
        super(TestWindow, self)._populate()

    def onWindowClose(self):
               mapName=self.flashObject.as_getMapName()
        print mapName
        self.destroy()
        start(mapName)

_alias = 'Main'
_url = 'DropDown2.swf'
_type = ViewTypes.WINDOW
_event = None
_scope = ScopeTemplates.VIEW_SCOPE

_settings = ViewSettings(_alias, TestWindow, _url, _type, _event, _scope)
g_entitiesFactories.addSettings(_settings)

class MOD:
    AUTHOR = 'Chirimen , alphasave1'
    NAME = 'OfflineMode'
    VERSION = '1.0'
    DESCRIPTION = 'Load Mod From ModsListApi ,OfflineMode will Start.\n Elif You Push END Key,OfflineMode will End.'
    SUPPORT_URL = 'http://twitter.com/chirimenspiral , http://www.twitter.com/alphasave1'

def start(mapName):
    print 'mod_OfflineMode: start'
    if not OfflineMode.enabled():
        gui_personality.fini()
    OfflineMode.launch(mapName)

def shutdown():
    print 'mod_OfflineMode: shutdown'
    if OfflineMode.enabled():
        OfflineMode.onShutdown()
        BigWorld.quit()

def onConnected():
    global enableHandleKeyEvent
    enableHandleKeyEvent=False

def onDisconnected():
    global enableHandleKeyEvent
    enableHandleKeyEvent=True

def handleKeyEvent(event):
    ret = wg_handleKeyEvent(event)
    try:
        if enableHandleKeyEvent and event.isKeyDown() and not event.isRepeatedEvent():
            if event.key==Keys.KEY_END:
                shutdown()
    except:
        LOG_CURRENT_EXCEPTION()
    return ret

wg_handleKeyEvent = game.handleKeyEvent
game.handleKeyEvent = handleKeyEvent
enableHandleKeyEvent=False

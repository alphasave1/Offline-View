from gui.Scaleform.framework import g_entitiesFactories, ViewSettings
from gui.Scaleform.framework import ViewTypes, ScopeTemplates
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView
from gui.app_loader import g_appLoader
from gui.Scaleform.framework.managers.loaders import ViewLoadParams
from gui.shared.utils.key_mapping import getBigworldNameFromKey

class TestWindow(AbstractWindowView):

    def __init__(self):
        super(TestWindow, self).__init__()

    def py_log(self,mapName):
        print mapName

    def _populate(self):
        super(TestWindow, self)._populate()

    def onWindowClose(self):
        self.flashObject.as_setText()
        self.destroy()


_alias = 'Main'
_url = 'DropDown2.swf'
_type = ViewTypes.WINDOW
_event = None
_scope = ScopeTemplates.VIEW_SCOPE


_settings = ViewSettings(_alias, TestWindow, _url, _type, _event, _scope)
g_entitiesFactories.addSettings(_settings)

def onhandleKeyEvent(event):
    key = getBigworldNameFromKey(event.key)
    if key == 'KEY_F12':
        g_appLoader.getDefLobbyApp().loadView(ViewLoadParams(_alias, None))
    return None

from gui import InputHandler
InputHandler.g_instance.onKeyDown += onhandleKeyEvent

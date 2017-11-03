# mod_OfflineMode.py

from debug_utils import LOG_CURRENT_EXCEPTION
import game
import Keys
import BigWorld
from helpers import dependency
from gui.shared import personality as gui_personality
from skeletons.connection_mgr import IConnectionManager
from helpers import OfflineMode

space_list=['spaces/84_winter','spaces/120_kharkiv_halloween','spaces/h03_shopfest_2015','spaces/hangar_premium_v2']
space_idx=0

class MOD:
    AUTHOR = 'Chirimen , alphasave1'
    NAME = 'OfflineMode'
    VERSION = '1.0'
    DESCRIPTION = 'If You Push HOME Key,OfflineMode will Start.\n Elif You Push END Key,OfflineMode will End.'
    SUPPORT_URL = 'http://www.twitter.com/alphasave1'

def init():
    manager=dependency.instance(IConnectionManager)
    manager.onConnected+=onConnected
    manager.onDisconnected+=onDisconnected
    global enableHandleKeyEvent
    enableHandleKeyEvent=True

def start():
    print 'mod_OfflineMode: start'
    if not OfflineMode.enabled():
        gui_personality.fini()
    global space_idx
    OfflineMode.launch(space_list[space_idx])
    space_idx=(space_idx+1) % len(space_list)
    
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
            if event.key == Keys.KEY_HOME:
                start()
            elif event.key==Keys.KEY_END:
                shutdown()
    except:
        LOG_CURRENT_EXCEPTION()
    return ret

wg_handleKeyEvent = game.handleKeyEvent
game.handleKeyEvent = handleKeyEvent
enableHandleKeyEvent=False

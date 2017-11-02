# mod_OfflineMode.py
import game
import Keys
import BigWorld
from helpers import OfflineMode
spaceName='spaces/h03_shopfest_2015'

class MOD:
    AUTHOR = 'Chirimen , alphasave1'
    NAME = 'OfflineMode'
    VERSION = '1.0'
    DESCRIPTION = 'If You Push HOME Key,OfflineMode will Start.'
    SUPPORT_URL = 'http://www.twitter.com/alphasave1'


def START():
    print 'mod_OfflineMode: onStartup'
    game.fini()
    OfflineMode.launch(spaceName)
    return True

def handleKeyEvent(event):
    ret = wg_handleKeyEvent(event)
    try:
        if event.isKeyDown() and not event.isRepeatedEvent():
            if event.key == Keys.KEY_HOME:
                START()
    except:
        LOG_CURRENT_EXCEPTION()

    return ret


wg_handleKeyEvent = game.handleKeyEvent
game.handleKeyEvent = handleKeyEvent

import game
from helpers import OfflineMode

spaceName='hangar_premium_v2'
game.fini()
OfflineMode.launch(spaceName)
 
OfflineMode.onShutdown()

game.start()

spaceName='hangar_v2'
game.fini()
OfflineMode.launch(spaceName)

OfflineMode.onShutdown()

game.start()

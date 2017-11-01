from gui.app_loader.loader import g_appLoader
from gui.mods.modsListApi import g_modsListApi
def init():
mod_name='mod_OfflineTest'
g_modsListApi.addMod(id='mod_offline',name=mod_name,description=mod_name,icon='',enabled=True,login=True,lobby=False,callback=lambda:g_appLoader.getApp().loadView(OBSERVER_ALIAS,OBSERVER_ALIAS))
)

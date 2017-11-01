from gui.app_loader.loader import g_appLoader
from gui.modsListApi import g_modsListApi
mod_name='mod_OfflineTest'
def init():
  g_modsListApi.addModification(id='mod_offline',name=mod_name,description=mod_name,enabled=True,callback=''login=True,lobby=False,icon='')

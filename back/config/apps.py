import os

from django.apps import AppConfig

def init():
    print("""
     ____    __ __    _ ____   _  _____  _____  ______  __   _  ____    
    |    \  /  |\ \  //|    \ | |/     \/     \|   ___||  |_| ||    \   
    |     \/   | \ \// |     \| ||     ||     | `-.`-. |   _  ||     \  
    |__/\__/|__| /__/  |__/\____|\_____/\_____/|______||__| |_||__|\__\ 
    """)

class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'


    def ready(self):
        if os.environ.get('RUN_MAIN'):
            init()

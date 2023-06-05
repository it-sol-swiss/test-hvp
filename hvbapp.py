# hvbapp.py

import os
from kivy.app import App
from kivy.lang import Builder

from app.controllers.home_screen import HomeScreen
from app.controllers.connection import Connection
from app.controllers.screen_two import ScreenTwo
from app.controllers.screen_three import ScreenThree


class HvBApp(App):
    def build(self):
        # Determine the path to the kv file
        kv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hvb.kv')
        return Builder.load_file(kv_path)

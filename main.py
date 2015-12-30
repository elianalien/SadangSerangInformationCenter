__author__ = 'Chairun R Siregar'

from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix

import logger
import gv

from menu_utama import menu_utama
from info_bdg import info_bdg
from peta import peta
from data import data
from rumah_kita import info_perkembangan_rumah
from rumah_kita import info_tematik

Window.clearcolor = (1, 1, 1, 1)
finalSize = (1920, 1080)

class SmartCityApp(App):
    def build(self):
        # Window.size = (finalSize[0] / 2, finalSize[1] / 2)
        # Window.fullscreen = 'fake'
        Window.size = (finalSize[0], finalSize[1])
        Window.fullscreen = True

        Builder.load_file('app.kv')
        Builder.load_file('menu_utama/style.kv')
        Builder.load_file('info_bdg/style.kv')
        Builder.load_file('peta/style.kv')
        Builder.load_file('data/style.kv')
        Builder.load_file('rumah_kita/style.kv')

        gv.app = MainContainer()
        gv.app.start()

        return gv.app

class MainContainer(FloatLayout):
# class MainContainer(ScatterLayout):
    def __init__(self, **kwargs):
        super(MainContainer, self).__init__(**kwargs)

    def start(self):
        # setup logger
        gv.logger = logger.Logger()
        
        gv.sm = self.ids['screen_manager']

        self.menu_utama = self.add_screen(menu_utama.MenuUtama(), False)

        self.info_ngabandungan = self.add_screen(info_bdg.InfoNgabandungan())
        self.peta = self.add_screen(peta.Peta())
        self.data = self.add_screen(data.Data())
        self.info_perkembangan_rumah = self.add_screen(info_perkembangan_rumah.InfoPerkembanganRumah())
        self.info_tematik = self.add_screen(info_tematik.InfoTematik())

        gv.sm.current = "Menu Utama"
        # gv.sm.current = "Info Tematik"

        # auto standby
        #   return to main menu after a period of inactivity
        Clock.schedule_interval(self.standby_count_down, 10)
        self.bind(on_touch_down = self.reset_standby)
        self.bind(on_touch_up = self.log_touch_up)

        # nanti scaling dimatiin dan scatternya diganti FlowLayout
        # mat = Matrix().scale(0.5, 0.5, 1)
        # self.apply_transform(mat)
        #---------------------------------------------------

    # add new screen and configure it
    def add_screen(self, new_screen, top_bar = True):
        if top_bar:
            new_screen.add_widget(TopBar())
            new_screen.size = finalSize

        gv.sm.add_widget(new_screen)

        return  new_screen

    def log_screen_change(self):
        gv.logger.log_screen_change(gv.sm.current)

    standby_timer = 0

    # reset standby timer
    def reset_standby(self, o, e):
        self.standby_timer = 6
        gv.logger.log_touch(e.pos)

    def log_touch_up(self, o, e):
        gv.logger.log_touch_up(e.pos)

    # count down timer to standby
    def standby_count_down(self, t):
        gv.logger.log_check()

        if self.standby_timer >= 0:
            self.standby_timer -= 1

        if self.standby_timer == 0:
            #globals.logger.log_standby()

            #if in Menu Utama -> reset Menu Utama
            if gv.sm.current == 'Menu Utama':
                gv.sm.current_screen.hide_submenu()

            #else -> go back to Menu Utama
            else:
                gv.sm.transition.direction = 'up'
                gv.sm.current = 'Menu Utama'


class TopBar(BoxLayout):
    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.page_title = self.ids['page_title']

        self.btn_back = self.ids['btn_back']
        self.btn_back.bind(on_release = self.log_back)

    def on_parent(self, a, b):
        if self.parent:
            self.page_title.text = self.parent.name.upper()

    def log_back(self, b):
        gv.logger.log_button('Menu Utama')
        gv.sm.transition.direction = 'up'
        gv.sm.current = 'Menu Utama'

if __name__ == '__main__':
    SmartCityApp().run()

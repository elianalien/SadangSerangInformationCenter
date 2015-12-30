__author__ = 'Elian Si Ganteng'

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.animation import Animation

import gv
#buat akses var global:
#   app = gv.app
#   class Data = gv.app.data
#   screen manager = gv.sm
#   logger = gv.logger
#       panggil gv.logger.log_button(*nama button*) buat masukin kegiatan ke log

class Data(Screen):
    def __init__(self, **kwargs):
        super(Data, self).__init__(**kwargs)

        ## TOGGLE BUTTON FUNCTION ##
        self.mataPencarianButton        = Button(background_normal = 'data/lib/data-mata-pencaharian.png',
                                                background_down = 'data/lib/data-mata-pencaharian-hit.png',
                                                state='normal',
                                                size_hint=(None,None),
                                                size = (159, 165))
        self.pemelukAgamaButton		    = Button(background_normal = 'data/lib/data-pemeluk-agama.png',
                                                background_down = 'data/lib/data-pemeluk-agama-hit.png',
                                                state='normal',
                                                size_hint=(None,None),
                                                size = (159, 165))
        self.dataPendidikanButton		= Button(background_normal = 'data/lib/data-pendidikan.png',
                                                background_down = 'data/lib/data-pendidikan-hit.png',
                                                state='normal',
                                                size_hint=(None,None),
                                                size = (159, 165))
        self.dataUmurButton				= Button(background_normal = 'data/lib/data-struktur-umur.png',
                                                background_down = 'data/lib/data-struktur-umur-hit.png',
                                                state='normal',
                                                size_hint=(None,None),
                                                size = (159, 165))

        self.infografik = []
        self.infografik.append(Image(source='data/content/data-mata-pencaharian-info.png',allow_stretch=True, size_hint=(.9,.9), pos_hint={'x': 0, 'y':0})) 	#0
        self.infografik.append(Image(source='data/content/data-pemeluk-agama-info.png',allow_stretch=True, size_hint=(.9,.9), pos_hint={'x': 0, 'y':0}))		#1
        self.infografik.append(Image(source='data/content/data-tingkat-pendidikan-info.png',allow_stretch=True, size_hint=(.9,.9), pos_hint={'x': 0, 'y':0}))	#2
        self.infografik.append(Image(source='data/content/data-struktur-umur-info.png',allow_stretch=True, size_hint=(.9,.9), pos_hint={'x': 0, 'y':0}))		#3
        self.infografik.append(Image(source='data/content/BG01c.png',allow_stretch=True)) 						                                                #4

        self.mataPencarianButton.bind(on_release=self.mataPencarian)
        self.pemelukAgamaButton.bind(on_release=self.pemelukAgama)
        self.dataPendidikanButton.bind(on_release=self.dataPendidikan)        
        self.dataUmurButton.bind(on_release=self.dataStrukturUmur)

        ## Button Container ##
        self.bLayout = BoxLayout(size_hint=(None,None),
                                    orientation='horizontal', 
                                    width = 720,
                                    height= 650,
                                    #pos_hint= {'y':0.05, 'x': 0.5},
                                    pos=(610,40))
        self.bLayout.add_widget(self.mataPencarianButton)
        self.bLayout.add_widget(self.pemelukAgamaButton)
        self.bLayout.add_widget(self.dataPendidikanButton)
        self.bLayout.add_widget(self.dataUmurButton)

        self.dataLayout = RelativeLayout()
        self.dataLayout.add_widget(self.infografik[4])
        
        self.add_widget(self.dataLayout)
        self.add_widget(self.bLayout)
        self.zoomIdx = 0

    ## Filter Button function method ##
    def mataPencarian(self,button = None,**args):
        self.dataLayout.clear_widgets()
        self.dataLayout.add_widget(self.infografik[0])

        # log
        gv.logger.log_button('view :' + 'Mata Pencaharian')

    def pemelukAgama(self,button = None,**args):
        self.dataLayout.clear_widgets()
        self.dataLayout.add_widget(self.infografik[1])

        # log
        gv.logger.log_button('view :' + 'Pemeluk Agama')
        
    def dataPendidikan(self,button = None,**args):
        self.dataLayout.clear_widgets()
        self.dataLayout.add_widget(self.infografik[2])

        # log
        gv.logger.log_button('view :' + 'Pendidikan')

    def dataStrukturUmur(self,button = None,**args):
        self.dataLayout.clear_widgets()
        self.dataLayout.add_widget(self.infografik[3])

        # log
        gv.logger.log_button('view :' + 'Struktur Umur')

    def reset(self):
        self.dataLayout.clear_widgets()
        self.dataLayout.add_widget(self.infografik[4])
        
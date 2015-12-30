__author__ = 'Elian Daiva'

from kivy.app import App
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
from kivy.graphics.transformation import Matrix
from kivy.graphics.instructions import CanvasBase, ContextInstruction
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Ellipse

import gv
#buat akses var global:
#   app = gv.app
#   class Peta = gv.app.peta
#   screen manager = gv.sm
#   logger = gv.logger
#       panggil gv.logger.log_button(*nama button*) buat masukin kegiatan ke log

#mainWindowSize = (1440,900)
mainWindowSize = (1920,1000)

class Peta(Screen):
    def __init__(self, **kwargs):
        super(Peta, self).__init__(**kwargs)

        self.Navigation     = Image(source='peta/lib/Navigation.png', pos_hint = {'x': 0.74, 'y': 0.80}, size_hint= (.2,.1))
        self.legendBatasWil = Image(source='peta/lib/peta-batas-wilayah-keterangan.png', size_hint=(1,1),pos_hint={'center_x':0.5, 'y': None})
        self.legendJalan    = Image(source='peta/lib/peta-jalan-keterangan.png', size_hint=(1,1),pos_hint={'center_x':0.5, 'y': None})
        self.legendAir      = Image(source='peta/lib/peta-air-bersih-keterangan.png', size_hint=(1,1),pos_hint={'center_x':0.5, 'y': None})
        self.legendGorong   = Image(source='peta/lib/peta-gorong-gorong-keterangan.png', size_hint=(1,1),pos_hint={'center_x':0.5, 'y': None})
        self.legendSarana   = Image(source='peta/lib/peta-sarana-publik-keterangan.png', size_hint=(1,2.5),pos_hint={'center_x':0.5, 'y': None})

        ## TOGGLE BUTTON FUNCTION ##
        self.jaringanJalanButton        = ToggleButton(background_normal = 'peta/lib/jalan.png',
                                                background_down = 'peta/lib/jalan-hit.png',
                                                state='normal', 
                                                size_hint=(.78,.25))
        self.jaringanAirBersihButton    = ToggleButton(background_normal = 'peta/lib/air-bersih.png',
                                                background_down = 'peta/lib/air-bersih-hit.png',
                                                state='normal', 
                                                size_hint=(.78,.25))
        self.jaringanGegorongButton     = ToggleButton(background_normal = 'peta/lib/gorong-gorong.png',
                                                background_down = 'peta/lib/gorong-gorong-hit.png',
                                                state='normal', 
                                                size_hint=(.78,.25))
        self.saranaPublik               = ToggleButton(background_normal = 'peta/lib/sarana-publik.png',
                                                background_down = 'peta/lib/sarana-publik-hit.png',
                                                state='normal', 
                                                size_hint=(.78,.25))

        ## BUTTON FUNCTION ##
        self.zoomInButton   = Button(background_normal = 'peta/lib/zoom-in.png',
                                        background_down = 'peta/lib/zoom-in-hit.png',
                                        state='normal', 
                                        size_hint=(.78,.25))
        self.zoomOutButton  = Button(background_normal = 'peta/lib/zoom-out.png',
                                        background_down = 'peta/lib/zoom-out-hit.png',
                                        state='normal', 
                                        size_hint=(.78,.25))

        self.jaringanJalanButton.bind(on_release=self.jalan)
        self.jaringanAirBersihButton.bind(on_release=self.air)
        self.jaringanGegorongButton.bind(on_release=self.gorong)
        self.saranaPublik.bind(on_release=self.sarana)
        
        self.zoomInButton.bind(on_release=self.zoomIn)
        self.zoomOutButton.bind(on_release=self.zoomOut)

        ## Button Container ##
        self.bLayout = BoxLayout(size_hint=(None,None),
                                    orientation='horizontal', 
                                    width = 900,
                                    height= 650,
                                    pos_hint= {'y':0.05, 'x': 0.05})
        self.bLayout.add_widget(self.jaringanJalanButton)
        self.bLayout.add_widget(self.jaringanAirBersihButton)
        self.bLayout.add_widget(self.jaringanGegorongButton)
        self.bLayout.add_widget(self.saranaPublik)
        self.bLayout.add_widget(self.zoomInButton)
        self.bLayout.add_widget(self.zoomOutButton)

        ## LEGEND CONTAINER ##
        self.legendContainer = StackLayout(orientation= 'lr-tb', 
                                        size_hint = (None,None),
                                        minimum_width = 366,
                                        minimum_height= 672,
                                        width = 366,
                                        height = 105,
                                        pos_hint={'x':0.75, 'y':0.70})
        self.legendContainer.add_widget(self.legendBatasWil)
        
        self.mapScreen = MapLayout()

        #self.add_widget(self.mapScreen)
        self.add_widget(self.mapScreen.mapBound)
        self.add_widget(self.bLayout)
        self.add_widget(self.Navigation)
        self.add_widget(self.legendContainer)
        self.zoomIdx = 0

    ## Filter Button function method ##
    def jalan(self,b,**kwargs):
        if b.state == 'down':
            self.mapScreen.addJalan()
            self.legendContainer.add_widget(self.legendJalan)

            # log
            gv.logger.log_button('view :' + 'jalan')
        elif b.state == 'normal':
            self.mapScreen.removeJalan()
            self.legendContainer.remove_widget(self.legendJalan)

            # log
            gv.logger.log_button('close :' + 'jalan')

    def air(self,b,**kwargs):
        if b.state == 'down':
            self.mapScreen.addAir()
            self.legendContainer.add_widget(self.legendAir)

            # log
            gv.logger.log_button('view :' + 'air bersih')
        elif b.state == 'normal':
            self.mapScreen.removeAir()
            self.legendContainer.remove_widget(self.legendAir)

            # log
            gv.logger.log_button('close :' + 'air bersih')

    def gorong(self,b,**kwargs):
        if b.state == 'down':
            self.mapScreen.addGorong()
            self.legendContainer.add_widget(self.legendGorong)

            # log
            gv.logger.log_button('view :' + 'gorong-gorong')
        elif b.state == 'normal':
            self.mapScreen.removeGorong()
            self.legendContainer.remove_widget(self.legendGorong)

            # log
            gv.logger.log_button('close :' + 'gorong-gorong')

    def sarana(self,b,**kwargs):
        if b.state == 'down':
            self.mapScreen.addSarana()
            self.legendContainer.add_widget(self.legendSarana)

            # log
            gv.logger.log_button('view :' + 'sarana')
        elif b.state == 'normal':
            self.mapScreen.removeSarana()
            self.legendContainer.remove_widget(self.legendSarana)

            # log
            gv.logger.log_button('close :' + 'sarana')

    def reset(self):
        self.mapScreen.resetMap()
        self.legendContainer.clear_widgets()
        self.legendContainer.add_widget(self.legendBatasWil)
        self.jaringanJalanButton.state = 'normal'
        self.jaringanAirBersihButton.state = 'normal'
        self.jaringanGegorongButton.state = 'normal'
        self.saranaPublik.state = 'normal' 

    def zoomIn(self,button = None,**args):
        self.mapScreen.zoomingIn()

    def zoomOut(self,button = None,**args):
        self.mapScreen.zoomingOut()

class MapLayout(RelativeLayout):    

    currentSize = 0
    sizeOption = (1,2,4)

    def __init__(self, **kwargs):
        super(MapLayout, self).__init__(**kwargs)

        self.mainContainer = RelativeLayout(size_hint = (None,None), size = mainWindowSize)
        self.mainContainer.currentSize = self.currentSize
        self.mainContainer.sizeOption = self.sizeOption

        self.filterContainer = RelativeLayout(size_hint = (None,None), size = mainWindowSize)

        self.mapBound = ScrollView(size_hint=(None,None), size=mainWindowSize)

        self.MapArray = []      
        self.MapArray.append(Image(source='peta/content/Base Map 1.png',allow_stretch=True))
        self.MapArray.append(Image(source='peta/content/Base Map 2.png',allow_stretch=True))
        self.MapArray.append(Image(source='peta/content/Base Map 3.png',allow_stretch=True))

        self.FilterArray = []
        self.FilterArray.append(Image(source='peta/content/peta-batas-wilayah.png', allow_stretch=True, opacity=.5))        
        self.FilterArray.append(Image(source='peta/content/peta-jalan.png', allow_stretch=True, opacity=.5))        
        self.FilterArray.append(Image(source='peta/content/peta-air-bersih.png', allow_stretch=True, opacity=.6))   
        self.FilterArray.append(Image(source='peta/content/peta-gorong-gorong.png', allow_stretch=True, opacity=.5))        
        self.FilterArray.append(Image(source='peta/content/peta-sarana-publik.png', allow_stretch=True, opacity=.9))        
        
        self.filterContainer.add_widget(self.FilterArray[0])

        self.mainContainer.add_widget(self.MapArray[0])
        self.mainContainer.add_widget(self.filterContainer)     
        
        self.mapBound.add_widget(self.mainContainer)

    def addJalan(self):
        #self.mainContainer.add_widget(self.FilterArray[1])
        self.filterContainer.add_widget(self.FilterArray[1])

    def removeJalan(self):
        #self.mainContainer.remove_widget(self.FilterArray[1])
        self.filterContainer.remove_widget(self.FilterArray[1])

    def addAir(self):
        #self.mainContainer.add_widget(self.FilterArray[2])
        self.filterContainer.add_widget(self.FilterArray[2])
    
    def removeAir(self):
        #self.mainContainer.remove_widget(self.FilterArray[2])
        self.filterContainer.remove_widget(self.FilterArray[2])

    def addGorong(self):
        #self.mainContainer.add_widget(self.FilterArray[3])
        self.filterContainer.add_widget(self.FilterArray[3])

    def removeGorong(self):
        #self.mainContainer.remove_widget(self.FilterArray[3])
        self.filterContainer.remove_widget(self.FilterArray[3])

    def addSarana(self):
        #self.mainContainer.add_widget(self.FilterArray[4])
        self.filterContainer.add_widget(self.FilterArray[4])

    def removeSarana(self):
        #self.mainContainer.remove_widget(self.FilterArray[4])
        self.filterContainer.remove_widget(self.FilterArray[4])

    def resetMap(self):
        self.filterContainer.clear_widgets()
        self.mainContainer.clear_widgets()
        self.filterContainer.add_widget(self.FilterArray[0])
        self.mainContainer.add_widget(self.MapArray[0])
        self.mainContainer.add_widget(self.filterContainer)
        self.mainContainer.currentSize = 0
        anim = Animation(width = mainWindowSize[0], height = mainWindowSize[1], 
            duration = 0.01, t='in_out_sine')
        anim.start(self.mainContainer)
        anim.start(self.filterContainer)

    def zoomingIn(self):
        if self.mainContainer.currentSize + 1 < len(self.mainContainer.sizeOption):
            self.mainContainer.currentSize += 1
            anim = Animation(width = mainWindowSize[0] * self.mainContainer.sizeOption[self.mainContainer.currentSize],
                            height = mainWindowSize[1] * self.mainContainer.sizeOption[self.mainContainer.currentSize], 
                            duration = 0.4,
                            t='in_out_sine')
            anim.start(self.mainContainer)
            anim.start(self.filterContainer)
            if self.mainContainer.currentSize == 1:
                self.mainContainer.clear_widgets()
                self.mainContainer.add_widget(self.MapArray[1])
                self.mainContainer.add_widget(self.filterContainer)
            elif self.mainContainer.currentSize == 2:
                self.mainContainer.clear_widgets()
                self.mainContainer.add_widget(self.MapArray[2])
                self.mainContainer.add_widget(self.filterContainer)

            # log
            gv.logger.log_button('zoom in to :' + str(self.mainContainer.currentSize))
        print self.mainContainer.currentSize
        
    def zoomingOut(self):
        if self.mainContainer.currentSize > 0:
            self.mainContainer.currentSize -= 1
            anim = Animation(width = mainWindowSize[0] * self.mainContainer.sizeOption[self.mainContainer.currentSize],
                            height = mainWindowSize[1] * self.mainContainer.sizeOption[self.mainContainer.currentSize],
                            duration = 0.4,
                            t='in_out_sine')
            anim.start(self.mainContainer)
            anim.start(self.filterContainer)
            if self.mainContainer.currentSize == 1:
                self.mainContainer.clear_widgets()
                self.mainContainer.add_widget(self.MapArray[1])
                self.mainContainer.add_widget(self.filterContainer)
            elif self.mainContainer.currentSize == 2:
                self.mainContainer.clear_widgets()
                self.mainContainer.add_widget(self.MapArray[2])
                self.mainContainer.add_widget(self.filterContainer)

            # log
            gv.logger.log_button('zoom out to :' + str(self.mainContainer.currentSize))
        print self.mainContainer.currentSize 

# class mapApp(App):
#     def build(self):
#         Window.size = mainWindowSize
#         Window.fullscreen = True
#         return Peta()

# if __name__ == '__main__':
#     mapApp().run()




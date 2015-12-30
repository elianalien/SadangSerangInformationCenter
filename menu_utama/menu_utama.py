__author__ = 'Chairun R Siregar'

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.animation import Animation

import gv
#buat akses var global:
#   app = gv.app
#   class MenuUtama = gv.app.menu_utama
#   screen manager = gv.sm
#   logger = gv.logger
#       panggil gv.logger.log_button(*nama button*) buat masukin kegiatan ke log

class MenuUtama(Screen):
    def __init__(self, **kwargs):
        super(MenuUtama, self).__init__(**kwargs)

        # Builder.load_file('menu_utama/style.kv')

        btn_cont = self.ids['btn_menu_utama_cont']

        btn_cont.add_widget(BtnMenuUtama(menu_utama = self,
                                        name = 'e-Kelurahan',
                                        background_normal = 'lib/btn e-kelurahan.png',
                                        background_down = 'lib/btn e-kelurahan down.png',
                                        screen = ''
                                        ))
        btn_cont.add_widget(BtnMenuUtama(menu_utama = self,
                                        name = 'Info Ngabandungan',
                                        background_normal = 'lib/btn info bdg.png',
                                        background_down = 'lib/btn info bdg down.png',
                                        screen = 'Info Ngabandungan'
                                        ))
        btn_cont.add_widget(BtnMenuUtama(menu_utama = self,
                                        name = 'Sadang Serang Interaktif',
                                        background_normal = 'lib/btn sadang serang.png',
                                        background_down = 'lib/btn sadang serang down.png',
                                        screen = '',
                                        submenu = ({'name' : 'Sadang Serang Interaktif - Peta',
                                                    'background_normal' : 'lib/btn peta.png',
                                                    'background_down': 'lib/btn peta down.png',
                                                    'screen' : 'Sadang Serang Interaktif - Peta'
                                                    },
                                                   {'name' : 'Sadang Serang Interaktif - Data',
                                                    'background_normal' : 'lib/btn data.png',
                                                    'background_down': 'lib/btn data down.png',
                                                    'screen' : 'Sadang Serang Interaktif - Data'
                                                    })

                                        ))
        btn_cont.add_widget(BtnMenuUtama(menu_utama = self,
                                        name = 'Rumah Kita',
                                        background_normal = 'lib/btn rumah kita.png',
                                        background_down = 'lib/btn rumah kita down.png',
                                        screen = '',
                                        submenu = ({'name' : 'Rumah Kita - Edukasi Tematik',
                                                    'background_normal' : 'lib/btn info tematik.png',
                                                    'background_down': 'lib/btn info tematik down.png',
                                                    'screen' : 'Rumah Kita - Edukasi Tematik'
                                                    },
                                                   {'name' : 'Rumah Kita - Galeri',
                                                    'background_normal' : 'lib/btn info perkembangan rumah.png',
                                                    'background_down': 'lib/btn info perkembangan rumah down.png',
                                                    'screen' : 'Rumah Kita - Galeri'
                                                    })
                                        ))

        self.submenu = self.ids['submenu']
        self.submenu_cont = self.ids['submenu_cont']
        self.submenu_bg = self.ids['submenu_bg']
        self.submenu_super = self.ids['submenu_super'] # image of the main button

        self.black_mask = self.ids['black_mask']
        self.black_mask.bind(on_press = self.hide_submenu)

        self.submenu_btn_1 = BtnMenuUtama(menu_utama = self,
                                        name = '',
                                        background_normal = '',
                                        background_down = '',
                                        screen = ''
                                    )
        self.submenu_btn_1.pos_hint = {'right': 0.5}
        self.submenu_btn_1.pos[1] = 60

        self.submenu_btn_2 = BtnMenuUtama(menu_utama = self,
                                        name = '',
                                        background_normal = '',
                                        background_down = '',
                                        screen = ''
                                    )
        self.submenu_btn_2.pos_hint = {'x': 0.5}
        self.submenu_btn_2.pos[1] = 60

        self.submenu_cont.add_widget(self.submenu_btn_1)
        self.submenu_cont.add_widget(self.submenu_btn_2)

    def disp_submenu(self, button):
        self.submenu.height = 1080
        self.black_mask.disabled = False
        self.submenu_btn_1.disabled = False
        self.submenu_btn_2.disabled = False

        self.submenu_btn_1.name = button.sub_btn_names[0]
        self.submenu_btn_1.background_normal = 'menu_utama/' + button.sub_btn_bgs[0]
        self.submenu_btn_1.background_down = 'menu_utama/' + button.sub_btn_bg_downs[0]
        self.submenu_btn_1.screen = button.sub_btn_screens[0]

        self.submenu_btn_2.name = button.sub_btn_names[1]
        self.submenu_btn_2.background_normal = 'menu_utama/' + button.sub_btn_bgs[1]
        self.submenu_btn_2.background_down = 'menu_utama/' + button.sub_btn_bg_downs[1]
        self.submenu_btn_2.screen = button.sub_btn_screens[1]

        # sub menu bg & main button image
        self.submenu_cont.pos[0] = button.pos[0] + button.size[0]/2
        self.submenu_super.source = button.background_normal[:-4] + ' super' + button.background_normal[-4:]

        # if it's in the middle or in the right hand position
        if self.submenu_cont.pos[0] < 1400:
            self.submenu_bg.source = 'menu_utama/lib/submenu container.png'
            self.submenu_super.x = -415/2
        else:
            self.submenu_cont.pos[0] = 1410
            self.submenu_bg.source = 'menu_utama/lib/submenu container right.png'
            self.submenu_super.x = -415/2 + 190

        anim = Animation(opacity = 1, duration = 0.3, t='in_out_sine')
        anim.start(self.submenu)

        self.submenu_bg.width = 0
        anim2 = Animation(width = 895, duration = 0.3, t='in_out_sine')
        anim2.start(self.submenu_bg)

        self.submenu_btn_1.pos[1] = 0
        self.submenu_btn_2.pos[1] = 0
        anim3 = Animation(y = 60, duration = 0.3, t='in_out_sine')
        anim3.start(self.submenu_btn_1)
        anim3.start(self.submenu_btn_2)

    def hide_submenu(self, button = None, **args):
        self.submenu.height = 0
        self.black_mask.disabled = True
        self.submenu_btn_1.disabled = True
        self.submenu_btn_2.disabled = True

        anim = Animation(opacity = 0, duration = 0.3, t='in_out_sine')
        anim.start(self.submenu)

        anim2 = Animation(width = 0, duration = 0.3, t='in_out_sine')
        anim2.start(self.submenu_bg)

        anim3 = Animation(y = 0, duration = 0.3, t='in_out_sine')
        anim3.start(self.submenu_btn_1)
        anim3.start(self.submenu_btn_2)

    def reset(self):
        self.hide_submenu()

class BtnMenuUtama(Button):
    def __init__(self, **kwargs):
        super(BtnMenuUtama, self).__init__(**kwargs)

        self.name = kwargs["name"]

        self.menu_utama = kwargs["menu_utama"]

        if(len(self.name) > 0):
            self.background_normal = 'menu_utama/' + kwargs["background_normal"]
            self.background_down = 'menu_utama/' + kwargs["background_down"]

        self.screen = kwargs["screen"]

        self.sub_btn_names = []
        self.sub_btn_bgs = []
        self.sub_btn_bg_downs = []
        self.sub_btn_screens = []

        if 'submenu' in kwargs.keys():
            for submenu_item in kwargs['submenu']:
                self.sub_btn_names.append(submenu_item['name'])
                self.sub_btn_bgs.append(submenu_item['background_normal'])
                self.sub_btn_bg_downs.append(submenu_item['background_down'])
                self.sub_btn_screens.append(submenu_item['screen'])

    def on_release(self):
        gv.logger.log_button(self.name)
        if len(self.screen)>0:
            gv.sm.transition.direction = 'down'
            gv.sm.current = self.screen
        elif len(self.sub_btn_screens)>0:
            self.menu_utama.disp_submenu(self)

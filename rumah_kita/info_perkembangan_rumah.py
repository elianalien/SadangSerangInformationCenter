from kivy.clock import Clock

__author__ = 'elian daiva'

import os, sys, os.path
import math
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

import widgets
import gv
#buat akses var global:
#   app = gv.app
#   class MenuUtama = gv.app.menu_utama
#   screen manager = gv.sm
#   logger = gv.logger
#       panggil gv.logger.log_button(*nama button*) buat masukin kegiatan ke log

#### class of scrollview thumbnail
class InfoPerkembanganRumah(Screen):
	def __init__(self, **kwargs):
		super(InfoPerkembanganRumah, self).__init__(**kwargs)

		# add popup to display pages
		self.album_view = AlbumView()

		# list photos and pages
		self.root_path = 'rumah_kita/'
		self.content_path = self.root_path + 'content/info_perkembangan_rumah/'
		self.photos = []
		self.photo_imgs = []

		self.crnt_book = 0

		for dir, subdir_list, file_list in os.walk( self.content_path, topdown=False):
			# if sub directory
			if len(dir) > len(self.content_path):
				self.photos.append(dir[len(self.content_path):])

		for photo in self.photos:
			self.photo_imgs.append([])
			for photo_imgs in os.listdir(self.content_path + photo + '/'):
				if str.upper(photo_imgs[-4:]) == '.JPG':
					self.photo_imgs[len(self.photo_imgs) - 1].append(photo_imgs)

		album_container = self.ids['album_container']

		# make thumbnails based on
		for i in xrange(len(self.photos)):
			self.btn = widgets.Thumbnail_Btn(label = self.photos[i],
											path = self.content_path + self.photos[i] + '/',
											pages = self.photo_imgs[i],
											index = i,
											)
			album_container.add_widget(self.btn)
			btn_bg = self.btn.ids['bg']
			btn_bg.bind(on_press = self.album_view.open)

		# define album_container height based on the number of photos
		album_container.height = (433 + 6.67) * (math.ceil(len(self.photos) / 4.0))
		self.add_widget(self.album_view)

	def reset(self):
		# Dipanggil tiap screen dibuka
		# Buat kode untuk balikin screen ke keadaan awal
		self.album_view.quick_close()

class AlbumView(RelativeLayout):
	"""docstring for albumView"""
	def __init__(self, **kwargs):
		super(AlbumView, self).__init__(**kwargs)

		self.full_size_viewer = widgets.FullSizeViewer(screen = self,
													   folder_type = 'album',
													   file_type = 'photo')
		self.add_widget(self.full_size_viewer)

		self.photo_container = self.ids['photo_container']

		self.x = gv.screen_width

		self.last_page = 0
		self.pages = []
		Clock.schedule_interval(self.add_photo, 0.5)

	def open(self,b,**kwargs):
		self.photo_container.clear_widgets()

		anim3 = Animation(duration = 0.2) + Animation(x = 0, duration = 0.3)
		anim3.start(self)

		self.photo_container.width = gv.screen_width
		self.photo_container.height = gv.content_height

		self.photo_container.clear_widgets()
		self.pages = b.parent.pages
		self.path = b.parent.path
		# make thumbnails based on

		back_btn = widgets.Thumbnail_Btn(back = True,
										 path = self.path)
		self.photo_container.add_widget(back_btn)
		btn_bg = back_btn.ids['bg']
		btn_bg.bind(on_press = self.close)

		self.last_page = 0

		# log
		gv.logger.log_button('open album :' + b.parent.label.text)

	def add_photo(self, *largs):
		if self.last_page < (len(self.pages)):
			btn = widgets.Thumbnail_Btn(label = self.pages[self.last_page][:-4],
										path = self.path,
										pages= self.pages,
										page_idx = self.last_page)
			self.photo_container.add_widget(btn)
			btn_bg = btn.ids['bg']
			btn_bg.bind(on_press = self.full_size_viewer.open)

			self.last_page += 1

			# define album_container height based on the number of photos deployed
			self.photo_container.height = (433 + 6.67) * (math.ceil((self.last_page + 1) / 4.0))

	def close(self, b = None):
		# if from the back button: log
		if b != None:
			gv.logger.log_button('close album')

		self.full_size_viewer.close()

		self.pages = []
		anim3 = Animation(x = gv.screen_width, duration = 0.2)
		anim3.start(self)

	def quick_close(self):
		self.x = gv.screen_width
		self.full_size_viewer.quick_close()

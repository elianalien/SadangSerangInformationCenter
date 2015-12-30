__author__ = 'Elian Daiva'

import os, sys, os.path
import math
from kivy.uix.screenmanager import Screen

import widgets
import gv
#buat akses var global:
#   app = gv.app
#   class InfoTematik = gv.app.info_tematik
#   screen manager = gv.sm
# 	screen width = gv.screen_width (1920)
# 	screen height = gv.screen_height (1060)
# 	content height = gv.content_height (1000)
#   logger = gv.logger
#       panggil gv.logger.log_button(*nama button*) buat masukin kegiatan ke log


class InfoTematik(Screen):
	def __init__(self, **kwargs):
		super(InfoTematik, self).__init__(**kwargs)

		# add popup to display pages
		self.full_size_viewer = widgets.FullSizeViewer(screen = self,
													   folder_type = 'e-book',
													   file_type = 'page')
		self.add_widget(self.full_size_viewer)

		# list books and pages
		self.root_path = 'rumah_kita/'
		self.content_path = self.root_path + 'content/info_tematik/'
		self.books = []
		self.book_imgs = []

		self.crnt_book = 0

		# list sub directories as books
		for dir, subdir_list, file_list in os.walk( self.content_path, topdown=False):
			# if sub directory
			if len(dir) > len(self.content_path):
				self.books.append(dir[len(self.content_path):])

		# list jpgs as book pages
		for book in self.books:
			self.book_imgs.append([])
			for book_img in os.listdir(self.content_path + book + '/'):
				if str.upper(book_img[-4:]) == '.JPG':
					self.book_imgs[len(self.book_imgs) - 1].append(book_img)

		# book container
		book_container = self.ids['book_container']

		# create thumbnails based on the first page of each book
		for i in xrange(len(self.books)):
			btn = widgets.Thumbnail_Btn(label = self.books[i],
								path = self.content_path + self.books[i] + '/',
								pages = self.book_imgs[i])
			book_container.add_widget(btn)
			btn_bg = btn.ids['bg']
			btn_bg.bind(on_press = self.full_size_viewer.open)

		# define book_container height based on the number of books
		book_container.height = (433 + 6.67) * (math.ceil(len(self.books) / 4.0))

	def reset(self):
		# Dipanggil tiap screen dibuka
		# Buat kode untuk balikin screen ke keadaan awal
		self.full_size_viewer.x = gv.screen_width
		self.full_size_viewer.quick_close()

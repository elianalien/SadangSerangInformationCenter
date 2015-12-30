__author__ = 'Chairun R Siregar'

from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation

import gv

class Thumbnail_Btn(RelativeLayout):
	def __init__(self, **kwargs):
		super(Thumbnail_Btn, self).__init__(**kwargs)

		self.label = self.ids['label']
		self.img = self.ids['img']

		if kwargs.get('back', False):
			self.back = True

			self.label.text = 'ke daftar album'
			self.img.source = 'rumah_kita/lib/back.png'
		else:
			self.back = False

			self.label.text = kwargs["label"]

			self.pages = kwargs["pages"]
			self.path = kwargs["path"]

			self.page_idx = kwargs.get('page_idx', 0)

			self.img.source = self.path + self.pages[self.page_idx]

class FullSizeViewer(RelativeLayout):
	def __init__(self, **kwargs):
		super(FullSizeViewer, self).__init__(**kwargs)

		self.folder_type = kwargs['folder_type']
		self.file_type = kwargs['file_type']

		self.screen = kwargs['screen']

		self.bg = self.ids['bg']
		self.img = self.ids['img']

		self.img_container = self.ids['img_container']

		self.prev_btn = self.ids['prev_btn']
		self.next_btn = self.ids['next_btn']

		# zoom vars
		self.def_size = 950
		self.crnt_zoom = 0
		self.zoom_lvls = [1, 1.5, 2]

		self.img_container.height = gv.content_height
		self.img_container.width = gv.screen_width

		self.quick_close()

	def next_image(self):
		if self.crnt_page < len(self.pages) - 1:
			self.crnt_page += 1
			self.change_image()

			#log
			gv.logger.log_button('next ' + self.file_type +' to :' + str(self.crnt_page))

	def prev_image(self):
		if self.crnt_page > 0:
			self.crnt_page -= 1
			self.change_image()

			#log
			gv.logger.log_button('prev ' + self.file_type +' to :' + str(self.crnt_page))

	# method to move popup into front of screen
	def open(self,b,**kwargs):
		self.pages = b.parent.pages
		self.path = b.parent.path
		self.labels = b.parent.label
		self.crnt_page = b.parent.page_idx

		# reset
		self.change_image()

		# show self
		self.x = 0

		# set starting size
		self.img.height = self.img.width = 500

		self.img_container.width = gv.screen_width
		self.img_container.height = gv.content_height

		# grow in image
		anim = Animation(height = self.def_size, width = self.def_size, duration = 0.3)
		anim.start(self.img)

		# fade in bg
		self.bg.height = gv.content_height
		anim2 = Animation(opacity = 1, duration = 0.3)
		anim2.start(self.bg)

		# log
		if self.folder_type == 'album':
			gv.logger.log_button('open photo :' + b.parent.label.text)
		elif self.folder_type == 'e-book':
			gv.logger.log_button('open e-book :' + b.parent.label.text)

	def close(self):
		# shrink out image
		anim = Animation(height = 310, width = 310, duration = 0.2) + Animation(height = 0, duration = 0)
		anim.start(self.img)

		# fade out bg
		anim2 = Animation(opacity = 0, duration = 0.2) + Animation(height = 0, duration = 0)
		anim2.start(self.bg)

		# hide self
		anim3 = Animation(duration = 0.2) + Animation(x = gv.screen_width, duration = 0)
		anim3.start(self)

		# log
		if self.folder_type == 'album':
			gv.logger.log_button('close photo')
		elif self.folder_type == 'e-book':
			gv.logger.log_button('close e-book')

	def quick_close(self):
		self.img.size = (310, 310)
		self.bg.opacity = 0
		self.x = gv.screen_width

	def change_image(self,*args):
		# change image
		self.img.source = self.path + self.pages[self.crnt_page]

		# activate/deactivate prev or next
		self.prev_btn.opacity = 1
		self.next_btn.opacity = 1

		if self.crnt_page == len(self.pages) - 1:
			self.next_btn.opacity = 0.5

		if self.crnt_page == 0:
			self.prev_btn.opacity = 0.5

	def zoom_in(self):
		if self.crnt_zoom < len(self.zoom_lvls) - 1:
			self.crnt_zoom += 1
			self.zoom(self.def_size * self.zoom_lvls[self.crnt_zoom])

			# log
			gv.logger.log_button('zoom in to :' + str(self.crnt_zoom))

	def zoom_out(self):
		if self.crnt_zoom > 0:
			self.crnt_zoom -= 1
			self.zoom(self.def_size * self.zoom_lvls[self.crnt_zoom])

			# log
			gv.logger.log_button('zoom out to :' + str(self.crnt_zoom))

	def zoom(self, size):
		# animate the image
		anim = Animation(width = size, height = size, duration=0.3)
		anim.start(self.img)

		# animate the image container
		# 	keep minimum size to screen size
		if size > self.img_container.width:
			container_trg_width = size
		else:
			container_trg_width = max(size, gv.screen_width)

		if size > self.img_container.height:
			container_trg_height = size
		else:
			container_trg_height = max(size, gv.content_height)

		anim2 = Animation(width = container_trg_width, height = container_trg_height, duration=0.3)
		anim2.start(self.img_container)
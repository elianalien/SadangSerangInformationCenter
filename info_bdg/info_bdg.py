__author__ = 'Chairun R Siregar'

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.accordion import AccordionItem
from kivy.loader import Loader
from kivy.uix.stencilview import StencilView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.stacklayout import StackLayout

import gv
#buat akses var global:
#   app = gv.app
#   class InfoNgabandungan = gv.app.info_ngabandungan
#   screen manager = gv.sm
#   logger = gv.logger
#       panggil gv.logger.log_button(*nama button*) buat masukin kegiatan ke log

from filter import *
from tweet_fetcher import *
from friendly_time import *
from web_browser import *


class InfoNgabandungan(Screen):

    crntName = "_home_"
    lastTweetId = 1
    animDur = 0.5
    trgHeight = 0
    maxTweet = 30

    def __init__(self, **kwargs):
        super(InfoNgabandungan, self).__init__(**kwargs)

        self.tweetScroll = self.ids['tweet_scroll']
        self.tweetContainer = self.ids['tweet_container']

        #full sized image and website
        self.fullSizedImageFilter = self.ids['full_sized_image_filter']
        self.fullSizedImage = self.ids['full_sized_image']

        self.fullSizedImageFilter.bind(on_press = self.close_full_image)


        #tweets and filters
        TweetFetcher(self)
        Clock.schedule_interval(self.add_tweet, self.animDur)

        self.filters = self.ids['filters']


        #add group of group of filters (AKUN TWITTER and KATA KUNCI / HASHTAG)
        for i in xrange(len(filterSuperGroups)):
            superGroup = FilterSuperGroup(title = filterSuperGroups[i])
            self.filters.add_widget(superGroup, 1)

            #add group of filters ('Pemkot Bandung', 'Persib Bandung', 'Info Lain', etc)
            for j in xrange(len(filterGroups[i])):
                group = FilterGroup(name = filterGroupsFiles[i][j])

                superGroup.accordion.add_widget(group)

                #add filters ('@ridwankamil','@odedmd','@2Serang','@diskominfobdg', etc)
                for k in xrange(len(filters[i][j])):
                    filter = BtnFilter(name = filters[i][j][k])
                    group.filters.add_widget(filter)

        self.btnSemua = self.ids['semua']
        self.btnSemua.bind(on_press = self.disp_all)

        self.base = self.ids['base']

        self.webPageBase = Button()
        self.webPageBase.size_hint = (None, None)
        self.webPageBase.size = (1140, 900)
        self.webPageBase.pos = (405,42.5)
        self.webPageBase.opacity = 0

        self.webPage = CefBrowser()
        self.web_page_width = 1110
        self.web_page_height = 900

    def update(self):
        self.disp_tweets()
   #print "update display"

    def disp_all(self, button, **args):
        self.disp_tweets('_home_')

    # Clear current tweets and parse new text file
    def disp_tweets(self, name = ""):

        if name == "":
            #if refreshing
            self.newToOld = False
            name = self.crntName
        else:
            #if displaying from new source
            self.crntName = name
            self.newToOld = True
            self.trgHeight = 0
            self.tweetContainer.height = 0
            self.tweetContainer.clear_widgets()


        # open the file, or create one if none exists
        try:
            tweetsJSONFile = open("./info_bdg/content/" + name + ".txt")
            tweetsJSON = tweetsJSONFile.read()
            tweetsJSONFile.close()
        except:
            open("./info_bdg/content/" + name + ".txt", "w")
            print name + ".txt file created"
            tweetsJSON = "[]"

        # load JSON form file, or create an empty one of none exists
        try:
            tweetDatas = json.loads(tweetsJSON)
        except:
            tweetDatas = json.loads("[]")

        tweetDatas = byteify(tweetDatas)

        #if refreshing
        if self.newToOld == False:
            #remove already displayed tweets
            newTweetDatas = []
            for i in xrange(len(tweetDatas)):
                if int(tweetDatas[i]["tweet_id"]) > self.lastTweetId:
                    newTweetDatas.append(tweetDatas[i])
                else:
                    break
            tweetDatas = newTweetDatas

        # save newest id, remove >50 tweets, reverse last newTweets idx
        if len(tweetDatas) > 0:
            self.lastTweetId = int(tweetDatas[0]["tweet_id"])
            if len(tweetDatas) > 50:
                del tweetDatas[50:]
            self.lastNewTweetIdx = 0

        #if refreshing, reverse the order so the older ones appear first
        if self.newToOld == False:
            tweetDatas.reverse()

        #add to newTweets to trigger the actual display via add_tweet()
        self.newTweets = tweetDatas

    #full sized image and website
    def disp_full_image(self, texture, srcHeight, trgHeight):
        self.fullSizedImage.texture = texture
        self.fullSizedImage.height = srcHeight
        self.fullSizedImage.opacity = 0

        anim1 = Animation(height = trgHeight, opacity = 1, duration = 0.3)
        anim1.start(self.fullSizedImage)

        self.fullSizedImageFilter.active = True
        self.fullSizedImageFilter.width = 2000
        self.fullSizedImageFilter.height = 2000

        anim = Animation(opacity = 1, duration = 0.3)
        anim.start(self.fullSizedImageFilter)

    def disp_web_page(self, url):
        self.base.add_widget(self.webPageBase)
        self.base.add_widget(self.webPage)

        self.webPage.start_cef(url)
        self.webPage.displaying = True

        self.fullSizedImageFilter.active = True
        self.fullSizedImageFilter.width = 2000
        self.fullSizedImageFilter.height = 2000

        anim = Animation(opacity = 1, duration = 0.3)
        anim.start(self.webPage)
        anim.start(self.fullSizedImageFilter)

    def close_full_image(self, b = None):
        gv.logger.log_button('close pop up')

        self.base.remove_widget(self.webPageBase)
        self.base.remove_widget(self.webPage)

        anim1 = Animation(opacity = 0, duration = 0.3)
        anim1.start(self.fullSizedImage)

        self.fullSizedImageFilter.active = False

        anim = Animation(opacity = 0, duration = 0.3) + Animation(height = 0, duration = 0)
        anim.start(self.fullSizedImageFilter)
        self.webPage.start_cef("")
        self.webPage.displaying = False

    def reset(self):
        # Dipanggil tiap screen dibuka
        # Buat kode untuk balikin screen ke keadaan awal

        self.disp_tweets('_home_')
        self.close_full_image()

    newTweets = []
    lastNewTweetIdx = 99999
    newToOld = True

    def add_tweet(self, *largs):
        # reverse so the older ones will be displayed first
        if self.lastNewTweetIdx < len(self.newTweets):
            tweetData = self.newTweets[self.lastNewTweetIdx]
            tweet = Tweet(**tweetData)
            #if displaying new account
            if self.newToOld:
                # add the tweet at the beginning (bottom) of the stack
                self.tweetContainer.add_widget(tweet)
            #if refreshing
            else:
                # add the tweet at the end (top) of the stack
                self.tweetContainer.add_widget(tweet, len(self.tweetContainer.children))

            # set target height for tweet container
            self.trgHeight += tweet.trgHeight + self.tweetContainer.spacing[1]

            # remove >50 tweets
            if len(self.tweetContainer.children) > self.maxTweet:
                self.trgHeight -= self.tweetContainer.children[0].height + self.tweetContainer.spacing[1]
                self.tweetContainer.children[0].delete()

            # start anim to change tweet container height to target height
            #anim = Animation(height = self.trgHeight, duration = self.animDur)
            #anim.start( self.tweetContainer)
            self.tweetContainer.height = self.trgHeight #testing no animantion
            self.lastNewTweetIdx += 1
        else:
            self.lastNewTweetIdx = 99999

# --- additional widgets ---

# Tweet display
class Tweet(BoxLayout, StencilView):
    trgHeight = 0;
    animDur = 0.5

    def __init__(self, **kwargs):
        super(Tweet, self).__init__(**kwargs)

        contentContainer = self.ids['content_container']

        self.profPic = self.ids['profile_image']
        profPicLoader = Loader.image(kwargs["profile_image"])
        profPicLoader.bind(on_load=self._image_loaded)

        userName = self.ids['user_name']
        userName.text = kwargs["user_name"] + " " + "[size=19][color=075981]" + " @"+kwargs["screen_name"] + " - " + to_friendly_time(kwargs["created_at"]) + "[/color][/size]"
        userName.markup = True


        tweetText = self.ids['tweet_text']
        tweetText.text = kwargs["text"]

        self.linkButton = self.ids['link_button']

        urls = kwargs['urls']
        if len(urls)>0:
            self.link = urls[0]["url"]
            if self.link[:15] != "http://youtu.be":
                self.add_hyperlinks(tweetText, urls)
                self.linkButton.bind(on_release = self.on_ref_pressed_btn)

        self.trgHeight = self.height

        if len(kwargs["media"]) > 0:

            self.addImageCont = self.ids['additional_image_cont']
            self.addImage = self.ids['additional_image']

            self.addImageBtn = self.ids['additional_image_button']

            self.image_url = kwargs["media"][0]['url']
            addImageLoader = Loader.image(self.image_url)
            addImageLoader.bind(on_load=self._add_image_loaded)

            self.addImageCont.height = 300
            self.fullHeight = int(kwargs["media"][0]['lrg_height'])

            self.trgHeight += self.addImageCont.height

        self.height = 0
        self.opacity = 0
        #anim = Animation(height = self.trgHeight, opacity = 1, duration = self.animDur)
        #anim.start(self)
        self.height = self.trgHeight
        self.opacity = 1

    hypStart = '[b][color=075981][ref='
    hypEnd = '[/ref][/color][/b]'

    def add_hyperlinks(self, label, urls):
            #apply in reverse so the char idx doesn't get mixed up
            for i in xrange(len(urls) - 1, -1, -1):
                url = urls[i]
                label.text = label.text[:url["start"]] + self.hypStart + url["url"] + ']' + label.text[url["start"]:url["end"]] + self.hypEnd + label.text[url["end"]:]

            label.markup = True

    def _image_loaded(self, proxyImage):
        if proxyImage.image.texture:
            self.profPic.texture = proxyImage.image.texture

    def _add_image_loaded(self, proxyImage):
        if proxyImage.image.texture:
            self.addImage.texture = proxyImage.image.texture

            self.addImage.opacity = 0
            #anim = Animation(opacity = 1, duration = self.animDur)
            #anim.start(self.addImage)
            self.addImage.opacity = 1

            self.addImageBtn.bind(on_press = self.on_image_pressed)

    def on_image_pressed(self, button, **args):
        gv.logger.log_button('view image: ' + self.image_url)
        gv.app.info_ngabandungan.disp_full_image(self.addImage.texture, self.addImage.height, self.fullHeight)

    def on_ref_pressed_btn(self, btn, *largs):
        gv.logger.log_button('view web page: ' + self.link)
        gv.app.info_ngabandungan.disp_web_page(self.link)

    def delete(self):
        self.parent.remove_widget(self)


# Filter display
class FilterSuperGroup(StackLayout):
    def __init__(self, **kwargs):
        super(FilterSuperGroup, self).__init__(**kwargs)

        title = self.ids['title']
        title.text = kwargs["title"]

        self.accordion = self.ids['accordion']

class FilterGroup(AccordionItem):
    def __init__(self, **kwargs):
        super(FilterGroup, self).__init__(**kwargs)

        self.bind(on_release = self.log_press)
        self.name = kwargs['name']

        self.background_normal = "info_bdg/lib/filter " + self.name + ".png"
        self.background_selected = "info_bdg/lib/filter " + self.name + " slct.png"

        self.filters = self.ids['filters']

    def log_press(self, b):
        gv.logger.log_button('filter group: ' + self.name)


class BtnFilter(ToggleButton):
    def __init__(self, **kwargs):
        super(BtnFilter, self).__init__(**kwargs)

        self.text = kwargs["name"]

    def on_release(self):
        gv.logger.log_button('filter: ' + self.text)
        gv.app.info_ngabandungan.disp_tweets(self.text)


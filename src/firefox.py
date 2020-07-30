import json
import re
import time
import ast
from datetime import datetime
from random import randrange

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Firefox(object):
  firefox = None

  def setUp(self, headless, firefox_binary_path):

    options = Options()
    options.headless = headless
    options.binary = firefox_binary_path
    firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
    firefox_capabilities['marionette'] = True
    firefox_capabilities['binary'] = firefox_binary_path
    firefox_binary = FirefoxBinary(firefox_binary_path)

    self.firefox = webdriver.Firefox(firefox_options=options, capabilities=firefox_capabilities, firefox_binary=firefox_binary, executable_path=GeckoDriverManager().install())

  def openWebsite(self, website):
    self.firefox.get(website)

    print('[{}] Openning Instagram: {}'.format(datetime.utcnow(), website))

    time.sleep(5)

  def makeLogin(self, username, password):
    self.firefox.find_element_by_name("username").send_keys(username)
    self.firefox.find_element_by_name("password").send_keys(password)
    self.firefox.find_element_by_name("password").send_keys(u'\ue007')

    print('[{}] Login successfull: {}'.format(datetime.utcnow(), username))

    time.sleep(10)

  def disableNotifiers(self):
    self.firefox.find_element_by_xpath("//*[contains(text(), 'Not Now')]").send_keys(u'\ue007')

    time.sleep(10)

    self.firefox.find_element_by_xpath("//*[contains(text(), 'Not Now')]").send_keys(u'\ue007')

    print('[{}] Disabling after-login features'.format(datetime.utcnow()))

    time.sleep(10)

  def loadProfilesToUnfollow(self, file_location_to_unfollow):
    i_will_unfollow_list = []

    with open(file_location_to_unfollow, 'r') as f:
      i_will_unfollow_list = json.load(f)
      print('[{}] List of not followers has been loaded'.format(datetime.utcnow()))

    return i_will_unfollow_list

  def unfollowList(self, i_will_unfollow_list):
    unfollowed = 0
    for profile in i_will_unfollow_list:
      if unfollowed >= 15:
        print('[{}] STOPPING UNFOLLOW FOR 15 MINUTES'.format(datetime.utcnow()))
        time.sleep(900)
        print('[{}] CONTINUING UNFOLLOW PROCESS'.format(datetime.utcnow()))
        unfollowed = 0

      self.unfollow(profile)
      unfollowed += 1

  def unfollow(self, profile):
    print('[{}] Stopping follow: {}'.format(datetime.utcnow(), profile['username']))

    # find profile
    find_profile = self.firefox.find_element_by_xpath("//input[@placeholder='Search']")
    find_profile.send_keys(profile['username'])

    print('[{}] Writed profile in search: {}'.format(datetime.utcnow(), profile['username']))
    time.sleep(2 + randrange(7))

    # apply search
    find_profile.send_keys(u'\ue007')

    print('[{}] Profile located: {}'.format(datetime.utcnow(), profile['username']))
    time.sleep(10 + randrange(7))

    # enter inside profile
    self.firefox.find_element_by_xpath('//a[@href=\'/{}/\']'.format(profile['username'])).send_keys(u'\ue007')

    print('[{}] Profile oppened: {}'.format(datetime.utcnow(), profile['username']))
    time.sleep(5 + randrange(7))

    # click stop follow
    following_button = self.firefox.find_element_by_xpath('//span[@aria-label="Following"]')
    following_button1 = following_button.find_element_by_xpath('..')
    following_button1.find_element_by_xpath('..').send_keys(u'\ue007')

    print('[{}] Clicked to stopped following: {}'.format(datetime.utcnow(), profile['username']))
    time.sleep(6 + randrange(2))

    self.firefox.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").send_keys(u'\ue007')

    print('[{}] Finish unfollow with success: {}'.format(datetime.utcnow(), profile['username']))
    print('---------------------------------------------------------------')
    time.sleep(5 + randrange(10))

  def closeWebsite(self):
    self.firefox.quit()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://code.google.com/apis/newssearch/v1/jsondevguide.html
# Copyright (c) 2010 Toomore Chiang, http://toomore.net/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import urllib, urllib2
import time, datetime
from datetime import timedelta

try:
  import simplejson as json
except:
  from django.utils import simplejson as json

class gnews(object):
  def __init__(self, q = '', topic = '', rsz = 4):
    a = urllib2.urlopen('https://ajax.googleapis.com/ajax/services/search/news?%s&ned=tw&hl=zh-tw' %
    urllib.urlencode({
      'v': '1.0',
      'q': q,
      'rsz': rsz,
      'topic': topic
      })
    )
    self.j = json.loads(a.read())

  def p(self):
    print self.j['responseData']['cursor']['estimatedResultCount']
    for i in self.j['responseData']['results']:
      print i['titleNoFormatting']
      print i['content']
      print '-' * 10
      print i['publishedDate'],i['publisher']
      print i['unescapedUrl']
      print '=' * 15

  def x(self):
    rt = ''
    for i in self.j['responseData']['results']:
      rt += '\r\n' + i['titleNoFormatting'] + '-' + i['publisher'] + '-' + self.covdate(i['publishedDate']) + '\r\n'
      rt += i['unescapedUrl']
    return rt

  def covdate(self, timestring):
    #timestring = "Sat, 27 Nov 2010 23:14:42"
    time_format = "%a, %d %b %Y %H:%M:%S"
    a = datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring[:-6], time_format)))
    return str(a + timedelta(hours = 16))

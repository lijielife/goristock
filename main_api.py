#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from django.conf import settings
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.shortcuts import render_to_response

## GAE lib
#from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

from grs import goapi

#Third Libraries
import webapp2

############## webapp Models ##############
class apidoc(webapp2.RequestHandler):
  def get(self):
    hh_api = memcache.get('hh_api')
    if hh_api:
      pass
    else:
      hh_api = render_to_response('hh_api.htm',{}).content
      memcache.set('hh_api', hh_api, 60*60*6)
    self.response.write(hh_api)

class stock_j(webapp2.RequestHandler):
  def get(self):
    reapi = goapi.goapi(self.request.get('q')).stock_j
    self.response.write(render_to_response('api.htm',{'reapi': reapi}).content)

class stock_real(webapp2.RequestHandler):
  def get(self):
    reapi = goapi.goapi(self.request.get('q')).stock_real
    self.response.write(render_to_response('api.htm',{'reapi': reapi}).content)

class weight(webapp2.RequestHandler):
  def get(self):
    reapi = goapi.weight()
    self.response.write(render_to_response('api.htm',{'reapi': reapi}).content)

class liststock(webapp2.RequestHandler):
  def get(self):
    reapi = goapi.stocklist()
    self.response.write(render_to_response('api.htm',{'reapi': reapi}).content)

class searchstock(webapp2.RequestHandler):
  def get(self):
    reapi = goapi.searchstock(self.request.get('q'))
    self.response.write(render_to_response('api.htm',{'reapi': reapi}).content)

class news(webapp2.RequestHandler):
  def get(self):
    reapi = goapi.newsapi(self.request.get('q'))
    self.response.write(render_to_response('api.htm',{'reapi': reapi}).content)

############## redirect Models ##############
class rewrite(webapp2.RequestHandler):
  def get(self):
    self.redirect('/API')

############## main Models ##############
application = webapp2.WSGIApplication(
              [
                ('/API', apidoc),
                ('/API/stock', stock_j),
                ('/API/real', stock_real),
                ('/API/weight', weight),
                ('/API/liststock', liststock),
                ('/API/searchstock', searchstock),
                ('/API/news', news),
                ('/API.*', rewrite)
              ],debug=True)

def main():
  application.run()

if __name__ == '__main__':
  main()
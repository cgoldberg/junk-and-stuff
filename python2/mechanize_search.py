#!/usr/bin/env python
#  2010 Corey Goldberg
#
#  examples using python-mechanize


import mechanize


br = mechanize.Browser()

br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
#br.set_handle_referer(True)
br.set_handle_robots(False)

#br.set_debug_http(True)

br.addheaders = [('User-agent', 'Mozilla/5.0 Compatible')]

resp = br.open('http://www.python.org')
resp.read()
#print resp.code
#print resp.msg
#print resp.info()
#print resp.get_data()

for f in br.forms():
    print f

br.select_form(nr=0)
br.form['q']='foo'
br.submit()
print br.response().read()

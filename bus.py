#!/usr/bin/python
# -*- coding: utf-8 -*-
#read from file a list of urls (one url per line) and output the shortened

from __future__ import with_statement
import pycurl, json
import sys
import time
import cStringIO

url = "https://www.googleapis.com/urlshortener/v1/url"


with open(sys.argv[1], "r") as f:
  f.seek (0, 2)           # Seek @ EOF
  fsize = f.tell()        # Get Size
  f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
  lines = f.readlines()       # Read to end


for line in lines:
  data = json.dumps({"longUrl": line})
  response = cStringIO.StringIO()

  c = pycurl.Curl()
  c.setopt(pycurl.URL, '%s' % url)
  c.setopt(pycurl.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/json'])
  c.setopt(pycurl.VERBOSE, 0)
  c.setopt(pycurl.POST, 1)
  c.setopt(c.WRITEFUNCTION, response.write)
  c.setopt(pycurl.POSTFIELDS, data)
  c.perform()
  c.close()
  resp=response.getvalue().split("id\":")[1].split(",")[0].replace("\"","")
  print "{}\t{}".format(line.replace("\n",""),resp)

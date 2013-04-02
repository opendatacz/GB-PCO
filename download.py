#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, requests
from datetime import date, datetime, timedelta

BASE_URI = "http://online.contractsfinder.businesslink.gov.uk/public_files/Notices/"
RECENT_NOTICES = BASE_URI + "Recent/notices.xml"
MONTHLY_NOTICES = BASE_URI + "Monthly/notices_{year:d}_{month:02d}.xml"
DOWNLOADED_FILES = os.listdir("download")

def download(url):
  print("[INFO] Downloading {0}...".format(url))
  req = requests.get(url)
  if req.status_code == 200:
    return req.text.encode("UTF-8")
  else:
    raise Exception("Failed to download URL: {0}".format(url))

def get(month, year):
  filename = getFilename(month, year)
  if not filename in DOWNLOADED_FILES: 
    url = MONTHLY_NOTICES.format(month = month, year = year)
    response = download(url)
    store(response, filename)

def getFilename(month, year):
  return "{year:d}-{month:02d}.xml".format(month = month, year = year)

def getRecent():
  filename = "recent.xml"
  if not filename in DOWNLOADED_FILES:
    store(download(RECENT_NOTICES), filename)

def store(data, filename):
  with open(os.path.join("download", filename), "w") as file:
    file.write(data)

def main(): 
  now = datetime.now().date()
  limit = date(2010, 12, 31)
  month = timedelta(days = 30)
  current = now - month
  
  while current > limit:
    get(current.month, current.year)
    current = current - month
  
  getRecent()

if __name__ == "__main__":
  main()

#!/usr/bin/env python
from __future__ import print_function
import requests
import dreqPy
import cmor

# CV

r = requests.get("https://github.com/WCRP-CMIP/CMIP6_CVs/releases")
cvtag = r.text.split('tag-name">')[1].split("</span")[0].strip()
print(cvtag)

# Dreq
dreqtag = dreqPy.version

# cmor 
cmortag = "{}.{}.{}".format(cmor.CMOR_VERSION_MAJOR, cmor.CMOR_VERSION_MINOR, cmor.CMOR_VERSION_PATCH)

# Tables
r = requests.get("https://github.com/PCMDI/cmip6-cmor-tables/releases")
print(r.text)
tablestag = cmortag

print("CVs:", cvtag)
print("DREQ:", dreqtag)
print("CMOR:", cmortag)

print("FULL: CMIP6_CVs-{}/DREQ-{}/CMIP6_CMOR_tables-{}".format(cvtag, dreqtag, tablestag))


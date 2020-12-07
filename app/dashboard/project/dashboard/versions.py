#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import os

def get_versions():

  user = os.environ['GH_USER']
  image = os.environ['GH_IMAGE']

  r = requests.get(f"https://github.com/users/{user}/packages/container/{image}/versions")
  html = BeautifulSoup(r.text, 'html.parser')

  tags = html.find_all('a', class_='Label')
  return [x.text for x in tags]

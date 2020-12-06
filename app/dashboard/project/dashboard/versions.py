#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests

def get_versions():

  image = 'temperature_reader'

  r = requests.get(f"https://github.com/users/martinparadiso/packages/container/{image}/versions")
  html = BeautifulSoup(r.text, 'html.parser')

  tags = html.find_all('a', class_='Label')
  return [x.text for x in tags]

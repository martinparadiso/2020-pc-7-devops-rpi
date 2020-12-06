#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests


def get_version_disp(ip):
  ulr = f''http://{ip}:1221/version''
	resultado = requests.get(url)
  resultado = resultado.json()['version']
  return(resultado)  

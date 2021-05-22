'''
This code uses requests and beautifulsoup
module to find meaning of a word as given in
dictionary.com.
usage:
python dictionary_scraper.py word
If no word is given it will raise an error
'''

import re
import sys

import requests
from bs4 import BeautifulSoup

# using dictionary.com for finding word meaning
WEBSITE = 'https://www.dictionary.com/browse/'

try:
  WORD = sys.argv[1]
except IndexError:
  print('You didnt input the word')
  sys.exit(-1)

URL = WEBSITE + WORD

# get the html pSOUPwith definitions
PAGE = requests.get(URL)

# create a soup element
SOUP = BeautifulSoup(PAGE.content, 'html.parser')

# get the section with all definSOUPns along
# with parts of speech
# upon inspection class=css-1avshm7 e16867sm0
# refers to div that contains the definitions
DIV_WITH_DEFS = SOUP.find('div', class_='css-1avshm7 e16867sm0')


# there are multiple sections with definitions
# eah section for a particular parts of speech
SECTION_LISTS = DIV_WITH_DEFS.find_all('section',
                                       class_=re.compile("^css-pnw38j "))

# if No such word exists in diictionary, then no sections present
if SECTION_LISTS == []:
  print('No word found in dictionary')
  sys.exit(-1)

for section in SECTION_LISTS:
  part_of_speech = section.find('h3').text

  # get the definitions
  definitions = section.find_all('div', {'class': re.compile("^css-"),
                                         'value': re.compile("[0-9]+")})

  # print the definitions
  print(part_of_speech)
  for index, definition in enumerate(definitions):
    print('\t', index+1, '. ', definition.text)
  print('---------------------------------------\
         -------------------------------\n')

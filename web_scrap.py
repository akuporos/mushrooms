import requests
import pathlib
import os
import urllib
from bs4 import BeautifulSoup

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def parse_pages(filename):
    results = {}
    text = read_file(filename)

    soup = BeautifulSoup(text)
    #Get caption
    caption = soup.find_all('div', {'class': 'caption'})
    dimension = soup.find_all('div', {'class': 'labelus'})
    descr_dim = soup.find_all('div', {'class': ['textus', 'longtextus']})
    mushroom_name = []
    mushroom_info = []
    for item in caption:
        caption_name = item.find('b')
        tag_list = caption_name.contents
        tag_list[0] = tag_list[0].replace(u'\xa0', u' ')
        tag_list[0] = tag_list[0].replace(u'\n', u' ')
        tag_list[0] = tag_list[0].split('(')[0]
        tag_list[0] = tag_list[0].strip()
        tag  = tag_list[0]
        '''mushroom_name.append(tag)
        for dim, descr in zip(dimension, descr_dim):
            str = dim.contents[0] + ' ' + descr.contents[0]
            mushroom_info.append(str)
           ''' '''name = dim.text
_descr = descr.text
if (name == 'Dimensions'):
    print(tag, name, _descr)
if (name == 'Description'):
    print(tag, name, _descr)
    break'''
        #Make dir
      #  pathlib.Path('./Inedible/' + tag).mkdir(parents=True, exist_ok=True)

    '''
    #Download images
    images_tag = soup.find_all('div', {'class': 'images'})
    for image_tag in images_tag:
        image_number = 1
        concrete_image_tag = image_tag.find_all('div', {'class' : 'image'})
        for _concrete_image_tag in concrete_image_tag:
            concrete_image_ref = _concrete_image_tag.find('a', {'class' : 'fancybox'}).get('href')
            mushroom_title_dir = _concrete_image_tag.find('a', {'class' : 'fancybox'}).get('title')
            mushroom_title_img = mushroom_title_dir.split()[0] + '_' + mushroom_title_dir.split()[1]
            concrete_image_ref = concrete_image_ref.split('/..')[1]
            concrete_image_ref = 'http://www.mushroom.world/%s' % (concrete_image_ref)
            path_to_image = ('./Inedible/' + mushroom_title_dir + '/' + mushroom_title_img + '_' + '%d' + '.jpg') % (image_number)
            image_number +=1
            urllib.request.urlretrieve(concrete_image_ref, path_to_image)
    '''
    return results
'''
pathlib.Path('./inedible_pages/').mkdir(parents=True, exist_ok=True)
#Download pages
for page in range(7):
    url = 'http://www.mushroom.world/mushrooms/inedible?page=%d' % (page)
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text)
    mushrooms_list = soup.find('div', {'id': 'mushroom-list'})
    with open('./inedible_pages/page_%d.html' % (page), 'wb') as output_file:
        output_file.write(mushrooms_list.encode('cp1251'))
'''
results = []
for filename in os.listdir('./inedible_pages/'):
    results.extend(parse_pages('./inedible_pages/' + filename))








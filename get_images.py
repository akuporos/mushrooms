import os
import urllib
from bs4 import BeautifulSoup
import requests
import glob
import logging

def send_request_and_get_list(cnt_page, name_for_ref):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    session = requests.Session()
    url = 'http://mushroomobserver.org/image/image_search?page={}&pattern='.format(cnt_page) + name_for_ref
    request = session.get(url, headers=headers)
    if request.status_code != 200:
        logging.error("Request for" + " " + name_for_ref + " " + "in page" + " " + str(cnt_page) + " is failed " + request.raise_for_status())
    text = request.text
    soup = BeautifulSoup(text)
    # find page count
    all_mushrooms = soup.find('div', {'class': 'push-down push-up'})
    all_mushrooms_results = all_mushrooms.find('div', {'class': 'results'})
    return  all_mushrooms_results

def find_last_page(page_count_tag_list):
    size_of_page_count_tag_list = round(len(page_count_tag_list)/2)
    size_of_page_count_tag_list -= 2
    concrete_tag = page_count_tag_list[size_of_page_count_tag_list].find('a')
    last_page = concrete_tag.text
    return int(last_page)

def download_concrete_image(concrete_mushroom_image, name, is_first):
    image_container_tag = concrete_mushroom_image.find('div', {'class' : 'thumbnail-container'})
    image_tag = image_container_tag.find('div', {'data-toggle' : 'expand-icon'})
    image_reference_tag = image_tag.find_all('a')
    image_tag = image_reference_tag[1].get('data-title')
    image_reference = BeautifulSoup(image_tag)
    reference = image_reference.a['href']
    logging.info(reference + 'is downloadwing')
    #find and create a path to mushroom directory, where pictures will be upload
    path = '*/*/' + name
    path_to_directory = './' + glob.glob(path)[0] + '/'
    path_to_directory = path_to_directory.replace('\\', '/')
    mushroom_title_img = name.split()[0] + '_' + name.split()[1]
    #count the current number of pictures
    image_number = len([name for name in os.listdir(path_to_directory) if os.path.isfile(os.path.join(path_to_directory, name))])
    image_number += 1
    #download image
    path_to_image = (path_to_directory + '/' + mushroom_title_img + '_' + '%d' + '.jpg') % (image_number)
    try:
        urllib.request.urlretrieve(reference, path_to_image)
    except urllib.URLError as e:
        logging.error("Failed to download " + reference + " to " + path_to_image + "with code" + e.code)
    return

#цикл по страницам
def download_pictures(all_mushrooms_results, last_page, name):
    cnt_page = 1
    mushrooms_list = []
    is_first = True
    name_for_ref = name.split()[0] + "+" + name.split()[1]
    while cnt_page <= last_page:
        logging.info(str(cnt_page) + 'is downloadwing')
        #all pictures of mashrooms on this page
        mushrooms_list = all_mushrooms_results.find_all('div', {'class': 'col-xs-12 col-sm-6 col-md-4 col-lg-4'})
        #download pictures from this page
        for concrete_mushroom_image in mushrooms_list:
            download_concrete_image(concrete_mushroom_image, name, is_first)
        cnt_page += 1
        #new page
        all_mushrooms_results = send_request_and_get_list(cnt_page, name_for_ref)
    return

def main():
    logging.basicConfig(format= u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s', filename='myapp.log', level=logging.ERROR)
    with open('mushrooms.txt') as file:
        mushroom_names = file.readlines()
    mushroom_names = [x.strip() for x in mushroom_names]
    for name in mushroom_names:
        logging.info(name + 'is downloadwing')
        name_for_ref = name.split()[0] + "+" + name.split()[1]
        all_mushrooms_results = send_request_and_get_list(1, name_for_ref)
        #find page count
        page_count = all_mushrooms_results.find_all('li')
        last_page = find_last_page(page_count)
        #download pictures for this name
        download_pictures(all_mushrooms_results, last_page, name)

if __name__ == '__main__':
    main()
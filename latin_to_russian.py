import glob
import json
import codecs

def main():
    data = json.load(open('data.json'))
    list_of_mushrooms_names = list(data.keys())
    with codecs.open('russian list.txt', 'r', 'utf-8') as file:
        latin_russian_mushrooms_list = file.readlines()
    latin_russian_mushrooms_list = [x.strip() for x in latin_russian_mushrooms_list]
    for mushroom_name in list_of_mushrooms_names:
        path = '*/*/' + mushroom_name
        path_to_directory = './' + glob.glob(path)[0] + '/'
        sort = path_to_directory.split('\\')[1]
        data[mushroom_name] = sort + " " + data[mushroom_name]
        for russian_mushroom_name in latin_russian_mushrooms_list:
            if russian_mushroom_name.find(mushroom_name) != -1:
                russian_name = russian_mushroom_name.split()[0] + " " + russian_mushroom_name.split()[1]
                data[mushroom_name] = russian_name + " " + data[mushroom_name]

    with open('data.json', 'w') as outfile:
        json_data = json.dump(data, outfile)
if __name__ == '__main__':
    main()
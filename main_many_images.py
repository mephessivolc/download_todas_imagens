import os 
import urllib.request
import requests
from bs4 import *

def download_image(url, file_path, file_name):
    full_path = os.path.join(file_path, f"{file_name}")
    try:
        urllib.request.urlretrieve(url, full_path)
        return True
    except:
        raise 

def download_images_in_one_url(images, folder_name):
    count = 0
    print(f"Found {len(images)} images")
    if len(images) != 0:
        for i, image in enumerate(images):
            image_link = image["src"]
            r = requests.get(image_link).content
            with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                f.write(r)
                count += 1
        if count == len(images):
            print("All the images have been downloaded!")
        else:
            print(f" {count} images have been downloaded out of {len(images)}")

def main(url, full_path):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    # folder_create(images)
    download_images_in_one_url(images, full_path)

url = input('Please enter image URL (string): ')

dir_name = input("Please insert directory name: ")
path = os.path.join(os.getcwd(), dir_name)

isExists = os.path.exists(path)

if not isExists:
    os.mkdir(path)

one_url = input("Is unique url? (y/n)")
if one_url == 'y':
    main(url, dir_name)

else:
    file_name = url.split("/")[-1]
    tmp_file_name = file_name.split('.')
    tmp_name = tmp_file_name[0] #nome original do arquivo
    tmp_ext_name = tmp_file_name[1] # extensao original do arquivo

    cont = 0
    for i in reversed(tmp_name):
        if i.isnumeric():
            cont = cont + 1
            tmp_name = tmp_name[:-1]

    cont1 = 0
    for i in reversed(url):
        if not i == "/":
            cont1 = cont1 + 1

        if i == "/":
            break

    tmp_url = url[:-cont1]

    print(tmp_url+"\n")
    print(url+"\n")
    number = 1
    while download_image(url, path, file_name):
        number = number + 1
        doc_name = f"{tmp_name}{str(number).zfill(cont)}.{tmp_ext_name}"
        file_name = f"{doc_name}"
        url = f"{tmp_url}{doc_name}"
        # print(url)
        print(f"{file_name} Image download successfully")

    # download_image(url, path, file_name)
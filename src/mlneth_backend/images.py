#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError, ImgurClientRateLimitError
import re
import urllib.request
from urllib.parse import urlparse
from config import *
from passwords import *
import imghdr
from PIL import Image


imgur = ImgurClient(client_id, client_secret)


def get_imgur_id(download_url):
    pattern = re.compile(u'imgur.com/(\w*)(?:.|$)')
    matches = re.findall(pattern, download_url)
    if matches:
        imgur_id = matches[0]  # only imgur banner id
    else:
        imgur_id = 0
    return imgur_id


def get_imgur_link(imgur_id):
    return imgur.get_image(imgur_id).link


def file_extension(url):
    a = urlparse(url)
    path, extension = os.path.splitext(a.path)
    print(extension[1:])
    return extension[1:]


def is_valid_extension(extension):
    if extension in IMAGE_FORMATS:
        return True


def is_valid_file(path):
    content = imghdr.what(path)
    if content in IMAGE_FORMATS:
        return True
    else:
        print("Wrong file content {}".format(content))
        return False


def resise_image(local_path_orig, width, height):
    im = Image.open(local_path_orig)
    resized_image = im.resize((width, height))
    file_name = os.path.basename(local_path_orig)
    path = BANNERS_FOLDER + file_name
    resized_image.save(path)
    return path


def download_image(id, src, width, height):
    error = ''
    local_path = ''

    try:
        imgur_id = get_imgur_id(src)
        if imgur_id != 0:
            src = get_imgur_link(imgur_id)
        # Download 
        # TODO huge file protection
        ext = file_extension(src)
        if (is_valid_extension(ext) is not True):
            return ('', 'Wrong format - please upload .jpg or .png image.')

        local_path_orig = DOWNLOAD_FOLDER + str(id) + '.' + ext
        urllib.request.urlretrieve(src, local_path_orig)
        if (is_valid_file(local_path_orig) is not True):
            return ('', 'Wrong file contents - please upload .jpg or .png image.')

    except ImgurClientError as e:
        if str(e.error_message)[:35] == "Unable to find an image with the id":  # TODO set to 35!
            print("Imgur. Got invalid imgur image id: " + str(imgur_id))
            error += "No such image on imgur"
            return ('', error)
        else:
            print ("Imgur error: " + str(e.error_message))
            # logging.error("Imgur error: " + str(e.error_message))
            error += "ERROR: No such image on imgur"
            return ('', error)
    # except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
    #     # logging.warning("Imgur. No internet connection: " + str(e.message))
    #     pass
    except (ImgurClientRateLimitError, ImgurClientError) as e:
        # logging.warning("Imgur. " + str(e.message))
        return ('', error)
        pass

    local_path = resise_image(local_path_orig, width, height)
    return (local_path, error)




# BIG PICTURE
def new_big_picture(big_picture_insertion):
    # logging.debug("BigPicture. Rendering bitmap...")
    # new_big_picture_bitmap = Image.new("RGB", (1000, 1000), "#ffffff")  # TODO use bg image instead
    
    new_big_picture_bitmap = Image.open(BIG_PICTURE_BG)
    for banner in big_picture_insertion:
        # if banner.error == '':
        if banner.local_path != '':
            box = (banner.x1, banner.y1, banner.x2, banner.y2)
            im = Image.open(banner.local_path)
            cropping_box = (0, 0, banner.x2 - banner.x1, banner.y2 - banner.y1)
            cropped_im = im.crop(cropping_box)
            new_big_picture_bitmap.paste(cropped_im, box)
    latest_banner_id = big_picture_insertion[0].id
    path = BIG_PICTURE_LOCAL_PATH + str(latest_banner_id) + '.png'
    new_big_picture_bitmap.save(path, "PNG")
    return path



def main():
    result = download_image(12, 'https://imgur.com/6cULacW', 1200, 1600)
    result = download_image(13, 'https://meduza.io/image/attachments/images/003/326/751/large/GfSuy14cR6kHMvPTDarGZA.jpg', 1200, 1600)
    print(result[0])

if __name__ == '__main__':
    # event_name, from_block, logger
    main()

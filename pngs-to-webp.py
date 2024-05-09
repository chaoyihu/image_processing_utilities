# Example: Downloading and converting all png images in the pokemon catelog.

import requests
from bs4 import BeautifulSoup
import os
import subprocess
import time

page_marks = [
    '',
    '&filefrom=%2A076%0A076Golem+Dream.png#mw-category-media',
    '&filefrom=%2A143%0A143Snorlax+Dream+6.png#mw-category-media',
    '&filefrom=%2A226%0A226Mantine+Dream.png#mw-category-media',
    '&filefrom=%2A352%0A352Kecleon+Dream.png#mw-category-media',
    '&filefrom=%2A463%0A463Lickilicky+Dream.png#mw-category-media',
    '&filefrom=%2A570%0A570Zorua+Hisui+Dream.png#mw-category-media',
    '&filefrom=%2A676%0A676Furfrou+Pharaoh+Dream.png#mw-category-media',
    '&filefrom=%2A784%0A784Kommo-o+Dream.png#mw-category-media',
    '&filefrom=%2A890%0A890Eternatus+Dream.png#mw-category-media',
    '&filefrom=Dream+Park+02.png#mw-category-media'
]
pages = ['https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_artwork' + page_mark for page_mark in page_marks]


def get_page(url):
    print("Request page:", url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Request succeeded: 200")
        else:
            print("Request failed:", image_page.status_code)
            return 0
    except Exception as e:
        print("Error occurred during the request:", e)
        return 0
    soup = BeautifulSoup(response.content, 'html.parser')
    png_items = soup.find_all('a', href=lambda href: href and href.endswith('.png'))
    png_links = [ele['href'] for ele in png_items]
    
    success_count = 0
    for png_link in png_links:
        image_name = png_link.split(':')[-1]
        png_data = get_png_data(png_link)
        success = process_image(png_data, image_name)
        if success:
            success_count += 1
    print(f"{ success_count } PNGs downloaded and converted to WEBP.")
    return success_count


def get_png_data(png_link):
    png_link = 'https://archives.bulbagarden.net' + png_link

    print("Request page:", png_link)
    try:
        png_page_response = requests.get(png_link)
        if png_page_response.status_code == 200:
            print("Request succeeded: 200.")
        else:
            print("Request failed:", image_page.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", e)
        return None
    
    print("Extract image URI.")
    try:
        soup = BeautifulSoup(png_page_response.content, 'html.parser')
        image_uri = soup.find('div', {'id': 'file'}).findChildren('a')[0]['href']
        print("Image URI extracted:", image_uri)
    except Exception as e:
        print("Failed to extract image URI:", e)
        return None

    print("Get image data.")
    try:
        png_data = requests.get(image_uri).content
    except Exception as e:
        print(e)
    
    return png_data


def process_image(png_data, image_name):
    if not png_data:
        print("Invalid png_data.")
        return 0
    filename = os.path.join('pngs', image_name)
    with open(filename, 'wb') as f:
        f.write(png_data)
    print(f"Image: {image_name} downloaded.")
    command = (f"cwebp pngs/{ image_name } -o webps/{ image_name[:-4] }.webp")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Image: {image_name} saved to WEBP.")
    return 1


if __name__ == "__main__":

    start_time = time.time()
    
    total = 0
    for url in pages:
        success_count = get_page(url)
        total += success_count
    
    duration_seconds = time.time() - start_time
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = int(duration_seconds % 60)
    print(f"Job finished. Total {total} PNGs downloaded and converted to WEBP.")
    print(f"Total execution time: {hours:02d}:{minutes:02d}:{seconds:02d}")

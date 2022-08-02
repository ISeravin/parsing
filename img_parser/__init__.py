import os
import re
from urllib import request

FOLDER = "img"


def parse_from(url: str) -> None:
    content = str(request.urlopen(url).read())
    img_urls = re.findall('<img .*?src="(.*?)"', content)
    print(img_urls)
    img_urls = [url + img_url for img_url in img_urls if img_url.find("https://") == -1]
    for img in img_urls:
        download_file(img)


def download_file(file_url: str, dest: str | None = None):
    if not os.path.isdir(FOLDER):
        os.mkdir(FOLDER)
    if not dest:
        dest = FOLDER + "/" + file_url[file_url.rfind("/") + 1 :]
    print(dest)
    print(file_url)

    response = request.urlretrieve(file_url, dest)

    return response

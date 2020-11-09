import requests
import json
from echo_http_test import url
import other
from PIL import ImageFile

# Borrowed from https://stackoverflow.com/questions/7460218/get-image-size-without-downloading-it-in-python
def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = requests.get(uri, stream=True)
    size = file.headers['content-length']
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.raw.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size
            break
    file.close()

    return(None)


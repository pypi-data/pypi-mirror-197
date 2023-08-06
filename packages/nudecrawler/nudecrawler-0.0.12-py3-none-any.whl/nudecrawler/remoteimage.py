import PIL
from PIL import Image

import os
from urllib.parse import urlparse
import tempfile
import sys
import requests

detector_address = 'http://localhost:9191/api/v1/detect'

class RemoteImage:
    def __init__(self, url):        
        self.url = url
        self.path = None
        pr = urlparse(self.url)
        suffix = os.path.splitext(pr.path)[1]
        r = requests.get(url)
        r.raise_for_status()
        self.threshold = 0.5

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            self.path = tmp.name
            tmp.file.write(r.content)

    def set_threshold(self, thr):
        self.threshold = thr

    def __del__(self):
        if self.path:
            os.unlink(self.path)

    def download(self):
        pass

    def detect_nudity(self):

        try:
            img = Image.open(self.path)
        except PIL.UnidentifiedImageError:
            raise ValueError('Incorrect image')
        w, h = img.size


        if w<200 or h<200:
            # boring! maybe icon
            raise ValueError('Image is too small')

        files = {'image': open(self.path,'rb')}
        try:
            r = requests.post(detector_address,files=files)
        except requests.RequestException as e:
            print(e)
            print("maybe detector not running?")
            print("docker run -d -p 9191:9191 opendating/adult-image-detector")
            print("or add -a to skip filtering")
            sys.exit(1)
        
        # return r.json()['an_algorithm_for_nudity_detection']
        return r.json()['open_nsfw_score'] > self.threshold
    


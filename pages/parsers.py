
import hashlib
# import urllib
import datetime
import requests


class BasicPageParser(object):

    def __init__(self):
        pass

    def get_site_comparator(self, site_url):
        """
        Gets the text from the given site url, hashes it, and sites the url and hash together for comparison
        :param site_url:
        :return: comparator: hash
        """
        text = self.get_site_text(site_url)
        digest = self.get_hash(text)
        return digest, str(datetime.datetime.now())

    def get_site_text(self, url):
        r = requests.get(url)
        return str(r.text).encode('utf-8')
        # return urllib.request.urlopen(url).read()

    # def check_site_meta(self, site_text):
    #     # TODO
    #     pass

    def get_hash(self, site_text):
        hash_obj = hashlib.sha256(site_text)
        return hash_obj.hexdigest()


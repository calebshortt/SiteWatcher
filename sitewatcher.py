
import argparse
import time
import settings

from mail.clients import BasicWatcherClient
from persistence.stores import BasicFileStore
from persistence.loaders import SiteFileLoader
from pages.parsers import BasicPageParser


class SiteWatcher(object):

    storage = None
    mailclient = None
    siteloader = None
    parser = None

    def __init__(self, sitesfilepath, email, pw, host=None, port=None):

        self.mailclient = BasicWatcherClient(email, pw, email, host, port)
        self.storage = BasicFileStore(settings.STORE_FILEPATH)
        self.loader = SiteFileLoader(sitesfilepath)
        self.parser = BasicPageParser()

    def start(self):
        while True:
            self.compare()
            time.sleep(86400)

    def compare(self):
        sites = self.loader.load()

        comparators = {}
        for site in sites:
            comparators[site] = self.parser.get_site_comparator(site)

        revised_histories = comparators.copy()

        modified_sites = []
        site_histories = self.storage.load()
        for history in site_histories:
            url = history[0]
            digest = history[1]
            if url in sites:
                # check the hashes
                if digest != comparators[url][0]:
                    modified_sites.append(url)

        self.storage.save(revised_histories)

        if len(modified_sites) > 0:
            msg = 'SiteWatcher has detected a change in some of the sites you monitor:\n\r\n\r'
            for site in modified_sites:
                msg += site + '\n\r'

            self.mailclient.send_mail('Test msg')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'sitesfilepath',
        help='Path to file that contains a list of sites to check (one site per line)')

    parser.add_argument(
        '--mailhost',
        help='The SMTP host you would like to use (e.g. smtp.gmail.com)')

    parser.add_argument(
        '--mailport',
        help='The port you would like to use for your mailhost')

    args = parser.parse_args()

    watcher = SiteWatcher(args.sitesfilepath, settings.EMAIL, settings.APP_PW, args.mailhost, args.mailport)
    watcher.start()

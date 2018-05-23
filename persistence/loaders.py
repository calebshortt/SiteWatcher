

class SiteFileLoader(object):

    filepath = None

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        data = []
        with open(self.filepath, 'r') as f:
            data = f.readlines()
        return [str(item).strip() for item in data]


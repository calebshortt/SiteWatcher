
import csv
from settings import STORE_FILEPATH


class BasicFileStore(object):

    filepath = None

    def __init__(self, filepath=None):
        self.filepath = filepath if filepath else STORE_FILEPATH

    def save(self, data):
        flattened = self.flatten_data(data)
        with open(self.filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in flattened:
                writer.writerow(row)

    def load(self):
        with open(self.filepath, 'r') as f:
            data = list(csv.reader(f))
        constructed = self.construct_data(data)
        return constructed

    def flatten_data(self, data):
        flattened = []
        for key, value in dict(data).items():
            flattened.append((key, ) + value)
        return flattened

    def construct_data(self, data):
        constructed = {}
        for row in list(data):
            constructed[row[0]] = row[1:]
        return constructed


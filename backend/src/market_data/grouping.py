import os
import json

class Grouping:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        self.data = {}
        self.load()

    def load(self):
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w+', encoding="utf-8") as f:
                f.write(f'')
                f.close()
            data = []
        else:
            with open(self.storage_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
                f.close()
            data = data.get('group')

        self.data = data


        
import os
import pickle

class SaveGame:
    def __init__(self, file_path):
       
        self.file_path = os.path.normpath(file_path)

    def save(self, data):
        
        try:
            with open(self.file_path, 'wb') as file:
                pickle.dump(data, file)
        except FileNotFoundError:
            # Create a new file if it doesn't exist
            with open(self.file_path, 'wb') as file:
                pickle.dump(data, file)

    def load(self):
       
        with open(self.file_path, 'rb') as file:
            data = pickle.load(file)
        return data



class SoundConverter:
    tmp_file = None

    def __init__(self, path_to_file):
        self.filename = path_to_file.split('/')[-1]
        self.path = path_to_file.replace(self.filename, '')[0:-1]
        self.format = self.filename.split('.')[-1]

    def convert_to_format(self, format):
        pass

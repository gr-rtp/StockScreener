class Logger():
    def __init__(self, dest):
        self.dest = dest
        self.log_file = None
        pass

    def start(self):
        self.log_file = open(self.dest, "w")
        pass

    def log(self, text: str):
        self.log_file.write(text)
        self.log_file.write('\n')
        pass

    def end(self):
        self.target.close()
        pass
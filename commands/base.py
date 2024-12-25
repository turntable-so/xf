class BaseCommand:
    command: str

    def check_installed(self):
        pass

    def start(self):
        pass

    def run(self, line: str):
        pass

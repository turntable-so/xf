class BaseCommand:
    command: str
    imports: list[str]

    def check_installed(self):
        for import_name in self.imports:
            try:
                __import__(import_name)
            except ImportError:
                return False
        return True

    def start(self):
        pass

    def run(self, line: str):
        pass

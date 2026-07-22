from datetime import datetime

class VersionManager:
    def __init__(self):
        self.version = "1.0.0"
        self.last_updated = datetime.now().strftime("%Y-%m-%d")

    def get_version(self):
        return {
            "version": self.version,
            "last_updated": self.last_updated
        }

    def update_version(self, version):
        self.version = version
        self.last_updated = datetime.now().strftime("%Y-%m-%d")
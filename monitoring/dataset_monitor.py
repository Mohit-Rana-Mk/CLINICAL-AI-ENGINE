import os

class DatasetMonitor:
    def __init__(self, dataset_folder):
        self.dataset_folder = dataset_folder

    def total_files(self):
        if not os.path.exists(self.dataset_folder):
            return 0
        return len(os.listdir(self.dataset_folder))

    def monitor(self):
        return {
            "dataset_folder": self.dataset_folder,
            "total_files": self.total_files()
        }
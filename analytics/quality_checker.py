import os

class QualityChecker:
    def check_missing_files(self, folder_path):
        if not os.path.exists(folder_path):
            return "Folder not found"

        files = os.listdir(folder_path)

        if len(files) == 0:
            return "No files available"

        return f"{len(files)} files found"

    def check_duplicate_files(self, folder_path):
        files = os.listdir(folder_path)
        duplicates = []

        seen = set()

        for file in files:
            if file in seen:
                duplicates.append(file)
            else:
                seen.add(file)

        return duplicates
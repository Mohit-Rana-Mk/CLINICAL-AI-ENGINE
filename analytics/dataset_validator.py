import os
import csv


class DatasetValidator:
    def check_duplicates(self, csv_path):
        if not os.path.exists(csv_path):
            return {"error": "File not found"}

        seen = set()
        duplicates = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                key = tuple(row)
                if key in seen:
                    duplicates.append(row)
                else:
                    seen.add(key)

        return {"duplicate_count": len(duplicates), "duplicates": duplicates}

    def check_missing_fields(self, csv_path):
        if not os.path.exists(csv_path):
            return {"error": "File not found"}

        missing = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for i, row in enumerate(reader, start=2):
                if any(field.strip() == "" for field in row):
                    missing.append({"row": i, "data": row})

        return {"missing_field_count": len(missing), "rows": missing}

    def check_broken_references(self, csv_path, path_column_index):
        if not os.path.exists(csv_path):
            return {"error": "File not found"}

        broken = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for i, row in enumerate(reader, start=2):
                if len(row) > path_column_index:
                    ref_path = row[path_column_index]
                    if ref_path and not os.path.exists(ref_path):
                        broken.append({"row": i, "path": ref_path})

        return {"broken_reference_count": len(broken), "rows": broken}

    def validate_all(self, csv_path, path_column_index=None):
        result = {
            "duplicates": self.check_duplicates(csv_path),
            "missing_fields": self.check_missing_fields(csv_path),
        }
        if path_column_index is not None:
            result["broken_references"] = self.check_broken_references(
                csv_path, path_column_index
            )
        return result

# create a file automation system- organizing files by type, renaming files, deleting duplicates, scheduling clean ups, and generating reports on file usage.
import os
import shutil
import hashlib
from datetime import datetime
from collections import defaultdict
import csv
import schedule
import time


class FileAutomationSystem:
    def __init__(self, base_directory):
        self.base_directory = base_directory

        self.file_types = {
            'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
            'Images': ['.jpg', '.png', '.gif', '.bmp'],
            'Videos': ['.mp4', '.avi', '.mov'],
            'Music': ['.mp3', '.wav', '.aac'],
            'Archives': ['.zip', '.rar', '.tar', '.gz']
        }

        self.report_file = os.path.join(
            self.base_directory, 'file_usage_report.csv'
        )

    # ---------------- ORGANIZE FILES ----------------
    def organize_files(self):
        for file in os.listdir(self.base_directory):
            file_path = os.path.join(self.base_directory, file)

            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()

                for folder, extensions in self.file_types.items():
                    if ext in extensions:
                        target_dir = os.path.join(self.base_directory, folder)
                        os.makedirs(target_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(target_dir, file))
                        break

    # ---------------- RENAME FILES ----------------
    def rename_files(self):
        for root, _, files in os.walk(self.base_directory):
            for file in files:
                if not file.startswith("REN_"):
                    old_path = os.path.join(root, file)
                    new_name = f"REN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file}"
                    new_path = os.path.join(root, new_name)
                    os.rename(old_path, new_path)

    # ---------------- DELETE DUPLICATES ----------------
    def delete_duplicates(self):
        hashes = defaultdict(list)

        for root, _, files in os.walk(self.base_directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_hash = self._hash_file(file_path)
                    hashes[file_hash].append(file_path)
                except:
                    pass

        for file_list in hashes.values():
            for duplicate in file_list[1:]:
                os.remove(duplicate)

    def _hash_file(self, path):
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()

    # ---------------- GENERATE REPORT ----------------
    def generate_report(self):
        with open(self.report_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['File Name', 'Size (Bytes)', 'Last Accessed'])

            for root, _, files in os.walk(self.base_directory):
                for f in files:
                    path = os.path.join(root, f)
                    size = os.path.getsize(path)
                    last_access = datetime.fromtimestamp(
                        os.path.getatime(path)
                    ).strftime('%Y-%m-%d %H:%M:%S')

                    writer.writerow([f, size, last_access])

    # ---------------- SCHEDULE CLEANUP ----------------
    def schedule_cleanup(self, minutes=60):
        schedule.every(minutes).minutes.do(self.organize_files)
        schedule.every(minutes).minutes.do(self.delete_duplicates)

        while True:
            schedule.run_pending()
            time.sleep(1)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    base_dir = r"C:\Users\Asus\OneDrive\Documents\GitHub\test_folder"   # CHANGE THIS

    fas = FileAutomationSystem(base_dir)
    fas.organize_files()
    fas.rename_files()
    fas.delete_duplicates()
    fas.generate_report()

    # Uncomment if scheduling is required
    fas.schedule_cleanup(60)

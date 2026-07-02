class DownloadStatistics:

    def __init__(self):

        self.downloaded = 0
        self.existing = 0
        self.holiday = 0
        self.failed = 0
        self.total = 0

    def increment(self, status):

        self.total += 1

        if status == "DOWNLOADED":
            self.downloaded += 1

        elif status == "EXISTS":
            self.existing += 1

        elif status in ["HOLIDAY", "NOT_FOUND"]:
            self.holiday += 1

        elif status == "FAILED":
            self.failed += 1

    def print_summary(self):

        print("\n")
    
        print("=" * 60)
        print("DOWNLOAD SUMMARY")
        print("=" * 60)
    
        print(f"Downloaded      : {self.downloaded}")
        print(f"Already Exists  : {self.existing}")
        print(f"Holiday         : {self.holiday}")
        print(f"Failed          : {self.failed}")
    
        print("-" * 60)
    
        success = self.downloaded + self.existing
    
        print(f"Successful      : {success}")
    
        print("=" * 60)
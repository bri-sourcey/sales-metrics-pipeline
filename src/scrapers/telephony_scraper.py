from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse
import os
import time
import shutil
import glob


class DialerScraper:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('DIALER_USERNAME')
        self.password = os.getenv('DIALER_PASSWORD')
        self.base_url = os.getenv('DIALER_URL')
        self.download_dir = os.path.expanduser("~/Downloads")
        self.project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.raw_data_dir = os.path.join(self.project_dir, "data", "raw")

    def _init_driver(self, headless=False):
        """Start Chrome browser."""
        options = Options()
        if headless:
            options.add_argument('--headless')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver

    def login(self):
        """Navigate to admin page with credentials."""
        print("Navigating to dialer...")
        parsed = urlparse(self.base_url)
        auth_url = f"https://{self.username}:{self.password}@{parsed.netloc}{parsed.path}"
        self.driver.get(auth_url)
        print("Logged in!")

    def navigate_to_report(self):
        """Navigate to the report page."""
        print("Clicking Reports...")
        reports_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Reports")))
        reports_link.click()

        print("Clicking Fronter - Closer Report...")
        report_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Fronter - Closer Report")))
        report_link.click()

    def download_report(self, date_str: str, metric_type: str):
        """Set date, select dropdown, submit, download."""
        print(f"Setting date to {date_str}...")
        date_field = self.wait.until(EC.presence_of_element_located((By.NAME, "query_date")))
        date_field.clear()
        date_field.send_keys(date_str)

        print(f"Selecting {metric_type} from dropdown...")
        dropdown = Select(self.driver.find_element(By.NAME, "group"))
        dropdown.select_by_visible_text(metric_type)

        print("Clicking Submit...")
        submit_btn = self.driver.find_element(By.NAME, "SUBMIT")
        submit_btn.click()

        print("Clicking Download...")
        time.sleep(2)
        download_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "DOWNLOAD")))
        download_link.click()

        time.sleep(3)
        return self._move_downloaded_file(date_str, metric_type)

    def _move_downloaded_file(self, date_str: str, metric_type: str):
        """Move downloaded file from Downloads to data/raw folder."""
        time.sleep(2)

        pattern = os.path.join(self.download_dir, "FCSTATS_*.csv")
        files = glob.glob(pattern)

        if not files:
            print("WARNING: No downloaded file found!")
            return None

        latest_file = max(files, key=os.path.getctime)

        date_folder = os.path.join(self.raw_data_dir, date_str)
        os.makedirs(date_folder, exist_ok=True)

        new_filename = f"{metric_type}_{date_str}.csv"
        new_path = os.path.join(date_folder, new_filename)
        shutil.move(latest_file, new_path)

        print(f"Saved to {new_path}")
        return new_path

    def run(self, date_str: str = None):
        """Run full extraction for all metrics."""
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        try:
            self._init_driver(headless=False)
            self.login()
            self.navigate_to_report()

            closure_file = self.download_report(date_str, "CloserQueue")

            self.navigate_to_report()
            mail_file = self.download_report(date_str, "MAIL")

            print(f"\nDone! Downloaded:")
            print(f"  - {closure_file}")
            print(f"  - {mail_file}")

        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    scraper = DialerScraper()
    scraper.run()
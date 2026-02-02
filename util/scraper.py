from contextlib import contextmanager
import logging
import os
from io import StringIO

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException

logger = logging.getLogger(__name__)

class TableScraper:
    def __init__(self, url):
        self.url = url
        self.options = self._get_chrome_options()
        self.driver = None

    def _get_chrome_options(self) -> Options:
        options = Options()
        
        # --- Kebutuhan Headless & Server ---
        options.add_argument("--headless=new") # Versi baru lebih stabil & support fitur modern
        options.add_argument("--no-sandbox") # Wajib buat Docker/Linux root
        options.add_argument("--disable-dev-shm-usage") # Cegah crash karena memory /dev/shm penuh
        options.add_argument("--single-process") # Lebih hemat resource di lingkungan terbatas
        
        # --- Bypass Detection (Anti-Bot) ---
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
        options.add_argument('--disable-blink-features=AutomationControlled') # Biar nggak ketahuan kalau ini script
        options.add_argument("--disable-infobars") # Hilangkan bar "Chrome is being controlled..."
        
        # --- Performance Boost ---
        options.add_argument('--disable-gpu') # Standar untuk headless mode
        options.add_argument('--blink-settings=imagesEnabled=false') # Jangan load gambar biar kenceng!
        options.add_argument('--disable-extensions') # Matikan extension biar enteng
        options.add_argument('--remote-debugging-port=9222') # Kadang butuh buat kestabilan headless
        
        # --- Navigasi & Misc ---
        options.add_argument("start-maximized")
        options.add_argument('--disable-browser-side-navigation')
        
        # Binary location jika pakai custom path (misal di server)
        chrome_bin = os.environ.get("GOOGLE_CHROME_BIN")
        if chrome_bin:
            options.binary_location = chrome_bin
            
        return options
    
    @contextmanager
    def _browser_context(self):
        """Context manager untuk handle lifecycle browser."""
        service = None
        driver_path = os.environ.get("CHROME_DRIVER_PATH")
        
        try:
            if driver_path:
                service = Service(driver_path)
            else:
                service = Service(ChromeDriverManager().install())
                
            self.driver = webdriver.Chrome(service=service, options=self.options)
            yield self.driver
        except WebDriverException as e:
            logger.error(f"Gagal inisialisasi browser: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()

    def get_data(self):
        try:
            with self._browser_context() as browser:
                logger.info(f"Scraping URL: {self.url}")
                browser.get(self.url)
                
                html = browser.page_source
                logger.info("Berhasil ambil konten HTML")
                
                tables = pd.read_html(StringIO(html), encoding='utf-8')
                return tables
                
        except TimeoutException:
            logger.error(f"Timeout pas loading: {self.url}")
        except Exception as e:
            logger.error(f"Error scraping tabel dari {self.url}: {str(e)}")
        return None
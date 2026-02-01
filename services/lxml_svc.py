import logging
import json
import pandas as pd
import json
import numpy as np
import requests
from lxml import html

logger = logging.getLogger(__name__)

class LxmlService:
    def __init__(self):
        self.base_uri = 'https://finance.yahoo.com'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Referrer': 'https://google.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36'
        }
        logger.debug("LxmlService initialized")

    def get_page(self, url):
        logger.debug(f"Fetching page content from URL: {url}")
        response = requests.session().get(url, headers=self.headers)
        response.raise_for_status()
        return response

    def parse_rows(self, table_rows):
        logger.debug("Parsing table rows from HTML")
        parsed_rows = []

        for table_row in table_rows:
            parsed_row = []
            el = table_row.xpath("./div")

            none_count = 0

            for rs in el:
                try:
                    (text,) = rs.xpath('.//span/text()[1]')
                    parsed_row.append(text)
                except ValueError:
                    parsed_row.append(np.NaN)
                    none_count += 1

            if none_count < 4:
                parsed_rows.append(parsed_row)
        
        logger.debug(f"Parsed {len(parsed_rows)} rows")
        return pd.DataFrame(parsed_rows)

    def clean_data(self, df):
        logger.debug("Cleaning scraped data")
        df = df.set_index(0)
        df = df.transpose()

        cols = list(df.columns)
        cols[0] = 'Date'
        df = df.set_axis(cols, axis='columns')

        for column_index in range(1, len(df.columns)):
            df.iloc[:, column_index] = df.iloc[:, column_index].str.replace(',', '')
            df.iloc[:, column_index] = df.iloc[:, column_index].astype(np.float64)
        
        logger.debug("Finished cleaning data")
        return df

    def scrape_table(self, url):
        logger.info(f"Scraping table from URL: {url}")
        try:
            page = self.get_page(url)
            tree = html.fromstring(page.content)

            table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
            if not table_rows:
                logger.warning("No table rows found for scraping")
                return pd.DataFrame()

            df = self.parse_rows(table_rows)
            df = self.clean_data(df)
            logger.info(f"Successfully scraped and processed table from {url}")
            return df
        except Exception as e:
            logger.error(f"Failed to scrape table from {url}: {e}", exc_info=True)
            raise

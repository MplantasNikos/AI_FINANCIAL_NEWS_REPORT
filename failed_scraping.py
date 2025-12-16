#Here I tried to scrape sites like the Financial Times, but I failed in every way I tried because their system 
# doesn’t allow it.
#However, I kept the code in case I find a way later.



from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time


def fetch_full_article(url, timeout=25000, headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        try:
            page.goto(url, timeout=timeout)
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            soup = BeautifulSoup(page.content(), "html.parser")

            candidates = soup.find_all(["article", "main", "div"])

            best_text = ""
            best_len = 0

            for block in candidates:
                paragraphs = block.find_all("p")
                text = " ".join(p.get_text(strip=True) for p in paragraphs)

                if len(text) > best_len:
                    best_len = len(text)
                    best_text = text

            browser.close()

            if best_len < 800:
                return None

            return best_text

        except Exception:
            browser.close()
            return None


x = fetch_full_article('https://www.ft.com/content/2c1a2841-fcc2-4ea4-979c-c9b4586320e5')


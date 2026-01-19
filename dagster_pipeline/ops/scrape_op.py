from dagster import op
import subprocess

@op(description="Scrape Telegram medical channels and save raw JSON files")
def scrape_telegram_op():
    subprocess.run(
        ["python", "src/scraping/telegram_scraper.py"],
        check=True
    )

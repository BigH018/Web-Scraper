from playwright.sync_api import sync_playwright
import csv

def scrape_game_data(url, csv_file_name, max_pages=5):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for no UI
        page = browser.new_page()

        # Navigate to the URL
        page.goto(url)

        # Wait for the dropdown to appear
        page.wait_for_selector("div.ant-select-selector")

        # Click the dropdown to open options for 100/page
        page.locator("div.ant-select-selector").click()
        page.wait_for_selector("div[title='100 / page']")
        page.locator("div[title='100 / page']").click()

        # Wait for the "Metrics" dropdown to appear
        page.wait_for_selector("button.ant-btn.css-1xjre7b.ant-btn-default.ant-dropdown-trigger")

        # Open the "Metrics" dropdown
        page.locator("button.ant-btn.css-1xjre7b.ant-btn-default.ant-dropdown-trigger").click()

        # Ensure "Genre" is selected in the metrics
        genre_option = page.locator("li.ant-dropdown-menu-item[title='Genre']")
        if genre_option.get_attribute("aria-checked") != "true":
            genre_option.click()

        # Wait for the page to reload with the selected settings
        page.wait_for_timeout(3000)

        # Open CSV file to write
        with open(csv_file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Updated header row
            writer.writerow([
                "Production Company", "Game Name", "Game Link", "Genre", "Visits", 
                "Active Players", "Est Avg Session Time", "Favorites", "Created"
            ])

            # Iterate through pages
            for current_page in range(1, max_pages + 1):
                print(f"Scraping page {current_page}...")

                # Ensure page is fully rendered
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_selector("tbody.ant-table-tbody")
                page.wait_for_timeout(2000)

                # Updated rows selector
                rows = page.locator("tbody.ant-table-tbody > tr:not([aria-hidden='true'])").all()

                print(f"Number of rows found: {len(rows)}")

                for index, row in enumerate(rows):
                    print(f"Processing row {index + 1}/{len(rows)}...")

                    try:
                        production_company = row.locator(
                            "a.ant-typography.ant-typography-secondary.css-1xjre7b"
                        ).inner_text(timeout=5000).strip()
                    except Exception:
                        production_company = "N/A"

                    try:
                        game_name_element = row.locator(
                            "a.ant-typography.css-1xjre7b[style='font-size: 14px;']"
                        )
                        game_name = game_name_element.inner_text(timeout=5000).strip()
                        game_link = game_name_element.get_attribute("href")
                        if game_link and game_link.startswith("/experience"):
                            game_link = f"https://www.roblox.com{game_link}"
                    except Exception:
                        game_name = "N/A"
                        game_link = "N/A"

                    try:
                        genre = row.locator(
                            "span.ant-typography.css-1xjre7b[style*='min-width: 60px']"
                        ).inner_text(timeout=5000).strip()
                    except Exception:
                        genre = "N/A"

                    try:
                        visits = row.locator(
                            "span.ant-typography.css-1xjre7b[style*='min-width: 68px'] > span"
                        ).inner_text(timeout=5000).strip()
                    except Exception:
                        visits = "N/A"

                    try:
                        avg_ccu = row.locator(
                            "span.ant-typography.css-1xjre7b[style*='min-width: 76px']"
                        ).nth(0).inner_text(timeout=5000).strip()
                    except Exception:
                        avg_ccu = "N/A"

                    try:
                        avg_session_time = row.locator(
                            "span.ant-typography.css-1xjre7b[style*='min-width: 76px']"
                        ).nth(1).inner_text(timeout=5000).strip()
                    except Exception:
                        avg_session_time = "N/A"

                    try:
                        favorites = row.locator(
                            "span.ant-typography.css-1xjre7b[style*='min-width: 92px']"
                        ).inner_text(timeout=5000).strip()
                    except Exception:
                        favorites = "N/A"

                    try:
                        created_date = row.locator(
                            "span.ant-typography.css-1xjre7b[style*='min-width: 76px']"
                        ).nth(2).inner_text(timeout=5000).strip()
                    except Exception:
                        created_date = "N/A"

                    # Log extracted fields
                    print(f"Row {index + 1} Data: {production_company}, {game_name}, {game_link}, {genre}, {visits}, {avg_ccu}, {avg_session_time}, {favorites}, {created_date}")

                    # Write to CSV
                    writer.writerow([
                        production_company, game_name, game_link, genre, visits,
                        avg_ccu, avg_session_time, favorites, created_date
                    ])
                    file.flush()

                # Updated next page button selector
                next_button = page.locator("li.ant-pagination-next button.ant-pagination-item-link")
                if next_button.get_attribute("aria-disabled") == "true":
                    print("Reached the last page.")
                    break
                next_button.click()
                # Wait for the next page to load
                page.wait_for_timeout(3000)

        print(f"Scraping completed! Data saved to {csv_file_name}")
        browser.close()

if __name__ == "__main__":
    WEBSITE_URL = "https://search.superbiz.gg/"
    CSV_FILE_NAME = "game_data.csv"

    scrape_game_data(WEBSITE_URL, CSV_FILE_NAME, max_pages=1)
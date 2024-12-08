# Game Data Scraper

This project is a web scraping tool that extracts data from [SuperBiz](https://search.superbiz.gg/) using Python and Playwright. The tool collects information about games, such as production company, game name, genre, visits, active players, and more, saving the data into a CSV file for further analysis.

## Features

- Scrapes game data, including:
  - Production Company
  - Game Name and Link
  - Genre
  - Visits
  - Active Players
  - Estimated Average Session Time
  - Favorites
  - Creation Date
- Supports pagination to scrape multiple pages.
- Saves data into a structured CSV file.

## Usage

# Open the script and configure the following settings if necessary:
# WEBSITE_URL = "https://search.superbiz.gg/"
# CSV_FILE_NAME = "game_data.csv"

# Run the script to start scraping:
python scraper.py

# The scraped data will be saved in the specified CSV file (game_data.csv by default).

## Customization

- **Pagination:** 
  Adjust the `max_pages` parameter in the `scrape_game_data` function call to scrape more pages.
  
- **Headless Mode:** 
  By default, the browser runs in non-headless mode for debugging. Change `headless=False` to `headless=True` in the `browser = p.chromium.launch()` line to run in the background.

## Troubleshooting

- Ensure the webpage structure hasn't changed if the scraper stops working.
- Make sure the required selectors in the script match the webpage's DOM.

## Contributing

Feel free to fork this repository, make changes, and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

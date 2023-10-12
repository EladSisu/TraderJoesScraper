# Trader Joe's Product Scraper

This project scrapes product data from Trader Joe's API and generates a CSV file with detailed nutritional information about each product.

## Features

- Fetches all current day's product data from Trader Joe's API.
- Generates a CSV file with the following columns for each product:
  - Name
  - Price
  - Calories
  - Total Fat
  - Saturated Fat
  - Trans Fat
  - Cholesterol
  - Sodium
  - Total Carbohydrate
  - Dietary Fiber
  - Total Sugars
  - Protein
  - Vitamin D
  - Calcium
  - Iron
  - Potassium

## Requirements

- Python 3.x
- Required Python libraries are mentioned in `requirements.txt`.

## Setup & Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/EladSisu/trader-joes-product-scraper.git
   cd trader-joes-product-scraper
   ```

2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the scraper:

   ```bash
   python main.py
   ```

4. After execution, you'll find a CSV file named `tj_products_{current_date}.csv` in the project directory.

## Contribution

Feel free to fork this repository, make changes, and submit pull requests. Feedback is always welcome.

## License

MIT License. See [LICENSE](LICENSE) for more details.

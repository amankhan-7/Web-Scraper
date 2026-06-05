# Blinkit Product Scraper

A Playwright-based Blinkit scraper that extracts category information, scrapes product listings, cleans and normalizes product data, and stores the results in a Neon PostgreSQL database.

## Features

* Extracts Blinkit feed data
* Parses and resolves category URLs
* Scrapes products from category pages
* Handles dynamic loading and scrolling
* Removes duplicate products
* Normalizes product attributes
* Stores data in Neon PostgreSQL
* Category-to-product mapping support
* Location-aware scraping (optional)
* JSON export for raw, extracted, and cleaned datasets

---

## Project Structure

```text
project/
│
├── data/
│   ├── raw/
│   │   └── <category>/
│   │       └── products.json
│   │
│   ├── extracted/
│   │   └── extracted_products.json
│   │
│   ├── cleaned/
│   │   └── cleaned_products.json
│   │
│   ├── feed.json
│   └── clean_feed.json
│
├── scraper/
│   ├── categories.py
│   ├── extractor.py
│   ├── visibility.py
│   ├── cleaner.py
│   └── database.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Data Pipeline

### 1. Feed Extraction

The scraper captures Blinkit feed requests:

```text
https://blinkit.com/feed/?template_version=9
```

The response is saved as:

```text
data/feed.json
data/clean_feed.json
```

---

### 2. Category Resolution

Categories are extracted from the feed and converted into valid Blinkit category URLs.

Example:

```text
https://blinkit.com/cn/full-cream-milk/cid/14/922
```

Stored metadata:

```json
{
  "parent_category": "cn",
  "category": "full-cream-milk",
  "l0_cat": "14",
  "l1_cat": "922",
  "category_path": "14/922"
}
```

---

### 3. Product Scraping

For each category:

* Opens category page
* Captures API responses
* Scrolls through listings
* Collects products
* Removes duplicates
* Saves raw category data

Output:

```text
data/raw/<category>/products.json
```

---

### 4. Product Extraction

The extractor:

* Reads all category files
* Supports multiple Blinkit response formats
* Normalizes product fields
* Removes duplicates globally

Extracted fields:

```json
{
  "product_id": 482995,
  "merchant_id": 31719,
  "category": "chewing-gum",
  "parent_category": "cn",
  "name": "Orbit Spearmint Flavour Sugar Free Chewing Gum",
  "brand": "Orbit",
  "price": 15.0,
  "inventory": 8,
  "rating": 4.69,
  "image_url": "...",
  "in_stock": true,
  "city": null,
  "state": null,
  "latitude": 27.1606595,
  "longitude": 77.9874933
}
```

Output:

```text
data/extracted/extracted_products.json
```

---

### 5. Data Cleaning

The cleaning stage:

* Removes invalid products
* Normalizes data types
* Handles missing values
* Standardizes fields

Output:

```text
data/cleaned/cleaned_products.json
```

---

### 6. Database Storage

The cleaned dataset is inserted into Neon PostgreSQL.

Tables:

### categories

```sql
id
category
parent_category
```

### blinkit_products

```sql
product_id
merchant_id
name
brand
price
inventory
rating
image_url
category_id
latitude
longitude
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd blinkit-scraper
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright

```bash
playwright install
```

---

## Environment Variables

Create a `.env` file:

```env
LATITUDE=27.1606595
LONGITUDE=77.9874933

NEON_HOST=your_host
NEON_DATABASE=your_database
NEON_USER=your_user
NEON_PASSWORD=your_password
```

---

## Run

```bash
python main.py
```

---

## Example Output

```text
Loaded 18 categories
Saved extracted data (529 products)
Saved cleaned data (529 products)
Saved 529 products to Neon DB
```

---

## Current Improvements

### Completed

* Feed interception
* Category extraction
* Product scraping
* Deduplication
* Cleaning pipeline
* Neon integration

### Planned

* Better pagination detection
* Improved price extraction
* Visibility endpoint fallback handling
* Incremental scraping
* Product change tracking
* Historical price monitoring

---

## Tech Stack

* Python 3.12
* Playwright
* Requests
* PostgreSQL
* Neon Database
* JSON Processing

---

## Disclaimer

This project is intended for educational and research purposes only. Respect Blinkit's Terms of Service and applicable laws when scraping data.

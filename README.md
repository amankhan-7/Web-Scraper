# 🛒 Blinkit Product Scraper

A Python-based web scraping project that extracts **Blinkit product data** for a specific **latitude and longitude**, cleans and structures the data, and stores it in a **PostgreSQL/Neon database** for further analytics.

The long-term goal of this project is to enable **location-based product intelligence**, including:

- 📈 Product trend analysis by location
- 📦 Inventory analysis
- 🗺️ Geo-based demand insights
- 🏪 Regional product availability tracking
- 💰 Pricing analysis across locations

---

# 🚀 Features

- Scrapes **Blinkit product catalog**
- Fetches products based on **latitude & longitude**
- Extracts product metadata from raw feed
- Cleans and standardizes product data
- Stores data in **Neon PostgreSQL**
- Creates and maps **categories table**
- Maintains **category foreign key relationships**
- Saves intermediate JSON files for debugging and processing

---

# 📂 Project Structure

```txt
WebScraping/
├── config/
│   └── settings.py

├── data/
│   ├── raw/
│   ├── extracted/
│   └── cleaned/

├── db/
│   ├── neon.py
│   ├── schema.sql
│   └── supabase.py

├── layout/
│   ├── clean_utils.py
│   ├── feed_extractor.py
│   ├── fill_categories.py
│   └── fill_categories_slug.py

├── scraper/
│   ├── categories.py
│   ├── cleaner.py
│   ├── extractor.py
│   ├── products.py
│   └── visibility.py

├── utils/
│   ├── headers.py
│   └── loggers.py

├── insertdb.py
├── main.py
├── requirements.txt
└── .env
```

---

# ⚙️ Data Pipeline

The scraper follows this workflow:

```txt
Feed Extraction
        ↓
Category Scraping
        ↓
Raw Product Collection
        ↓
Product Extraction
        ↓
Data Cleaning
        ↓
Category Table Creation
        ↓
Category FK Mapping
        ↓
Store in Neon/PostgreSQL
```

---

# 🗄️ Database Design

## Categories Table

```sql
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,

    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,

    url TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);
```

## Blinkit Products Table

```sql
CREATE TABLE blinkit_products (
    id BIGSERIAL PRIMARY KEY,

    product_id BIGINT UNIQUE NOT NULL,
    merchant_id BIGINT,

    category_id BIGINT
    REFERENCES categories(id),

    name TEXT NOT NULL,
    brand TEXT,

    price NUMERIC(10,2),
    inventory INT,

    rating FLOAT,

    image_url TEXT,

    in_stock BOOLEAN DEFAULT TRUE,

    city TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    scraped_at TIMESTAMP DEFAULT NOW(),

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

# 📦 Example Extracted Product

```json
{
  "product_id": 364457,
  "merchant_id": 31719,
  "category": "sharbat",
  "parent_category": "cn",
  "ptype": "",
  "name": "Rasna Fruit Fun Nagpur Orange Drink Mix (32 Glasses)",
  "brand": "Rasna Fruit Fun",
  "price": 50.0,
  "inventory": 12,
  "rating": 4.329999923706055,
  "image_url": "https://cdn.grofers.com/product.png",
  "in_stock": true,
  "city": "Agra",
  "latitude": 27.1606595,
  "longitude": 77.9874933
}
```

---

# 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=your_neon_database_url

LATITUDE=27.1606595
LONGITUDE=77.9874933

CITY=Agra
```

---

# 📥 Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd WebScraping
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Run the scraper:

```bash
python main.py
```

The pipeline automatically:

1. Fetches Blinkit feed
2. Scrapes categories
3. Extracts raw products
4. Cleans product data
5. Creates category records
6. Maps `category_id`
7. Inserts products into PostgreSQL

---

# 📁 Data Storage

Temporary scraped data is stored inside:

```txt
data/
```

This folder is ignored from Git to avoid pushing scraped JSON files.

---

# 🔮 Future Scope

This project can be extended to support:

### 1. Product Trend Analysis
Track how products perform across locations over time.

### 2. Inventory Intelligence
Identify products with:

- Frequent stockouts
- High availability
- Seasonal demand

### 3. Geo-Based Analytics
Compare:

- Product pricing
- Availability
- Inventory levels

Across different latitudes and longitudes.

### 4. Demand Forecasting
Use historical data to predict:

- High-demand products
- Inventory shortages
- Region-specific preferences

### 5. Real-Time Monitoring
Schedule scraping jobs for:

- Hourly tracking
- Daily trend analysis
- Live inventory monitoring

---

# 🛠️ Tech Stack

- **Python**
- **PostgreSQL**
- **Neon DB**
- **psycopg2**
- **JSON Processing**
- **REST APIs**
- **Environment Variables (.env)**

---

# 📜 License

This project is intended for **educational and research purposes**.

Please ensure compliance with Blinkit's Terms of Service before using at scale.

---

## 👨‍💻 Author

Built with Python for location-based product intelligence and analytics.

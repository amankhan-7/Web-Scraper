

CREATE TABLE blinkit_products (
    id BIGSERIAL PRIMARY KEY,

    product_id BIGINT UNIQUE NOT NULL,
    merchant_id BIGINT,

    name TEXT NOT NULL,
    brand TEXT,

    category_id BIGINT REFERENCES product_categories(id),

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

CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT
);

CREATE TABLE product_categories (
    product_id BIGINT REFERENCES blinkit_products(product_id),
    category_id BIGINT REFERENCES categories(id),
    PRIMARY KEY (product_id, category_id)
);
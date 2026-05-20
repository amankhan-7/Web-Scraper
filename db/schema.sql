

CREATE TABLE blinkit_products (
    id BIGSERIAL PRIMARY KEY,

    product_id BIGINT UNIQUE NOT NULL,
    merchant_id BIGINT,

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
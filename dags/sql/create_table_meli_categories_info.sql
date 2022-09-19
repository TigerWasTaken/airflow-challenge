CREATE TABLE IF NOT EXISTS meli_categories_info (
    id VARCHAR(255) NOT NULL,
    site_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    sold_quantity INT NOT NULL,
    thumbnail VARCHAR(255) NOT NULL,
    total_earnings FLOAT NOT NULL,
    created_date TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);
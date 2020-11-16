CREATE TABLE IF NOT EXISTS Category(
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Products(
    code VARCHAR(13) NOT NULL,
    product_category SMALLINT UNSIGNED NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    nutrition_score CHAR(1) NOT NULL,
    nova_score TINYINT UNSIGNED NOT NULL,
    store_name VARCHAR(100),
    PRIMARY KEY(code),
    CONSTRAINT fk_cateogry
        FOREIGN KEY (product_category)
        REFERENCES Category(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Favorite_products(
    code VARCHAR(13) NOT NULL,
    substitute_code VARCHAR(13) NOT NULL,
    PRIMARY KEY(code),
    CONSTRAINT fk_code1
        FOREIGN KEY (code)
        REFERENCES Products(code)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_code2
        FOREIGN KEY (substitute_code)
        REFERENCES Products(code)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE = InnoDB;
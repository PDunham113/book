CREATE TABLE `account` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(6) DEFAULT NOW(6),
    `updated_at` DATETIME(6) DEFAULT NOW(6),
    `name` VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `category` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(6) DEFAULT NOW(6),
    `updated_at` DATETIME(6) DEFAULT NOW(6),
    `name` VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `currency` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(6) DEFAULT NOW(6),
    `updated_at` DATETIME(6) DEFAULT NOW(6),
    `name` VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `transaction` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(6) DEFAULT NOW(6),
    `updated_at` DATETIME(6) DEFAULT NOW(6),
    `date_start` DATETIME NOT NULL,
    `date_end` DATETIME NOT NULL,
    `category_id` INT UNSIGNED,
    `notes` TEXT,
    CONSTRAINT `fk_transaction_category_id`
        FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
    PRIMARY KEY (`id`)
);

CREATE TABLE `transaction_stub` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(6) DEFAULT NOW(6),
    `updated_at` DATETIME(6) DEFAULT NOW(6),
    `txn_id` INT UNSIGNED NOT NULL,
    `acct_id` INT UNSIGNED NOT NULL,
    `amount` DECIMAL(13, 4) NOT NULL,
    `currency_id` INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_transaction_stub_txn_id`
        FOREIGN KEY (`txn_id`) REFERENCES `transaction` (`id`),
    CONSTRAINT `fk_transaction_stub_acct_id`
        FOREIGN KEY (`acct_id`) REFERENCES `account` (`id`),
    CONSTRAINT `fk_transaction_stub_currency_id`
        FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`),
    PRIMARY KEY (`id`)
);

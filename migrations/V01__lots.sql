CREATE TABLE `lot` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `created_at` DATETIME(6) DEFAULT NOW(6),
    `updated_at` DATETIME(6) DEFAULT NOW(6),
    `date` DATETIME,
    `currency_id` INT UNSIGNED NOT NULL,
    `purchase_currency_id` INT UNSIGNED NOT NULL,
    `purchase_amount` DECIMAL(13, 4) NOT NULL,
    UNIQUE KEY `uk_lot`  (`date`, `currency_id`, `purchase_currency_id`, `purchase_amount`),
    FOREIGN KEY `fk_currency_id` (`currency_id`) REFERENCES `currency`(`id`),
    FOREIGN KEY `fk_purchase_currency_id` (`purchase_currency_id`) REFERENCES `currency`(`id`),
    PRIMARY KEY (`id`)
);

# If I had any entered transactions, I should transform them to lots here

ALTER TABLE `transaction_stub`
    ADD COLUMN `lot_id` INT UNSIGNED NOT NULL AFTER `amount`,
    ADD COLUMN `purchase_amt` DECIMAL(13, 4) NOT NULL,
    ADD FOREIGN KEY `fk_lot_id` (`lot_id`) REFERENCES `lot`(`id`);

ALTER TABLE `transaction_stub`
    RENAME COLUMN `currency_id` TO `purchase_currency_id`;

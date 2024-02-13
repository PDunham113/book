ALTER TABLE `transaction_stub`
    RENAME COLUMN `purchase_currency_id` TO `currency_id`;


ALTER TABLE `transaction_stub`
    DROP FOREIGN KEY `fk_lot_id`,
    DROP COLUMN `purchase_amt`,
    DROP COLUMN `lot_id`;

DROP TABLE IF EXISTS `lot`;

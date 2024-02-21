ALTER TABLE `transaction_stub`
    RENAME COLUMN `purchase_currency_id` TO `currency_id`;


ALTER TABLE `transaction_stub`
    DROP FOREIGN KEY `fk_transaction_stub_lot_id`,
    DROP INDEX `fk_transaction_stub_lot_id`,
    DROP COLUMN `purchase_amt`,
    DROP COLUMN `lot_id`;

DROP TABLE IF EXISTS `lot`;

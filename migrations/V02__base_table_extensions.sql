ALTER TABLE `account`
    ADD COLUMN `opened_at` DATETIME,
    ADD COLUMN `closed_at` DATETIME;

RENAME TABLE `category` TO `group`;

CREATE TABLE `transactions_groups` (
    `created_at` DATETIME(6) DEFAULT NOW(6),
    `updated_at` DATETIME(6) DEFAULT NOW(6),
    `txn_id` INT UNSIGNED NOT NULL,
    `group_id` INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_txn_id` FOREIGN KEY (`txn_id`) REFERENCES `transaction` (`id`),
    CONSTRAINT `fk_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`),
    PRIMARY KEY (`txn_id`, `group_id`)
);

INSERT INTO `transactions_groups` (`txn_id`, `group_id`)
    SELECT `t`.`id`, `t`.`category_id` FROM `transaction` AS `t`;

ALTER TABLE `transaction`
    DROP FOREIGN KEY `fk_transaction_category_id`,
    DROP INDEX `fk_transaction_category_id`,
    DROP COLUMN `category_id`;

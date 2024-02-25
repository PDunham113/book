ALTER TABLE `transaction`
    ADD COLUMN `category_id` INT UNSIGNED,
    ADD CONSTRAINT `fk_transaction_category_id`
        FOREIGN KEY (`category_id`) REFERENCES `group` (`id`);

# WARN: This is inherently destructive, as we're mapping from many->many to one->one
# We choose the first relationship by time, as it will be what was originally in category_id, if any
UPDATE `transaction` AS `t`
    LEFT JOIN (
        SELECT `txn_id`, `group_id` FROM `transactions_groups`
        WHERE `created_at` IN (
            SELECT MIN(`created_at`) FROM `transactions_groups` GROUP BY `txn_id`
        )
    ) AS `tmp` ON `t`.`id` = `tmp`.`txn_id`
    SET `t`.`category_id` = `tmp`.`group_id`;

DROP TABLE `transactions_groups`;

RENAME TABLE `group` TO `category`;

ALTER TABLE `account`
    DROP COLUMN `opened_at`,
    DROP COLUMN `closed_at`;

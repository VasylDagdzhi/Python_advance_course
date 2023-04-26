CREATE TABLE `files` (
	`id` INT(32) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL,
	`directory_id` INT(32) NOT NULL,
	`size` INT(64) NOT NULL,
	`content` blob NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `directories` (
	`id` INT(32) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) NOT NULL AUTO_INCREMENT,
	`parent_id` INT(32) NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `files` ADD CONSTRAINT `files_fk0` FOREIGN KEY (`directory_id`) REFERENCES `directories`(`id`);

ALTER TABLE `directories` ADD CONSTRAINT `directories_fk0` FOREIGN KEY (`parent_id`) REFERENCES `directories`(`id`);




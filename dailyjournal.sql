CREATE TABLE `Mood` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);

CREATE TABLE `Entry` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `date` TEXT NOT NULL,
    `mood_id` INT,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

INSERT INTO `Mood` VALUES (null,"Apathetic");
INSERT INTO `Mood` VALUES (null, "Ecstatic");
INSERT INTO `Mood` VALUES (null,"Bored");
INSERT INTO `Mood` VALUES (null,"Apprehensive");

INSERT INTO `Entry` VALUES (null, "SQL", "I am learning the basics of SQL queries", "Wed April 13 2022 15:33:00", 4);
INSERT INTO `Entry` VALUES (null, "Python", "I am learning how to delete entries", "Wed April 15 2022 15:33:00", 1);

SELECT * FROM Entry

CREATE TABLE `Tag` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL
);

CREATE TABLE `EntryTag` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER,
    `tag_id` INTEGER,
    FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`)
);

INSERT INTO `Tag` VALUES (null, "tag1")
INSERT INTO `Tag` VALUES (null, "tag2")
INSERT INTO `Tag` VALUES (null, "tag3")

SELECT * FROM 
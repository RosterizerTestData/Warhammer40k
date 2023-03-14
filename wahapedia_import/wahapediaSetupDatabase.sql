START TRANSACTION;

DROP TABLE IF EXISTS datasheets_wargear;
DROP TABLE IF EXISTS datasheets_options;
DROP TABLE IF EXISTS datasheets_models;
DROP TABLE IF EXISTS datasheets_keywords;
DROP TABLE IF EXISTS datasheets_damage;
DROP TABLE IF EXISTS strategems;
DROP TABLE IF EXISTS warlord_traits;
DROP TABLE IF EXISTS psychic_powers;
DROP TABLE IF EXISTS datasheets_abilities;
DROP TABLE IF EXISTS abilities;
DROP TABLE IF EXISTS datasheets;
DROP TABLE IF EXISTS wargear_list;
DROP TABLE IF EXISTS wargear;
DROP TABLE IF EXISTS factions;
DROP TABLE IF EXISTS sources;

ALTER DATABASE wahapedia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "sources";
CREATE TABLE sources (
  source_id INT PRIMARY KEY,
  name VARCHAR(255),
  type VARCHAR(255),
  edition INT,
  version VARCHAR(255),
  errata_date VARCHAR(255),
  errata_link VARCHAR(255),
  check_me INT DEFAULT 0 /*boolean*/
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "factions";
CREATE TABLE factions (
  faction_id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255),
  link VARCHAR(255),
  is_subfaction VARCHAR(255),
  main_faction_id VARCHAR(255),
  check_me INT DEFAULT 0 /*boolean*/
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "wargear";
CREATE TABLE wargear (
  wargear_id INT PRIMARY KEY,
  name VARCHAR(255),
  type VARCHAR(255),
  description TEXT,
  is_relic INT, /*boolean*/
  faction_id VARCHAR(255),
  legend TEXT,
  check_me INT DEFAULT 0, /*boolean*/
  CONSTRAINT wargear_fk_factions FOREIGN KEY (faction_id) REFERENCES factions (faction_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "wargear_list";
CREATE TABLE wargear_list (
  wargear_id INT,
  line  INT,
  name VARCHAR(255),
  weapon_range VARCHAR(255),
  type VARCHAR(255),
  strength VARCHAR(255),
  armor_piercing VARCHAR(255),
  damage VARCHAR(255),
  abilities TEXT,
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (wargear_id, line),
  CONSTRAINT wargear_list_fk_wargear FOREIGN KEY (wargear_id) REFERENCES wargear (wargear_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "datasheets";
CREATE TABLE datasheets (
  datasheet_id INT PRIMARY KEY,
  name VARCHAR(255),
  link VARCHAR(255),
  faction_id VARCHAR(255),
  source_id INT,
  role VARCHAR(255),
  unit_composition TEXT,
  transport TEXT,
  power_points VARCHAR(255),
  priest TEXT,
  psyker TEXT,
  open_play_only INT, /*boolean*/
  crusade_only INT, /*boolean*/
  virtual_ INT, /*boolean*/
  cost INT,
  cost_per_unit INT, /*boolean*/
  check_me INT DEFAULT 0, /*boolean*/
  CONSTRAINT datasheets_fk_factions FOREIGN KEY (faction_id) REFERENCES factions (faction_id),
  CONSTRAINT datasheets_fk_sources FOREIGN KEY (source_id) REFERENCES sources (source_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "abilities";
CREATE TABLE abilities (
  ability_id INT PRIMARY KEY,
  type VARCHAR(255),
  name VARCHAR(255),
  legend TEXT,
  is_other_wargear INT, /*boolean*/
  faction_id VARCHAR(255),
  description TEXT,
  check_me INT DEFAULT 0, /*boolean*/
  CONSTRAINT abilities_fk_factions FOREIGN KEY (faction_id) REFERENCES factions (faction_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "datasheets_abilities";
CREATE TABLE datasheets_abilities (
  datasheet_id INT,
  line INT,
  ability_id INT,
  is_index_wargear INT, /*boolean*/
  cost INT,
  model VARCHAR(255),
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (datasheet_id, line),
  CONSTRAINT datasheets_abilities_fk_datasheets FOREIGN KEY (datasheet_id) REFERENCES datasheets (datasheet_id),
  CONSTRAINT datasheets_abilities_fk_abilities FOREIGN KEY (ability_id) REFERENCES abilities (ability_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "psychic_powers";
CREATE TABLE psychic_powers (
  psychic_power_id INT,
  roll INT,
  name VARCHAR(255),
  faction_id VARCHAR(255),
  legend TEXT,
  type VARCHAR(255),
  description TEXT,
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (psychic_power_id, roll),
  CONSTRAINT psychic_powers_fk_factions FOREIGN KEY (faction_id) REFERENCES factions (faction_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "warlord_traits";
CREATE TABLE warlord_traits (
  trait_id INT PRIMARY KEY AUTO_INCREMENT,
  faction_id VARCHAR(255),
  type VARCHAR(255),
  roll VARCHAR(255),
  name VARCHAR(255),
  legend TEXT,
  description TEXT,
  check_me INT DEFAULT 0, /*boolean*/
  CONSTRAINT warlord_traits_fk_factions FOREIGN KEY (faction_id) REFERENCES factions (faction_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "strategems";
CREATE TABLE strategems (
  strategem_id INT PRIMARY KEY,
  faction_id VARCHAR(255),
  subfaction_id VARCHAR(255),
  name VARCHAR(255),
  type VARCHAR(255),
  cp_cost VARCHAR(255),
  legend TEXT,
  source_id INT,
  description TEXT,
  check_me INT DEFAULT 0 /*boolean*/
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "datasheets_damage";
CREATE TABLE datasheets_damage (
  datasheet_id INT,
  line INT,
  col1 VARCHAR(255),
  col2 VARCHAR(255),
  col3 VARCHAR(255),
  col4 VARCHAR(255),
  col5 VARCHAR(255),
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (datasheet_id, line),
  CONSTRAINT datasheets_damage_fk_datasheets FOREIGN KEY (datasheet_id) REFERENCES datasheets (datasheet_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "datasheets_keywords";
CREATE TABLE datasheets_keywords (
  datasheet_id INT,
  keyword VARCHAR(255),
  model VARCHAR(255),
  is_faction_keyword INT, /*boolean*/
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (datasheet_id, keyword),
  CONSTRAINT datasheets_keywords_fk_datasheets FOREIGN KEY (datasheet_id) REFERENCES datasheets (datasheet_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "datasheets_models";
CREATE TABLE datasheets_models (
  datasheet_id INT,
  line INT,
  name VARCHAR(255),
  movement VARCHAR(255),
  weapon_skill INT,
  ballistic_skill INT,
  strength INT,
  toughness INT,
  wounds INT,
  attacks VARCHAR(255),
  leadership INT,
  save INT,
  cost INT,
  cost_description TEXT,
  models_per_unit VARCHAR(255),
  cost_including_wargear INT, /*boolean*/
  base_size VARCHAR(255),
  base_size_descr VARCHAR(255),
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (datasheet_id, line),
  CONSTRAINT datasheets_models_fk_datasheets FOREIGN KEY (datasheet_id) REFERENCES datasheets (datasheet_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "datasheets_options";
CREATE TABLE datasheets_options (
  datasheet_id INT,
  line INT,
  button VARCHAR(255),
  description TEXT,
  is_index_wargear INT, /*boolean*/
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (datasheet_id, line),
  CONSTRAINT datasheets_options_fk_datasheets FOREIGN KEY (datasheet_id) REFERENCES datasheets (datasheet_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT "datasheets_wargear";
CREATE TABLE datasheets_wargear (
  datasheet_id INT,
  line INT,
  wargear_id INT,
  cost INT,
  is_index_wargear INT, /*boolean*/
  model VARCHAR(255),
  is_upgrade INT, /*boolean*/
  check_me INT DEFAULT 0, /*boolean*/
  PRIMARY KEY (datasheet_id, line, is_upgrade),
  CONSTRAINT datasheets_wargear_fk_datasheets FOREIGN KEY (datasheet_id) REFERENCES datasheets (datasheet_id),
  CONSTRAINT datasheets_wargear_fk_wargear FOREIGN KEY (wargear_id) REFERENCES wargear (wargear_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

COMMIT;
	-- 1. 建立名為eduu的，可包含中文的 schema
-- CREATE DATABASE eduu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- SHOW TABLES;
-- SHOW COLUMNS FROM snake_species
-- DESCRIBE snake_species;
-- ALTER TABLE snake_species
-- ADD COLUMN species_id INT AUTO_INCREMENT PRIMARY KEY;
-- SELECT * FROM snake_species;

-- DESCRIBE product;
-- ALTER TABLE product
-- ADD COLUMN product_id INT AUTO_INCREMENT PRIMARY KEY;
-- ALTER TABLE product
-- ADD CONSTRAINT fk_species
-- FOREIGN KEY (species_id) REFERENCES snake_species(species_id);
 SELECT * FROM product;

-- DESCRIBE care_requirements;
-- ALTER TABLE care_requirements
-- ADD COLUMN care_id INT AUTO_INCREMENT PRIMARY KEY;
-- ALTER TABLE care_requirements
-- ADD CONSTRAINT fk_species_care
-- FOREIGN KEY (species_id) REFERENCES snake_species(species_id);
-- SELECT * FROM care_requirements;

DROP PROCEDURE IF EXISTS industry__get;
DROP PROCEDURE IF EXISTS company__get;
DROP PROCEDURE IF EXISTS pub__get;
DROP PROCEDURE IF EXISTS pub__create;
DROP PROCEDURE IF EXISTS article__create;

-- set delimiter
DELIMITER //

-- create sprocs

CREATE PROCEDURE industry__get()
    SELECT 
        id,
        name
    FROM industry ORDER BY name;
//

CREATE PROCEDURE company__get()
    SELECT 
        id,
        name
    FROM company ORDER BY name;
//

CREATE PROCEDURE pub__get()
    SELECT 
        id,
        name
    FROM pub ORDER BY name;
//

CREATE PROCEDURE pub__create(
    p_name VARCHAR(100))
    BEGIN
        INSERT INTO pub (name) 
        VALUES(p_name);
        SELECT LAST_INSERT_ID();  
    END 
//


CREATE PROCEDURE article__create(
    p_company_id INT,
    p_pub_id INT,
    p_published  DATE,
    p_author VARCHAR(100), 
    p_headline VARCHAR(500),
    p_body LONGTEXT) 
    BEGIN
        INSERT INTO article (company_id, pub_id, published, author, headline, body)
        VALUES (p_company_id, p_pub_id, p_published, p_author, p_headline, p_body);
        SELECT LAST_INSERT_ID();  
    END 
//


-- reset delimiter
DELIMITER ; 

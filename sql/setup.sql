/* drop tables */
SET foreign_key_checks=0;

DROP TABLE IF EXISTS industry;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS pub;
DROP TABLE IF EXISTS prelease;
DROP TABLE IF EXISTS article; 
DROP TABLE IF EXISTS pair; 
DROP TABLE IF EXISTS block; 

SET foreign_key_checks=1;


/* create tables*/

CREATE TABLE IF NOT EXISTS industry (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS company (
	id INT NOT NULL PRIMARY KEY,
    industry_id INT NOT NULL,
    rank INT NOT NULL,
	name VARCHAR(50) NOT NULL UNIQUE,
    releases INT NOT NULL,
    articles INT NOT NULL,
    pairs INT NOT NULL)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS pub (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL UNIQUE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS prelease (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    published  DATE,
	title VARCHAR(500),
    all_tokens INT,
    pos_tokens INT,
    neg_tokens INT,
    all_sents INT,
    pos_sents INT,
    neg_sents INT,
    posneg_sents INT,
    subj_score DOUBLE,
    sent_score DOUBLE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS article (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    pub_id INT NOT NULL,
    published  DATE,
	author VARCHAR(100),
	headline VARCHAR(500),
    all_tokens INT,
    pos_tokens INT,
    neg_tokens INT,
    all_sents INT,
    pos_sents INT,
    neg_sents INT,
    posneg_sents INT,
    subj_score DOUBLE,
    sent_score DOUBLE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS pair (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    prelease_id INT NOT NULL,
    article_id INT NOT NULL,
    proportion_in_rel DOUBLE,
    proportion_in_art DOUBLE)
    ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS block (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pair_id INT NOT NULL,
    tokens INT,
    text TEXT)
    ENGINE = InnoDB;


/* add foreign keys */

ALTER TABLE company
	ADD CONSTRAINT fk_company_industry
		FOREIGN KEY (industry_id) REFERENCES industry(id);

ALTER TABLE prelease
	ADD CONSTRAINT fk_prelease_company
		FOREIGN KEY (company_id) REFERENCES company(id);

ALTER TABLE article
	ADD CONSTRAINT fk_article_company
		FOREIGN KEY (company_id) REFERENCES company(id),
	ADD CONSTRAINT fk_article_pub
		FOREIGN KEY (pub_id) REFERENCES pub(id);

ALTER TABLE pair
	ADD CONSTRAINT fk_pair_company
		FOREIGN KEY (company_id) REFERENCES company(id),
	ADD CONSTRAINT fk_pair_prelease
		FOREIGN KEY (prelease_id) REFERENCES prelease(id),
	ADD CONSTRAINT fk_pair_article
		FOREIGN KEY (article_id) REFERENCES article(id);

ALTER TABLE block
	ADD CONSTRAINT fk_block_pair
		FOREIGN KEY (pair_id) REFERENCES pair(id);


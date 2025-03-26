-- TEST: Questo script viene eseguito all'inizializzazione del database
-- Creazione del database
DROP DATABASE IF EXISTS simulazione;
CREATE DATABASE simulazione;
USE simulazione;

-- Tabella veicoliSicuri
CREATE TABLE IF NOT EXISTS `veicoliSicuri` (
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `tipo` VARCHAR(255) NOT NULL,
    `durata` BIGINT NOT NULL,
    `partenza` VARCHAR(255) NOT NULL,
    `arrivo` VARCHAR(255) NOT NULL,
    `tempoPartenza` BIGINT NOT NULL,
    `tempoArrivo` BIGINT NOT NULL
);

-- Tabella IncidentiSicuri
CREATE TABLE IF NOT EXISTS `incidentiSicuri` (
    `numeroIncidenti` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `tempo` VARCHAR(255) NOT NULL
);

-- Tabella statisticheSicure
CREATE TABLE IF NOT EXISTS `statisticheSicure` (
    `tempo` BIGINT NOT NULL,
    `nMacchine` BIGINT NOT NULL,
    `mDurata` BIGINT NOT NULL,
    `mFermo` FLOAT NOT NULL
);

-- Tabella veicoliSicuri
CREATE TABLE IF NOT EXISTS `veicoliRischiosi` (
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `tipo` VARCHAR(255) NOT NULL,
    `durata` BIGINT NOT NULL,
    `partenza` VARCHAR(255) NOT NULL,
    `arrivo` VARCHAR(255) NOT NULL,
    `tempoPartenza` BIGINT NOT NULL,
    `tempoArrivo` BIGINT NOT NULL
);

-- Tabella IncidentiRischiosi
CREATE TABLE IF NOT EXISTS `incidentiRischiosi` (
    `numeroIncidenti` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `tempo` VARCHAR(255) NOT NULL
);

-- Tabella statisticheRischiosi
CREATE TABLE IF NOT EXISTS `statisticheRischiose` (
    `tempo` BIGINT NOT NULL,
    `nMacchine` BIGINT NOT NULL,
    `mDurata` BIGINT NOT NULL,
    `mFermo` FLOAT NOT NULL
);

-- Tabella logs
CREATE TABLE IF NOT EXISTS `logs` (
    `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `time` TIMESTAMP NOT NULL
);






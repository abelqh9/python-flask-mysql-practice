-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema python_belt_2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema python_belt_2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `python_belt_2` DEFAULT CHARACTER SET utf8 ;
USE `python_belt_2` ;

-- -----------------------------------------------------
-- Table `python_belt_2`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `python_belt_2`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(225) NULL,
  `last_name` VARCHAR(225) NULL,
  `email` VARCHAR(225) NULL,
  `password` VARCHAR(225) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `python_belt_2`.`cars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `python_belt_2`.`cars` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `price` INT NULL,
  `model` VARCHAR(225) NULL,
  `make` VARCHAR(225) NULL,
  `year` DATETIME NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_cars_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_cars_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `python_belt_2`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `python_belt_2`.`purchases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `python_belt_2`.`purchases` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `car_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_purchases_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_purchases_cars1_idx` (`car_id` ASC) VISIBLE,
  CONSTRAINT `fk_purchases_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `python_belt_2`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_purchases_cars1`
    FOREIGN KEY (`car_id`)
    REFERENCES `python_belt_2`.`cars` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

--- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- -----------------------------------------------------
-- Schema lab_mysql
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `lab_mysql` DEFAULT CHARACTER SET utf8 ;
USE `lab_mysql` ;

-- -----------------------------------------------------
-- Table `lab_mysql`.`cars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lab_mysql`.`cars` (
  `ID` INT(11) NOT NULL,
  `vin` VARCHAR(45) NOT NULL,
  `manufacturer` VARCHAR(45) NOT NULL,
  `model` VARCHAR(45) NOT NULL,
  `year` INT(11) NOT NULL,
  `color` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `lab_mysql`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lab_mysql`.`customers` (
  `ID` INT(11) NOT NULL,
  `id_customer` INT(11) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `phone` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `address` VARCHAR(45) NULL DEFAULT NULL,
  `city` VARCHAR(45) NULL DEFAULT NULL,
  `state` VARCHAR(45) NULL DEFAULT NULL,
  `country` VARCHAR(45) NULL DEFAULT NULL,
  `postal` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `lab_mysql`.`salespersons`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lab_mysql`.`salespersons` (
  `ID` INT(11) NOT NULL,
  `staff_id` INT(11) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `store` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `lab_mysql`.`customers_has_salespersons`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lab_mysql`.`customers_has_salespersons` (
  `Customers_ID` INT(11) NOT NULL,
  `SalesPersons_ID` INT(11) NOT NULL,
  PRIMARY KEY (`Customers_ID`, `SalesPersons_ID`),
  INDEX `fk_Customers_has_SalesPersons_SalesPersons1_idx` (`SalesPersons_ID` ASC) VISIBLE,
  INDEX `fk_Customers_has_SalesPersons_Customers1_idx` (`Customers_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Customers_has_SalesPersons_Customers1`
    FOREIGN KEY (`Customers_ID`)
    REFERENCES `lab_mysql`.`customers` (`ID`),
  CONSTRAINT `fk_Customers_has_SalesPersons_SalesPersons1`
    FOREIGN KEY (`SalesPersons_ID`)
    REFERENCES `lab_mysql`.`salespersons` (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `lab_mysql`.`invoices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lab_mysql`.`invoices` (
  `ID` INT(11) NOT NULL,
  `invoice_number` INT(11) NOT NULL,
  `date` DATE NULL DEFAULT NULL,
  `Customers_ID` INT(11) NOT NULL,
  `SalesPersons_ID` INT(11) NOT NULL,
  PRIMARY KEY (`ID`, `Customers_ID`, `SalesPersons_ID`),
  INDEX `fk_Invoices_Customers_idx` (`Customers_ID` ASC) VISIBLE,
  INDEX `fk_Invoices_SalesPersons1_idx` (`SalesPersons_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Invoices_Customers`
    FOREIGN KEY (`Customers_ID`)
    REFERENCES `lab_mysql`.`customers` (`ID`),
  CONSTRAINT `fk_Invoices_SalesPersons1`
    FOREIGN KEY (`SalesPersons_ID`)
    REFERENCES `lab_mysql`.`salespersons` (`ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `lab_mysql`.`invoices_has_cars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lab_mysql`.`invoices_has_cars` (
  `Invoices_ID` INT(11) NOT NULL,
  `Invoices_Customers_ID` INT(11) NOT NULL,
  `Invoices_SalesPersons_ID` INT(11) NOT NULL,
  `Cars_ID` INT(11) NOT NULL,
  PRIMARY KEY (`Invoices_ID`, `Invoices_Customers_ID`, `Invoices_SalesPersons_ID`, `Cars_ID`),
  INDEX `fk_Invoices_has_Cars_Cars1_idx` (`Cars_ID` ASC) VISIBLE,
  INDEX `fk_Invoices_has_Cars_Invoices1_idx` (`Invoices_ID` ASC, `Invoices_Customers_ID` ASC, `Invoices_SalesPersons_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Invoices_has_Cars_Cars1`
    FOREIGN KEY (`Cars_ID`)
    REFERENCES `lab_mysql`.`cars` (`ID`),
  CONSTRAINT `fk_Invoices_has_Cars_Invoices1`
    FOREIGN KEY (`Invoices_ID` , `Invoices_Customers_ID` , `Invoices_SalesPersons_ID`)
    REFERENCES `lab_mysql`.`invoices` (`ID` , `Customers_ID` , `SalesPersons_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

CREATE TABLE IF NOT EXISTS INVENTORY (
	INVT_CODE INTEGER UNSIGNED AUTO_INCREMENT,
    INVT_NAME VARCHAR(50) NOT NULL,
    INVT_DESC TEXT NOT NULL,
    INVT_CATEGORY VARCHAR(20) NOT NULL,
    INVT_QTY SMALLINT,
    INVT_EXP_DATE DATE,
    PRIMARY KEY (INVT_CODE),
    CONSTRAINT INVT_NAME UNIQUE (INVT_NAME)
);

/* notes
an inventory item cannot be entered twice; therefore, a unique constraint is placed.
a food inventory item must have an expiration date. 
any set of food or ingredients deployed for students to eat and the remaining untouched must be thrown by the end of the day.
*/

ALTER TABLE INVENTORY
MODIFY INVT_NAME VARCHAR(150) NOT NULL;

ALTER TABLE INVENTORY
MODIFY INVT_QTY SMALLINT NULL;

ALTER TABLE INVENTORY
MODIFY INVT_CATEGORY VARCHAR(50) NOT NULL;
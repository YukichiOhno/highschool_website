CREATE TABLE IF NOT EXISTS EMPLOYEE (
	EMP_ID INTEGER UNSIGNED AUTO_INCREMENT,
    EMP_FNAME VARCHAR(20) NOT NULL,
    EMP_LNAME VARCHAR(20) NOT NULL,
    EMP_INITIAL CHAR(1),
    EMP_DOB DATE NOT NULL,
    EMP_ADDRESS VARCHAR(150) NOT NULL,
    EMP_CITY VARCHAR(50) NOT NULL,
    EMP_PHONE VARCHAR(10) NOT NULL,
    EMP_EMAIL VARCHAR(50) NOT NULL,
    EMP_EMPLOY_DATE DATE NOT NULL,
    POS_CODE INTEGER UNSIGNED,
    PRIMARY KEY (EMP_ID),
    FOREIGN KEY (POS_CODE) REFERENCES POSITION (POS_CODE) ON UPDATE CASCADE,
    CONSTRAINT EMP_EMAIL UNIQUE (EMP_EMAIL)
);

CREATE INDEX EMP_NAME ON EMPLOYEE (EMP_LNAME, EMP_FNAME);

/* notes 
an employee cannot share the same email; therefore a unique constraint is placed.
*/
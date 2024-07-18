CREATE TABLE IF NOT EXISTS POSITION (
	POS_CODE INTEGER UNSIGNED AUTO_INCREMENT,
    POS_TITLE VARCHAR(25) NOT NULL,
    POS_DESC TEXT NOT NULL,
    POS_SALARY DECIMAL(8, 2) NOT NULL,
    POS_REQ TEXT,
    DEPT_CODE INTEGER UNSIGNED,
    PRIMARY KEY (POS_CODE),
    FOREIGN KEY (DEPT_CODE) REFERENCES DEPARTMENT (DEPT_CODE) ON UPDATE CASCADE
);

ALTER TABLE POSITION
ADD CONSTRAINT POS_TITLE UNIQUE (POS_TITLE);

CREATE INDEX POS_SALARY ON POSITION (POS_SALARY);

/* notes
a position name cannot repeat; therefore a unqiue constraint is placed.
*/
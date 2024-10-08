CREATE TABLE IF NOT EXISTS BUDGET (
	BUD_ID INTEGER UNSIGNED AUTO_INCREMENT,
    BUD_TYPE VARCHAR(25) NOT NULL,
    BUD_DESC TEXT NOT NULL,
    BUD_ALLOCATED DECIMAL(9, 2) NOT NULL,
    BUD_REMAIN DECIMAL(9, 2) NOT NULL,
    BUD_APPROVAL_DATE DATE NOT NULL,
    BUD_EXP_DATE DATE NOT NULL,
    DEPT_CODE INTEGER UNSIGNED,
    PRIMARY KEY (BUD_ID),
    FOREIGN KEY (DEPT_CODE) REFERENCES DEPARTMENT (DEPT_CODE) ON UPDATE CASCADE,
    CONSTRAINT BUD_ALLOCATED CHECK (BUD_ALLOCATED > 0),
    CONSTRAINT BUD_REMAIN CHECK (BUD_REMAIN > 0)
);

/* notes
a budget may not be allocated at less than $0
once a budget is expired, budget allocation and remaining will cease to update
*/

ALTER TABLE BUDGET
MODIFY BUD_REMAIN DECIMAL(9, 2) NULL;

ALTER TABLE BUDGET
MODIFY BUD_TYPE VARCHAR(50) NOT NULL;


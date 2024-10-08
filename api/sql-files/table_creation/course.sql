CREATE TABLE IF NOT EXISTS COURSE (
	COURSE_ID INTEGER UNSIGNED AUTO_INCREMENT,
    COURSE_NAME VARCHAR(50) NOT NULL,
    COURSE_DESC TEXT NOT NULL,
    COURSE_TYPE VARCHAR(20) NOT NULL,
    COURSE_HRS SMALLINT NOT NULL,
    COURSE_GRADE_LVL SMALLINT,
    PRIMARY KEY (COURSE_ID),
    CONSTRAINT COURSE_NAME UNIQUE (COURSE_NAME)
);
/* notes
a course cannot be entered twice, therefore a unqiue constraint is placed on the name
*/
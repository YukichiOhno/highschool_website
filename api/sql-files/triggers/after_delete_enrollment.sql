/*ENROLLMENT trigger*/

DELIMITER //

CREATE TRIGGER AFTER_DELETE_ENROLLMENT AFTER DELETE 
ON ENROLLMENT
FOR EACH ROW 
BEGIN
    DECLARE TOTAL_GRADE DECIMAL(10, 2);
    DECLARE CLASS_COUNT INT;
    DECLARE CALCULATED_GPA DECIMAL(4, 2);

    -- Calculate the student's total grades excluding dropped classes and the deleted row
    SELECT SUM(E.ENROLL_SCORE * C.COURSE_HRS) AS TOTAL_GRADE_PTS, SUM(C.COURSE_HRS) AS TOTAL_COURSE_HRS INTO TOTAL_GRADE, CLASS_COUNT
    FROM ENROLLMENT E
    JOIN CLASS CL ON E.CLASS_ID = CL.CLASS_ID
    JOIN COURSE C ON CL.COURSE_ID = C.COURSE_ID
    WHERE E.STUD_ID = OLD.STUD_ID AND E.ENROLL_STATUS != 'dropped';

    -- Calculate GPA and ensure it's within the valid range
    IF CLASS_COUNT > 0 THEN
        SET CALCULATED_GPA = TOTAL_GRADE / CLASS_COUNT;
        -- Clamp GPA between 0 and 4
        IF CALCULATED_GPA > 4.0 THEN
            SET CALCULATED_GPA = 4.0;
        ELSEIF CALCULATED_GPA < 0 THEN
            SET CALCULATED_GPA = 0;
        END IF;
    ELSE
        SET CALCULATED_GPA = 0;
    END IF;

    -- Update the student's GPA in the student table
    UPDATE STUDENT
    SET STUD_GPA = CALCULATED_GPA
    WHERE STUD_ID = OLD.STUD_ID;

END //

DELIMITER ;

/*
After deleting the ENROLL_SCORE attribute of an entity in the ENROLLMENT table,
update the student's GPA in the STUDENT table
*/
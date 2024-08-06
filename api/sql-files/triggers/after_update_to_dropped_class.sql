/*ENROLLMENT trigger*/

DELIMITER //

CREATE TRIGGER AFTER_UPDATE_TO_DROPPED_CLASS 
AFTER UPDATE ON ENROLLMENT
FOR EACH ROW 
BEGIN
    DECLARE TOTAL_GRADE DECIMAL(10, 2);
    DECLARE CLASS_COUNT INT;
    DECLARE CALCULATED_GPA DECIMAL(4, 2);

    -- Only recalculate GPA if ENROLL_STATUS has changed to "dropped" or if it's an update of interest
    IF OLD.ENROLL_STATUS <> NEW.ENROLL_STATUS AND NEW.ENROLL_STATUS = 'dropped' THEN

        -- Calculate the student's total grades excluding dropped classes
        SELECT SUM(E.ENROLL_SCORE * C.COURSE_HRS) AS TOTAL_GRADE_PTS, SUM(C.COURSE_HRS) AS TOTAL_COURSE_HRS INTO TOTAL_GRADE, CLASS_COUNT
        FROM ENROLLMENT E
        JOIN CLASS CL ON E.CLASS_ID = CL.CLASS_ID
        JOIN COURSE C ON CL.COURSE_ID = C.COURSE_ID
        WHERE E.STUD_ID = NEW.STUD_ID AND E.ENROLL_STATUS != 'dropped';

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
        WHERE STUD_ID = NEW.STUD_ID;

    END IF;

END //

DELIMITER ;
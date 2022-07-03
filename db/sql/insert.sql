INSERT INTO JOBS
    (
        TITLE
        , OCCUPATION
        , SALARY
        , WORK_LOCATION
        , WORKING_HOURS
        , CREATED_AT
    ) VALUES (
        '{title}'
        , '{occupation}'
        , '{salary}'
        , '{work_location}'
        , '{working_hours}'
        , SYSDATE()
    )

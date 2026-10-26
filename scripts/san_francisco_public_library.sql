DROP DATABASE IF EXISTS san_francisco_public_library;
CREATE DATABASE san_francisco_public_library;
USE san_francisco_public_library;


CREATE TABLE PATRON_TYPE (
    PatronTypeCode TINYINT UNSIGNED NOT NULL,
    PatronTypeDescription VARCHAR(20) NOT NULL,

    CONSTRAINT PATRON_TYPE_CODE_PK PRIMARY KEY (PatronTypeCode)
);

CREATE TABLE AGE_RANGE (
	AgeRangeCode TINYINT UNSIGNED NOT NULL,
    AgeRangeDescription VARCHAR(15) NOT NULL,
    
    CONSTRAINT AGE_RANGE_CODE_PK PRIMARY KEY (AgeRangeCode)
);

CREATE TABLE NOTIFICATION_MEDIUM (
    NotificationMediumCode CHAR(1) NOT NULL,
    NotificationDescription VARCHAR(10) NOT NULL,

    CONSTRAINT NOTIFICATION_MEDIUM_CODE_PK PRIMARY KEY (NotificationMediumCode)
);

CREATE TABLE HOME_LIBRARY (
    HomeLibraryCode VARCHAR(5) NOT NULL,
    HomeLibraryDescription VARCHAR(20) NOT NULL,

    CONSTRAINT HOME_LIBRARY_CODE_PK PRIMARY KEY (HomeLibraryCode)
);

CREATE TABLE PATRON (
    PatronNumber INT UNSIGNED NOT NULL AUTO_INCREMENT,
    PatronTypeCode TINYINT UNSIGNED NOT NULL,
    AgeRangeCode TINYINT UNSIGNED NOT NULL,
    NotificationPreference CHAR(1) NOT NULL,
    HomeLibraryCode VARCHAR(5),
    
    CheckoutTotal INT UNSIGNED NOT NULL,
    RenewalTotal INT UNSIGNED NOT NULL,
    CirculationActiveMonth TINYINT UNSIGNED,
    CirculationActiveYear SMALLINT UNSIGNED,
    ProvidedEmailAddress BOOLEAN NOT NULL,
    WithinSanFranciscoCounty BOOLEAN NOT NULL,
    YearPatronRegistered SMALLINT UNSIGNED NOT NULL,

    CONSTRAINT PATRON_NUMBER_PK PRIMARY KEY (PatronNumber),
    CONSTRAINT PATRON_TYPE_CODE_FK FOREIGN KEY (PatronTypeCode) 
        REFERENCES PATRON_TYPE (PatronTypeCode),
    CONSTRAINT AGE_RANGE_CODE_FK FOREIGN KEY (AgeRangeCode) 
        REFERENCES AGE_RANGE (AgeRangeCode),
    CONSTRAINT NOTIFICATION_PREFERENCE_FK FOREIGN KEY (NotificationPreference) 
        REFERENCES NOTIFICATION_MEDIUM (NotificationMediumCode),
    CONSTRAINT HOME_LIBRARY_CODE_FK FOREIGN KEY (HomelibraryCode) 
        REFERENCES HOME_LIBRARY (HomeLibraryCode)
);

INSERT INTO PATRON_TYPE (PatronTypeCode, PatronTypeDescription) VALUES (0, "test 0");
INSERT INTO PATRON_TYPE (PatronTypeCode, PatronTypeDescription) VALUES (1, "test 1");
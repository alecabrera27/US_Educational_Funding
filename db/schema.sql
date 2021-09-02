-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "BaseRecord" (
    "Id" int   NOT NULL,
    "Year" int   NOT NULL,
    "State" string   NOT NULL,
    CONSTRAINT "pk_BaseRecord" PRIMARY KEY (
        "Id"
     )
);

CREATE TABLE "Financials" (
    "RecordId" int   NOT NULL,
    "Enrolled" int   NOT NULL,
    "TotalRevenue" int   NOT NULL,
    "FederalRevenue" int   NOT NULL,
    "StateRevenue" int   NOT NULL,
    "LocalRevenue" int   NOT NULL,
    "InstructionExpenditure" int   NOT NULL,
    "SupportServicesExpenditure" int   NOT NULL,
    "CapitalOutlayExpenditure" int   NOT NULL,
    "OtherExpenditure" int   NOT NULL,
    CONSTRAINT "pk_Financials" PRIMARY KEY (
        "RecordId"
     )
);

CREATE TABLE "Achievements" (
    "RecordId" int   NOT NULL,
    "AvgMath4Score" int   NOT NULL,
    "AvgMath8Score" int   NOT NULL,
    "AvgReading4Score" int   NOT NULL,
    "AvgReading8Score" int   NOT NULL,
    CONSTRAINT "pk_Achievements" PRIMARY KEY (
        "RecordId"
     )
);

ALTER TABLE "Financials" ADD CONSTRAINT "fk_Financials_RecordId" FOREIGN KEY("RecordId")
REFERENCES "BaseRecord" ("Id");

ALTER TABLE "Achievements" ADD CONSTRAINT "fk_Achievements_RecordId" FOREIGN KEY("RecordId")
REFERENCES "BaseRecord" ("Id");

CREATE INDEX "idx_BaseRecord_Year"
ON "BaseRecord" ("Year");

CREATE INDEX "idx_BaseRecord_State"
ON "BaseRecord" ("State");


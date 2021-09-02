-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "BaseRecord" (
    "ID" int   NOT NULL,
    "Year" int   NOT NULL,
    "State" string   NOT NULL,
    CONSTRAINT "pk_BaseRecord" PRIMARY KEY (
        "ID"
     )
);

CREATE INDEX "idx_BaseRecord_Year"
ON "BaseRecord" ("Year");

CREATE INDEX "idx_BaseRecord_State"
ON "BaseRecord" ("State");


-- ============================================
-- Luxury Housing Sales Analysis - SQL Schema
-- Database: luxury_housing_db
-- ============================================

CREATE DATABASE IF NOT EXISTS luxury_housing_db;
USE luxury_housing_db;

DROP TABLE IF EXISTS luxury_housing;

CREATE TABLE luxury_housing (
    Property_ID         VARCHAR(20) PRIMARY KEY,
    Micro_Market        VARCHAR(50),
    Project_Name        VARCHAR(100),
    Developer_Name      VARCHAR(100),
    Unit_Size_Sqft      FLOAT,
    Configuration       VARCHAR(10),
    Ticket_Price_Cr     FLOAT,
    Transaction_Type    VARCHAR(20),
    Buyer_Type          VARCHAR(30),
    Purchase_Quarter    DATE,
    Connectivity_Score  FLOAT,
    Amenity_Score       FLOAT,
    Possession_Status   VARCHAR(30),
    Sales_Channel       VARCHAR(20),
    NRI_Buyer           VARCHAR(5),
    Locality_Infra_Score FLOAT,
    Avg_Traffic_Time_Min INT,
    Buyer_Comments      TEXT,
    Price_per_Sqft      FLOAT,
    Quarter_Number      INT,
    Quarter_Label       VARCHAR(10),
    Booking_Flag        INT
);

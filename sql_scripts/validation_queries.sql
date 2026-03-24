-- =====================================================
-- Luxury Housing Sales Analysis - Validation Queries
-- Run these after loading data to verify correctness
-- =====================================================

USE luxury_housing_db;

-- 1. Total record count
SELECT COUNT(*) AS total_records FROM luxury_housing;

-- 2. Booking status distribution (Possession_Status)
SELECT 
    Possession_Status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM luxury_housing), 2) AS percentage
FROM luxury_housing
GROUP BY Possession_Status
ORDER BY count DESC;

-- 3. Average ticket price per developer (Top 10)
SELECT 
    Developer_Name,
    COUNT(*) AS total_properties,
    ROUND(AVG(Ticket_Price_Cr), 2) AS avg_ticket_price_cr,
    ROUND(SUM(Ticket_Price_Cr), 2) AS total_revenue_cr
FROM luxury_housing
GROUP BY Developer_Name
ORDER BY total_revenue_cr DESC
LIMIT 10;

-- 4. Top 10 micro-markets by total revenue
SELECT 
    Micro_Market,
    COUNT(*) AS total_properties,
    ROUND(SUM(Ticket_Price_Cr), 2) AS total_revenue_cr,
    ROUND(AVG(Ticket_Price_Cr), 2) AS avg_price_cr
FROM luxury_housing
GROUP BY Micro_Market
ORDER BY total_revenue_cr DESC
LIMIT 10;

-- 5. Configuration demand breakdown
SELECT 
    Configuration,
    COUNT(*) AS demand_count,
    ROUND(AVG(Ticket_Price_Cr), 2) AS avg_price_cr,
    ROUND(AVG(Unit_Size_Sqft), 0) AS avg_sqft
FROM luxury_housing
GROUP BY Configuration
ORDER BY demand_count DESC;

-- 6. Quarterly trend (total revenue per quarter)
SELECT 
    Quarter_Label,
    COUNT(*) AS num_transactions,
    ROUND(SUM(Ticket_Price_Cr), 2) AS total_revenue_cr,
    ROUND(AVG(Ticket_Price_Cr), 2) AS avg_price_cr
FROM luxury_housing
GROUP BY Quarter_Label
ORDER BY Quarter_Label;

-- 7. Booking flag distribution
SELECT 
    Booking_Flag,
    COUNT(*) AS count
FROM luxury_housing
GROUP BY Booking_Flag;

-- 8. Sales channel performance
SELECT 
    Sales_Channel,
    COUNT(*) AS total_leads,
    SUM(Booking_Flag) AS successful_bookings,
    ROUND(SUM(Booking_Flag) * 100.0 / COUNT(*), 2) AS conversion_rate
FROM luxury_housing
GROUP BY Sales_Channel
ORDER BY conversion_rate DESC;

-- 9. Buyer type analysis
SELECT 
    Buyer_Type,
    COUNT(*) AS count,
    ROUND(AVG(Ticket_Price_Cr), 2) AS avg_price_cr,
    ROUND(AVG(Amenity_Score), 2) AS avg_amenity_score
FROM luxury_housing
GROUP BY Buyer_Type
ORDER BY count DESC;

-- 10. NRI vs Non-NRI buyer comparison
SELECT 
    NRI_Buyer,
    COUNT(*) AS count,
    ROUND(AVG(Ticket_Price_Cr), 2) AS avg_price_cr,
    ROUND(SUM(Ticket_Price_Cr), 2) AS total_revenue_cr
FROM luxury_housing
GROUP BY NRI_Buyer;

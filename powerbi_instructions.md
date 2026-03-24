# Power BI Dashboard Setup – Luxury Housing Sales Analysis

## Step 1: Connect Power BI to MySQL

1. Open **Power BI Desktop**
2. Click **Get Data** → **MySQL database**
3. Enter connection details:
   - **Server**: `localhost`
   - **Database**: `luxury_housing_db`
4. Authentication: **Database** → Username: `root`, Password: `pass@123`
5. Select the `luxury_housing` table → Click **Load**

> **Note**: Install the MySQL Connector/NET if prompted by Power BI.

---

## Step 2: DAX Measures

Create these measures in Power BI:

```dax
-- Total Revenue
Total Revenue = SUM(luxury_housing[Ticket_Price_Cr])

-- Average Ticket Size
Avg Ticket Size = AVERAGE(luxury_housing[Ticket_Price_Cr])

-- Booking Count
Booking Count = SUM(luxury_housing[Booking_Flag])

-- Total Properties
Total Properties = COUNTROWS(luxury_housing)

-- Booking Conversion Rate
Booking Conversion Rate = 
    DIVIDE(
        SUM(luxury_housing[Booking_Flag]),
        COUNTROWS(luxury_housing),
        0
    ) * 100

-- Average Amenity Score
Avg Amenity Score = AVERAGE(luxury_housing[Amenity_Score])

-- Average Price per Sqft
Avg Price per Sqft = AVERAGE(luxury_housing[Price_per_Sqft])
```

---

## Step 3: Dashboard Visuals (10 Charts)

### 1. Market Trends – Quarterly Bookings by Micro-Market
- **Type**: Line Chart
- **X-axis**: `Quarter_Label`
- **Y-axis**: `Booking Count` (measure)
- **Legend**: `Micro_Market`

### 2. Builder Performance – Revenue & Avg Ticket
- **Type**: Clustered Bar Chart (or Table)
- **Axis**: `Developer_Name`
- **Values**: `Total Revenue`, `Avg Ticket Size`
- Sort descending by Total Revenue

### 3. Amenity Impact – Score vs Booking Rate
- **Type**: Scatter Plot
- **X-axis**: Average of `Amenity_Score`
- **Y-axis**: `Booking Conversion Rate`
- **Size**: Count of `Property_ID`
- **Details**: `Micro_Market`

### 4. Booking Conversion by Micro-Market
- **Type**: Stacked Column Chart
- **Axis**: `Micro_Market`
- **Values**: Count of `Property_ID`
- **Legend**: `Possession_Status`

### 5. Configuration Demand
- **Type**: Donut Chart
- **Legend**: `Configuration`
- **Values**: Count of `Property_ID`

### 6. Sales Channel Efficiency
- **Type**: 100% Stacked Column Chart
- **Axis**: `Sales_Channel`
- **Values**: Count of `Property_ID`
- **Legend**: `Booking_Flag`

### 7. Quarterly Builder Contribution
- **Type**: Matrix Table
- **Rows**: `Developer_Name`
- **Columns**: `Quarter_Label`
- **Values**: `Total Revenue`

### 8. Possession Status vs Buyer Type
- **Type**: Clustered Column Chart
- **Axis**: `Possession_Status`
- **Values**: Count of `Property_ID`
- **Legend**: `Buyer_Type`

### 9. Geographical Insights
- **Type**: Filled Map or Treemap
- **Location/Category**: `Micro_Market`
- **Size**: `Total Revenue`
- **Color**: `Booking Conversion Rate`

### 10. Top 5 Builders – KPI Cards
- Create **Card visuals** for the top 5 builders showing:
  - Total Revenue
  - Booking Count
  - Avg Ticket Size
- Add a **drill-through** page filtered by `Developer_Name` with full project details

---

## Step 4: Slicers & Filters

Add **Slicer visuals** for:
- `Micro_Market` (dropdown)
- `Developer_Name` (dropdown)
- `Quarter_Label` (between)
- `Configuration` (buttons)
- `Buyer_Type` (dropdown)
- `Possession_Status` (buttons)

---

## Step 5: Formatting Tips

- Use a **dark theme** for a premium dashboard look
- Add a **text box** at the top with the title: *"Luxury Housing Sales Analysis – Bengaluru"*
- Use **conditional formatting** on the Matrix table (color scale for revenue)
- Add **tooltips** showing Price_per_Sqft and Amenity_Score on hover
- Include a **Buyer Comments** text analysis section using a Word Cloud custom visual

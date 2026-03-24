"""
Luxury Housing Sales Analysis - Data Cleaning & Feature Engineering
Cleans the raw Bangalore luxury housing dataset and exports a refined CSV.
"""

import pandas as pd
import numpy as np
import os


def load_data(filepath):
    """Load raw CSV file into a DataFrame."""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df


def clean_ticket_price(df):
    """
    Clean the Ticket_Price_Cr column:
    - Remove '₹' prefix and ' Cr' suffix
    - Convert to float
    - Cap extreme outliers (>50 Cr) as NaN
    """
    print("Cleaning Ticket_Price_Cr...")

    def parse_price(val):
        if pd.isna(val):
            return np.nan
        val = str(val).strip()
        # Remove ₹ symbol and 'Cr' text
        val = val.replace('₹', '').replace('Cr', '').strip()
        try:
            price = float(val)
            # Cap extreme outliers
            if price > 50:
                return np.nan
            return price
        except ValueError:
            return np.nan

    df['Ticket_Price_Cr'] = df['Ticket_Price_Cr'].apply(parse_price)
    return df


def normalize_text_fields(df):
    """
    Normalize text columns:
    - Micro_Market -> Title Case
    - Developer_Name -> Title Case
    - Configuration -> Uppercase (3BHK, 4BHK, 5BHK+)
    - NRI_Buyer -> lowercase
    """
    print("Normalizing text fields...")

    # Micro_Market: title case
    df['Micro_Market'] = df['Micro_Market'].str.strip().str.title()

    # Developer_Name: title case
    df['Developer_Name'] = df['Developer_Name'].str.strip().str.title()

    # Configuration: uppercase
    df['Configuration'] = df['Configuration'].str.strip().str.upper()

    # NRI_Buyer: lowercase
    df['NRI_Buyer'] = df['NRI_Buyer'].str.strip().str.lower()

    # Buyer_Type: title case
    df['Buyer_Type'] = df['Buyer_Type'].str.strip().str.title()

    # Transaction_Type: title case
    df['Transaction_Type'] = df['Transaction_Type'].str.strip().str.title()

    # Possession_Status: title case
    df['Possession_Status'] = df['Possession_Status'].str.strip().str.title()

    # Sales_Channel: title case
    df['Sales_Channel'] = df['Sales_Channel'].str.strip().str.title()

    return df


def fix_invalid_values(df):
    """Replace invalid values with NaN."""
    print("Fixing invalid values...")

    # Negative or zero Unit_Size_Sqft -> NaN
    df.loc[df['Unit_Size_Sqft'] <= 0, 'Unit_Size_Sqft'] = np.nan

    return df


def handle_nulls(df):
    """
    Handle missing values:
    - Amenity_Score: fill with median
    - Unit_Size_Sqft: fill with median per Configuration
    - Ticket_Price_Cr: fill with median per Micro_Market
    - Buyer_Comments: fill with empty string
    """
    print("Handling null values...")

    # Amenity_Score: fill with overall median
    median_amenity = df['Amenity_Score'].median()
    df['Amenity_Score'] = df['Amenity_Score'].fillna(median_amenity)

    # Unit_Size_Sqft: fill with median per Configuration
    df['Unit_Size_Sqft'] = df.groupby('Configuration')['Unit_Size_Sqft'].transform(
        lambda x: x.fillna(x.median())
    )

    # Ticket_Price_Cr: fill with median per Micro_Market
    df['Ticket_Price_Cr'] = df.groupby('Micro_Market')['Ticket_Price_Cr'].transform(
        lambda x: x.fillna(x.median())
    )

    # Buyer_Comments: fill with empty string
    df['Buyer_Comments'] = df['Buyer_Comments'].fillna('')

    return df


def derive_features(df):
    """
    Create derived columns:
    - Price_per_Sqft: Ticket_Price_Cr * 10000000 / Unit_Size_Sqft
    - Quarter_Number: Q1, Q2, Q3, Q4 from Purchase_Quarter date
    - Booking_Flag: 1 if booked (Ready To Move / Under Construction), 0 otherwise
    """
    print("Deriving new features...")

    # Price per square foot (in INR)
    df['Price_per_Sqft'] = (df['Ticket_Price_Cr'] * 10000000) / df['Unit_Size_Sqft']
    df['Price_per_Sqft'] = df['Price_per_Sqft'].round(2)

    # Quarter Number from Purchase_Quarter (date like 2024-03-31)
    df['Purchase_Quarter'] = pd.to_datetime(df['Purchase_Quarter'], errors='coerce')
    df['Quarter_Number'] = df['Purchase_Quarter'].dt.quarter
    df['Quarter_Label'] = df['Purchase_Quarter'].dt.year.astype(str) + '-Q' + df['Quarter_Number'].astype(str)

    # Booking Flag: 1 for Ready To Move or Under Construction
    df['Booking_Flag'] = df['Possession_Status'].apply(
        lambda x: 1 if x in ['Ready To Move', 'Under Construction'] else 0
    )

    return df


def main():
    """Main function to run the full data cleaning pipeline."""
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_file = os.path.join(base_dir, 'Luxury_Housing_Bangalore.csv')
    clean_file = os.path.join(base_dir, 'Luxury_Housing_Cleaned.csv')

    # Step 1: Load data
    df = load_data(raw_file)

    # Step 2: Clean ticket price
    df = clean_ticket_price(df)

    # Step 3: Normalize text fields
    df = normalize_text_fields(df)

    # Step 4: Fix invalid values
    df = fix_invalid_values(df)

    # Step 5: Handle nulls
    df = handle_nulls(df)

    # Step 6: Derive features
    df = derive_features(df)

    # Step 7: Remove duplicate Property_IDs
    before = len(df)
    df = df.drop_duplicates(subset='Property_ID', keep='first')
    print(f"Removed {before - len(df)} duplicate Property_IDs.")

    # Save cleaned data
    df.to_csv(clean_file, index=False)
    print(f"\nCleaned data saved to {clean_file}")
    print(f"Final shape: {df.shape}")
    print(f"\nNull counts:\n{df.isnull().sum()}")
    print(f"\nSample rows:\n{df.head()}")


if __name__ == '__main__':
    main()

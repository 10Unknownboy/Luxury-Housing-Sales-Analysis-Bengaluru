"""
Luxury Housing Sales Analysis - Load Cleaned Data into MySQL
Uses mysql-connector-python to insert the cleaned CSV into MySQL.
"""

import pandas as pd
import mysql.connector
import os


def get_connection(host, user, password, database=None):
    """Create a MySQL connection."""
    config = {
        'host': host,
        'user': user,
        'password': password,
    }
    if database:
        config['database'] = database
    return mysql.connector.connect(**config)


def create_database(host, user, password, database):
    """Create the database if it doesn't exist."""
    conn = get_connection(host, user, password)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Database '{database}' is ready.")


def create_table(conn):
    """Create the luxury_housing table."""
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS luxury_housing")
    cursor.execute("""
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
        )
    """)
    conn.commit()
    cursor.close()
    print("Table 'luxury_housing' created.")


def load_data(conn, csv_path):
    """Load cleaned CSV into MySQL table using batch inserts."""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)

    # Convert Purchase_Quarter to string date format for MySQL
    df['Purchase_Quarter'] = pd.to_datetime(
        df['Purchase_Quarter'], errors='coerce'
    ).dt.strftime('%Y-%m-%d')

    cursor = conn.cursor()

    insert_sql = """
        INSERT IGNORE INTO luxury_housing (
            Property_ID, Micro_Market, Project_Name, Developer_Name,
            Unit_Size_Sqft, Configuration, Ticket_Price_Cr, Transaction_Type,
            Buyer_Type, Purchase_Quarter, Connectivity_Score, Amenity_Score,
            Possession_Status, Sales_Channel, NRI_Buyer, Locality_Infra_Score,
            Avg_Traffic_Time_Min, Buyer_Comments, Price_per_Sqft,
            Quarter_Number, Quarter_Label, Booking_Flag
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    # Convert NaN to None for MySQL compatibility
    def to_python(val):
        if pd.isna(val):
            return None
        return val

    # Insert in batches
    batch_size = 5000
    rows = [tuple(to_python(v) for v in row) for row in df.values]
    total = len(rows)

    for i in range(0, total, batch_size):
        batch = rows[i:i + batch_size]
        cursor.executemany(insert_sql, batch)
        conn.commit()
        print(f"  Inserted {min(i + batch_size, total)}/{total} rows...")

    cursor.close()
    print("Data loaded successfully!")
    return total


def validate_data(conn):
    """Run basic validation queries."""
    cursor = conn.cursor()

    # Total count
    cursor.execute("SELECT COUNT(*) FROM luxury_housing")
    count = cursor.fetchone()[0]
    print(f"\nTotal records in table: {count}")

    # Possession status distribution
    cursor.execute(
        "SELECT Possession_Status, COUNT(*) as cnt "
        "FROM luxury_housing GROUP BY Possession_Status ORDER BY cnt DESC"
    )
    print("\nPossession Status Distribution:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")

    # Avg price per developer (top 5)
    cursor.execute(
        "SELECT Developer_Name, ROUND(AVG(Ticket_Price_Cr), 2) as avg_price "
        "FROM luxury_housing GROUP BY Developer_Name "
        "ORDER BY avg_price DESC LIMIT 5"
    )
    print("\nTop 5 Developers by Avg Ticket Price:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: ₹{row[1]} Cr")

    cursor.close()


def main():
    """Main function to load data into MySQL."""
    # MySQL connection details
    host = 'localhost'
    user = 'root'
    password = 'pass@123'
    database = 'luxury_housing_db'

    # File path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'Luxury_Housing_Cleaned.csv')

    # Check if cleaned file exists
    if not os.path.exists(csv_path):
        print("ERROR: Cleaned CSV not found. Run data_cleaning.py first.")
        return

    # Step 1: Create database
    create_database(host, user, password, database)

    # Step 2: Connect to database
    conn = get_connection(host, user, password, database)

    # Step 3: Create table
    create_table(conn)

    # Step 4: Load data
    rows_loaded = load_data(conn, csv_path)

    # Step 5: Validate
    validate_data(conn)

    # Cleanup
    conn.close()
    print(f"\nDone! {rows_loaded} rows loaded into {database}.luxury_housing")


if __name__ == '__main__':
    main()

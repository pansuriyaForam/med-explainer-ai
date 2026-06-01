import sqlite3
import pandas as pd
import os

def create_medicines_database(cleaned_csv='cleaned_medicine_data.csv', db_name='medicines.db'):
    """
    Create SQLite database from cleaned medicine data:
    - Create medicines table
    - Insert all records
    - Create indexes for fast searching
    - Validate data integrity
    """
    
    # Check if cleaned data exists
    if not os.path.exists(cleaned_csv):
        print(f"Error: {cleaned_csv} not found")
        print("Please run clean_data.py first")
        return
    
    print("📦 Loading cleaned medicine data...")
    df = pd.read_csv(cleaned_csv)
    
    # Remove existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Removed existing {db_name}")
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    print(f"🗄️  Creating SQLite database: {db_name}")
    
    # Create medicines table
    cursor.execute('''
        CREATE TABLE medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL UNIQUE,
            sub_category TEXT,
            salt_composition TEXT,
            product_price TEXT,
            product_manufactured TEXT,
            medicine_desc TEXT,
            side_effects TEXT,
            drug_interactions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    print("📝 Inserting medicine records...")
    
    # Insert data with error handling
    inserted_count = 0
    skipped_count = 0
    
    for index, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT INTO medicines 
                (product_name, sub_category, salt_composition, product_price, 
                 product_manufactured, medicine_desc, side_effects, drug_interactions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['product_name'],
                row['sub_category'],
                row['salt_composition'],
                row['product_price'],
                row['product_manufactured'],
                row['medicine_desc'],
                row['side_effects'],
                row['drug_interactions']
            ))
            inserted_count += 1
        except sqlite3.IntegrityError:
            # Skip duplicate entries
            skipped_count += 1
            continue
    
    print(f"✅ Records inserted: {inserted_count}")
    print(f"⏭️  Records skipped (duplicates): {skipped_count}")
    
    # Create indexes for faster searching
    print("🔍 Creating indexes...")
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_product_name 
        ON medicines(product_name)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sub_category 
        ON medicines(sub_category)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_salt_composition 
        ON medicines(salt_composition)
    ''')
    
    # Create full-text search index (for product name search)
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_product_name_search 
        ON medicines(product_name COLLATE NOCASE)
    ''')
    
    # Commit all changes
    conn.commit()
    
    # Validate data
    cursor.execute('SELECT COUNT(*) FROM medicines')
    total_medicines = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT sub_category) FROM medicines')
    total_categories = cursor.fetchone()[0]
    
    print(f"\n📊 Database Statistics:")
    print(f"Total medicines: {total_medicines}")
    print(f"Total categories: {total_categories}")
    
    # Show sample categories
    cursor.execute('''
        SELECT sub_category, COUNT(*) as count 
        FROM medicines 
        GROUP BY sub_category 
        ORDER BY count DESC 
        LIMIT 5
    ''')
    
    print("\nTop 5 categories:")
    for category, count in cursor.fetchall():
        print(f"  - {category}: {count} medicines")
    
    # Close connection
    conn.close()
    
    print(f"\n✨ Database created successfully: {db_name}")
    return db_name


if __name__ == '__main__':
    create_medicines_database()

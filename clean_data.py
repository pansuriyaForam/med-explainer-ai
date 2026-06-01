import pandas as pd
import os

def clean_medicine_data(input_file='medicine_data.csv', output_file='cleaned_medicine_data.csv'):
    """
    Clean medicine dataset:
    - Remove duplicates
    - Handle missing values
    - Standardize column names
    - Trim whitespace
    - Convert text to consistent format
    - Remove invalid entries
    """
    
    print("📋 Loading medicine data...")
    df = pd.read_csv("medicine_data.csv")
    
    print(f"Initial records: {len(df)}")
    
    # Step 1: Standardize column names (convert to snake_case)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Step 2: Strip whitespace from all string columns
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        df[col] = df[col].str.strip()
    
    # Step 3: Remove completely empty rows
    df = df.dropna(how='all')
    
    # Step 4: Handle missing values strategically
    # product_name is mandatory - drop rows without it
    df = df.dropna(subset=['product_name'])
    
    # Fill missing values with appropriate defaults
    df['sub_category'] = df['sub_category'].fillna('Uncategorized')
    df['salt_composition'] = df['salt_composition'].fillna('Not specified')
    df['product_price'] = df['product_price'].fillna('Price not available')
    df['product_manufactured'] = df['product_manufactured'].fillna('Manufacturer unknown')
    df['medicine_desc'] = df['medicine_desc'].fillna('No description available')
    df['side_effects'] = df['side_effects'].fillna('Consult doctor for side effects')
    df['drug_interactions'] = df['drug_interactions'].fillna('No known interactions')
    
    # Step 5: Clean price field - remove currency symbol
    df['product_price'] = df['product_price'].apply(
        lambda x: x.replace('₹', '').replace(',', '').strip() if isinstance(x, str) and x != 'Price not available' else x
    )
    
    # Step 6: Remove duplicate products (keep first occurrence)
    initial_count = len(df)
    df = df.drop_duplicates(subset=['product_name'], keep='first')
    duplicates_removed = initial_count - len(df)
    
    print(f"Duplicates removed: {duplicates_removed}")
    
    # Step 7: Remove rows with empty product_name after stripping
    df = df[df['product_name'].str.len() > 0]
    
    # Step 8: Normalize text fields (title case for names)
    df['product_name'] = df['product_name'].str.title()
    df['sub_category'] = df['sub_category'].str.title()
    df['salt_composition'] = df['salt_composition'].str.title()
    df['product_manufactured'] = df['product_manufactured'].str.title()
    
    # Step 9: Validate data integrity
    print(f"\n✅ Data validation:")
    print(f"Records with product name: {len(df[df['product_name'].notna()])}")
    print(f"Records with category: {len(df[df['sub_category'].notna()])}")
    print(f"Records with description: {len(df[df['medicine_desc'].notna()])}")
    
    print(f"\nFinal records: {len(df)}")
    
    # Step 10: Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"\n💾 Cleaned data saved to: {output_file}")
    
    return df


if __name__ == '__main__':
    if os.path.exists('medicine_data.csv'):
        clean_medicine_data()
    else:
        print("Error: medicine_data.csv not found")
        print("Make sure the file is in the current directory")

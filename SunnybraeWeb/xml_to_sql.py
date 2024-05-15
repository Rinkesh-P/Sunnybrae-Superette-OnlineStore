import os
import xml.etree.ElementTree as ET
import sqlite3

# Check if the XML file exists
file_path = 'data.xml'

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Connect to the existing SQLite database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS store_product (
             item_id INTEGER PRIMARY KEY,
             item_code TEXT,
             item_name TEXT,
             category_id INTEGER,
             current_price REAL)''')

# Function to get the text of an XML element or return an empty string if the element is None
def get_text(element):
    return element.text.strip() if element is not None and element.text else ''

# Function to convert text to an integer, defaulting to None if conversion fails
def convert_to_int(text):
    try:
        return int(text)
    except (ValueError, TypeError):
        return None

# Function to convert text to a float, defaulting to None if conversion fails
def convert_to_float(text):
    try:
        return float(text)
    except (ValueError, TypeError):
        return None

# Insert data into table with type conversions
for item in root.findall('tbl_Item'):
    item_id = convert_to_int(get_text(item.find('Item_ID')))
    item_code = get_text(item.find('Item_Code'))
    item_name = get_text(item.find('Item_Name'))
    category_id = convert_to_int(get_text(item.find('Category_ID')))
    current_price = convert_to_float(get_text(item.find('Current_Price')))
    
    # Skip insertion if item_id or category_id is None
    if item_id is None or category_id is None or current_price is None:
        print(f"Skipping record due to None value: {item_id}, {item_code}, {item_name}, {category_id}, {current_price}")
        continue

    data = (
        item_id,
        item_code,
        item_name,
        category_id,
        current_price
    )
    
    # Debugging: Print data to ensure it is being extracted and converted correctly
    #print("Extracted and converted data:", data)
    
    try:
        c.execute('''INSERT OR IGNORE INTO store_product (item_id, item_code, item_name, category_id, current_price) 
                     VALUES (?, ?, ?, ?, ?)''', data)
    except sqlite3.Error as e:
        print(f"Error inserting data {data}: {e}")

# Commit the changes 
conn.commit()

# Delete Records which have contain a 0 as the price
try:
    c.execute('DELETE FROM store_product WHERE current_price = 0')
    conn.commit()
except sqlite3.Error as e:
    print(f"Error deleting records with current_price 0: {e}")

# Close the Connection
conn.close()

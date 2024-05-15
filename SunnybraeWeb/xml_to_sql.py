import os
import xml.etree.ElementTree as ET
import sqlite3

# Print the current working directory
#print("Current working directory:", os.getcwd())

# Check if the XML file exists
file_path = 'data.xml'

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Connect to the existing SQLite database
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS ProductTable (
             Item_ID INTEGER PRIMARY KEY,
             Item_Code TEXT,
             Item_Name TEXT,
             Category_ID INTEGER,
             Current_Price REAL)''')

# Function to get the text of an XML element or return an empty string if the element is None
def get_text(element):
    return element.text if element is not None else ''

# Insert data into table
for item in root.findall('tbl_Item'):
    data = (
        get_text(item.find('Item_ID')),
        get_text(item.find('Item_Code')),
        get_text(item.find('Item_Name')),
        get_text(item.find('Category_ID')),
        get_text(item.find('Current_Price'))
    )
    
    # Debugging: Print data to ensure it is being extracted correctly
    # print("Extracted data:", data)
    
    c.execute('''INSERT OR IGNORE INTO ProductTable (Item_ID, Item_Code, Item_Name, Category_ID, Current_Price) 
                 VALUES (?, ?, ?, ?, ?)''', data)

# Commit the changes 
conn.commit()

#Delete Records which have contain a 0 as the price
c.execute('DELETE FROM ProductTable WHERE Current_Price = 0')

conn.commit()

# Close the Connection 
conn.close()

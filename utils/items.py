import pandas as pd
import csv
import os

# --- 1. Download necessary CSV files ---
print("Downloading community-listfile.csv...")
!wget -q https://github.com/wowdev/wow-listfile/releases/latest/download/community-listfile.csv
print("Downloading items.csv...")
!wget -q https://wago.tools/db2/Item/csv?build=2.5.6.68184 -O items.csv
print("Downloading itemsparse.csv...")
!wget -q https://wago.tools/db2/ItemSparse/csv?build=2.5.6.68184 -O itemsparse.csv

# --- 2. Extract and clean icon paths to create icons.csv ---
print("Processing community-listfile.csv to create icons.csv...")
with open('community-listfile.csv', mode='r', newline='') as infile, open('icons.csv', mode='w', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile)
    writer.writerow(['ID', 'ModifiedPath'])
    for row in reader:
        file_id = row[0]
        file_path = row[1]
        if 'interface/icons/' in file_path:
            modified_path = file_path.replace('interface/icons/', '').replace('.blp', '')
            writer.writerow([file_id, modified_path])
print("icons.csv created.")

# --- 3. Load DataFrames ---
print("Loading data into DataFrames...")
items_df = pd.read_csv('items.csv')
icons_df = pd.read_csv('icons.csv')
itemsparse_df = pd.read_csv('itemsparse.csv')

# --- 4. Merge DataFrames ---
# Merge items_df with icons_df
merged_df = pd.merge(items_df, icons_df, left_on='IconFileDataID', right_on='ID', how='left', suffixes=('_item', '_icon'))

# Select initial columns and rename the item ID
clean_icons_df = merged_df[['ID_item', 'ModifiedPath']].rename(columns={'ID_item': 'ID'})

# Merge with itemsparse_df to add Display_lang and OverallQualityID
clean_icons_df = pd.merge(clean_icons_df, itemsparse_df[['ID', 'Display_lang', 'OverallQualityID']], on='ID', how='left')
print("Initial DataFrame created.")

# --- 5. Rename columns ---
clean_icons_df = clean_icons_df.rename(columns={
    'ID': 'id',
    'ModifiedPath': 'icon',
    'Display_lang': 'name',
    'OverallQualityID': 'qua'
})
print("Columns renamed.")

# --- 6. Remove rows with NaN in 'name' or 'qua' ---
original_rows = len(clean_icons_df)
clean_icons_df.dropna(subset=['name', 'qua'], inplace=True)
removed_rows = original_rows - len(clean_icons_df)
print(f"Removed {removed_rows} rows due to NaN values in 'name' or 'qua'.")

# --- 7. Convert 'qua' to integer ---
# 'qua' should now be free of NaNs due to the previous dropna, so direct conversion is safe.
clean_icons_df['qua'] = clean_icons_df['qua'].astype(int)
print("'qua' column converted to integer.")

print("Final Clean Icons DataFrame Head:")
display(clean_icons_df.head())

# --- 8. Save the final DataFrame ---
clean_icons_df.to_json('items.json', orient='records', indent=4)
print("Final 'items.csv' and 'items.json' saved successfully.")

# Clean up downloaded files
print("Cleaning up temporary files...")
os.remove('community-listfile.csv')
os.remove('icons.csv')
os.remove('items.csv')
os.remove('itemsparse.csv')
print("Cleanup complete.")

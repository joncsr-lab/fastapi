import pandas as pd

def modify_rows(row):
    modified_rows = []
    modified_rows.append({
        'ID': row['ID'],
        'Item Tax Template (Taxes)': "Philippines Tax Exempt - ADC",
        'Tax Category (Taxes)': "Vat-In"
    })
    modified_rows.append({
        'ID': "",
        'Item Tax Template (Taxes)': "Senior Citizen Tax Ex",
        'Tax Category (Taxes)': "Senior Vat-Ex"
    })
    modified_rows.append({
        'ID': "",
        'Item Tax Template (Taxes)': "Zero Rated Ex - ADC",
        'Tax Category (Taxes)': "Zero Rated"
    })
    return modified_rows

# Load the CSV file
df = pd.read_csv('file.csv')  # Replace with your file name

# Apply the modify_rows function to each row in the original dataframe
new_rows = df.apply(modify_rows, axis=1).explode().reset_index(drop=True)

# Create a new DataFrame with the modified rows
df_modified = pd.DataFrame(new_rows.tolist())

# Save the modified DataFrame to a new CSV file
df_modified.to_csv('file3.csv', index=False)


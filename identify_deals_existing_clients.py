
import pandas as pd

# Read CSV file
pipewise = pd.read_csv("mapped_opportunities_file.csv")

# Select specific columns by their names
selected_columns = pipewise[['Deal ID', 'Deal Status', 'Created', 'Closed', 'Deal Age', 'Deal Size', 'Account ID', 'Has LeadSource']]

# Convert 'Created' column to datetime
selected_columns['Created'] = pd.to_datetime(selected_columns['Created'])

# Function to determine if an account is an existing client
def mark_existing_client(df):
    df = df.sort_values(by='Created')  # Ensure data is sorted by 'Created' date
    df['Existing Client'] = df['Account ID'].duplicated(keep='first')
    return df

# Apply the function to mark existing clients
selected_columns = mark_existing_client(selected_columns)

# Save the updated dataframe to a new CSV file if needed
selected_columns.to_csv("identify_deals_related_to_existing_clients.csv", index=False)

print("Data has been mapped and saved to 'updated_opportunities_file.csv'.")

# Display the updated dataframe
print(selected_columns.head())

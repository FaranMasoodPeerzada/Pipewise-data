import pandas as pd

# Read Csv file
df = pd.read_csv("opportunity_records_all_fields.csv")


#Select specific columns by their names
selected_columns = df[['Id','StageName','IsClosed','IsWon','CreatedDate','CloseDate','Amount','AccountId','Webactivity_Business_Unit__c']]



# # Convert 'CreatedDate' and 'CloseDate' to datetime objects
selected_columns.loc[:, 'CreatedDate'] = pd.to_datetime(selected_columns['CreatedDate'], format='%Y-%m-%dT%H:%M:%S.%f%z').dt.date
selected_columns.loc[:, 'CloseDate'] = pd.to_datetime(selected_columns['CloseDate'], format='%Y-%m-%d').dt.date

# Calculate 'Deal Age' as the difference in days between 'CloseDate' and 'CreatedDate'

selected_columns['Deal Age'] = (pd.to_datetime(selected_columns['CloseDate']) - pd.to_datetime(selected_columns['CreatedDate'])).dt.days
#selected_columns['Deal Age'] = pd.to_datetime(selected_columns['CloseDate']) - pd.to_datetime(selected_columns['CreatedDate'])

selected_columns['Deal Age'] = abs(selected_columns['Deal Age'])

# Update the 'Status' column based on conditions
selected_columns.loc[(selected_columns['StageName'] == 'Gesloten gewonnen') , 'Status'] = 'Won'
selected_columns.loc[(selected_columns['StageName'] == 'Gesloten verloren') , 'Status'] = 'Lost'
# Update the 'Status' column for all other values to 'Still Pending'
selected_columns.loc[~selected_columns['StageName'].isin(['Gesloten gewonnen', 'Gesloten verloren']), 'Status'] = 'Still Pending'

# Check 'Webactivity_Business_Unit__c' and update with True or False
selected_columns['Webactivity_Business_Unit__c'] = selected_columns['Webactivity_Business_Unit__c'].notna()


# Create a new DataFrame with the desired format
mapped_data = pd.DataFrame({
    'Deal ID': selected_columns['Id'],
    'Deal Status': selected_columns['Status'],
    'Created': selected_columns['CreatedDate'],
    'Closed': selected_columns['CloseDate'],
    'Deal Age': selected_columns['Deal Age'],
    'Deal Size': selected_columns['Amount'],
    'Account ID': selected_columns['AccountId'],
    'Has LeadSource': selected_columns['Webactivity_Business_Unit__c']
   
    })

mapped_data.to_csv('mapped_opportunities_file.csv', index=False)
print("Data has been mapped and saved to 'mapped_opportunities_file.csv'.")
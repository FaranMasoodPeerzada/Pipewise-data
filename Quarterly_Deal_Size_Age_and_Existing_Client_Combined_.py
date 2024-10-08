import pandas as pd

# Read CSV file
df = pd.read_csv("identify_deals_related_to_existing_clients.csv")

# Select specific columns by their names
selected_columns = df[['Deal ID', 'Deal Status', 'Created', 'Closed', 'Deal Age', 'Deal Size', 'Account ID', 'Has LeadSource','Existing Client']]

# Convert 'Created' and 'Closed' columns to datetime
selected_columns['Created'] = pd.to_datetime(selected_columns['Created'])
selected_columns['Closed'] = pd.to_datetime(selected_columns['Closed'])

# Create 'Quarter' column based on 'Created' date
selected_columns['Quarter'] = selected_columns['Created'].dt.to_period('Q').astype(str)
selected_columns['Quarter'] = selected_columns['Quarter'].apply(lambda x: f"{x[:4]} Q{x[5]}")

# Group by 'Quarter' and calculate counts of each deal status
quarterly_deal_age_stats = selected_columns.groupby('Quarter').agg(
    Count_of_Deals=('Deal ID', 'size'),
    Count_of_Won_Deals=('Deal Status', lambda x: (x == 'Won').sum()),
    Count_of_Lost_Deals=('Deal Status', lambda x: (x == 'Lost').sum()),
    Count_of_Still_Pending_Deals=('Deal Status', lambda x: (x == 'Still Pending').sum()),
    Average_of_Deal_Age=('Deal Age', 'mean'),
    Median_of_Deal_Age=('Deal Age', 'median'),
    Percentile_5th_of_Deal_Age= ('Deal Age', lambda x: x.quantile(0.05)),
    Percentile_25th_of_Deal_Age= ('Deal Age', lambda x: x.quantile(0.25)),
    Percentile_75th_of_Deal_Age= ('Deal Age', lambda x: x.quantile(0.75)),
    Percentile_95th_of_Deal_Age= ('Deal Age', lambda x: x.quantile(0.95))


    
).reset_index()


# Filter for Won deals
won_deals = selected_columns[selected_columns['Deal Status'] == 'Won']


# Group by 'Quarter' and Calculate statistics for Deal Size
quarterly_deal_size_stats  = won_deals.groupby('Quarter').agg(
    Average_of_Deal_Size=('Deal Size', 'mean'),
    Median_of_Deal_Size=('Deal Size', 'median'),
    Percentile_5th_of_Deal_Size= ('Deal Size', lambda x: x.quantile(0.05)),
    Percentile_25th_of_Deal_Size= ('Deal Size', lambda x: x.quantile(0.25)),
    Percentile_75th_of_Deal_Size= ('Deal Size', lambda x: x.quantile(0.75)),
    Percentile_95th_of_Deal_Size= ('Deal Size', lambda x: x.quantile(0.95))


    
).reset_index()




# Calculate percentages
quarterly_deal_age_stats['% of Won Deals'] = (quarterly_deal_age_stats['Count_of_Won_Deals'] / quarterly_deal_age_stats['Count_of_Deals']) * 100
quarterly_deal_age_stats['% of Lost Deals'] = (quarterly_deal_age_stats['Count_of_Lost_Deals'] / quarterly_deal_age_stats['Count_of_Deals']) * 100
quarterly_deal_age_stats['% of Still Pending Deals'] = (quarterly_deal_age_stats['Count_of_Still_Pending_Deals'] / quarterly_deal_age_stats['Count_of_Deals']) * 100



# Calculate percentage of Won Deals with LeadSource
# Create a DataFrame to store LeadSource info
leadsource_df = selected_columns[selected_columns['Deal Status'] == 'Won']

# Group by 'Quarter' and calculate counts of Won Deals with LeadSource
won_leadsource_stats = leadsource_df.groupby('Quarter').agg(
    Count_of_Won_Deals_With_LeadSource=('Has LeadSource', lambda x: (x == True).sum())
).reset_index()

# Merge the two DataFrames to include the LeadSource percentages
quarterly_deal_age_stats = pd.merge(quarterly_deal_age_stats, won_leadsource_stats, on='Quarter', how='left')
quarterly_deal_age_stats['% Deal Won With LeadSource'] = (quarterly_deal_age_stats['Count_of_Won_Deals_With_LeadSource'] / quarterly_deal_age_stats['Count_of_Won_Deals']) * 100

# Drop the intermediate columns used for calculations
quarterly_deal_age_stats.drop(columns=['Count_of_Won_Deals_With_LeadSource'], inplace=True)








# Format percentage and deal age statistics columns to show as numeric with 2 decimal places
quarterly_deal_age_stats['% of Won Deals'] = quarterly_deal_age_stats['% of Won Deals'].round(2)
quarterly_deal_age_stats['% of Lost Deals'] = quarterly_deal_age_stats['% of Lost Deals'].round(2)
quarterly_deal_age_stats['% of Still Pending Deals'] = quarterly_deal_age_stats['% of Still Pending Deals'].round(2)
quarterly_deal_age_stats['% Deal Won With LeadSource'] = quarterly_deal_age_stats['% Deal Won With LeadSource'].round(2)
quarterly_deal_age_stats['Average_of_Deal_Age'] = quarterly_deal_age_stats['Average_of_Deal_Age'].round(2)
quarterly_deal_age_stats['Median_of_Deal_Age'] = quarterly_deal_age_stats['Median_of_Deal_Age'].round(2)
quarterly_deal_age_stats['Percentile_5th_of_Deal_Age'] = quarterly_deal_age_stats['Percentile_5th_of_Deal_Age'].round(2)
quarterly_deal_age_stats['Percentile_25th_of_Deal_Age'] = quarterly_deal_age_stats['Percentile_25th_of_Deal_Age'].round(2)
quarterly_deal_age_stats['Percentile_75th_of_Deal_Age'] = quarterly_deal_age_stats['Percentile_75th_of_Deal_Age'].round(2)
quarterly_deal_age_stats['Percentile_95th_of_Deal_Age'] = quarterly_deal_age_stats['Percentile_95th_of_Deal_Age'].round(2)


quarterly_deal_size_stats['Average_of_Deal_Size'] = quarterly_deal_size_stats['Average_of_Deal_Size'].round(2)
quarterly_deal_size_stats['Median_of_Deal_Size'] = quarterly_deal_size_stats['Median_of_Deal_Size'].round(2)
quarterly_deal_size_stats['Percentile_5th_of_Deal_Size'] = quarterly_deal_size_stats['Percentile_5th_of_Deal_Size'].round(2)
quarterly_deal_size_stats['Percentile_25th_of_Deal_Size'] = quarterly_deal_size_stats['Percentile_25th_of_Deal_Size'].round(2)
quarterly_deal_size_stats['Percentile_75th_of_Deal_Size'] = quarterly_deal_size_stats['Percentile_75th_of_Deal_Size'].round(2)
quarterly_deal_size_stats['Percentile_95th_of_Deal_Size'] = quarterly_deal_size_stats['Percentile_95th_of_Deal_Size'].round(2)


# Calculate percentage of Won Deals with LeadSource
# Create a DataFrame to store LeadSource info
existing_client_won_deals = selected_columns[(selected_columns['Deal Status'] == 'Won') & (selected_columns['Existing Client'] == True)]

# Group by 'Quarter' and calculate counts of Won Deals with LeadSource
won_existing_client_stats = existing_client_won_deals.groupby('Quarter').agg(
    Count_of_Won_Deals_With_existing_client=('Existing Client', lambda x: (x == True).sum())
).reset_index()

# Merge the two DataFrames to include the LeadSource percentages
quarterly_deal_age_stats = pd.merge(quarterly_deal_age_stats, won_existing_client_stats, on='Quarter', how='left')

quarterly_deal_age_stats['% Of Won Deals With Existing Client'] = (quarterly_deal_age_stats['Count_of_Won_Deals_With_existing_client'] / quarterly_deal_age_stats['Count_of_Won_Deals']) * 100

# Drop the intermediate columns used for calculations
quarterly_deal_age_stats.drop(columns=['Count_of_Won_Deals_With_existing_client'], inplace=True)


# Debugging: Print counts before merging
print("Won Deals per Quarter:")
print(quarterly_deal_age_stats[['Quarter', 'Count_of_Won_Deals']])

print("\nWon Deals with Existing Client per Quarter:")
print(won_existing_client_stats)



# Round the new percentage column to 2 decimal places
quarterly_deal_age_stats['% Of Won Deals With Existing Client'] = quarterly_deal_age_stats['% Of Won Deals With Existing Client'].round(2)



# Debugging: Print the computed percentages
print("\n% Of Won Deals With Existing Client:")
print(quarterly_deal_age_stats['% Of Won Deals With Existing Client'])
# Merge the Deal Age and Deal Size statistics
quarterly_deal_stats = pd.merge(quarterly_deal_age_stats, quarterly_deal_size_stats, on='Quarter')

# Rename columns to remove underscores and capitalize properly
quarterly_deal_stats.columns = [
    'Quarter',
    'Count Of Deals',
    'Count Of Won Deals',
    'Count Of Lost Deals',
    'Count Of Still Pending Deals',
    'Average Of Deal Age',
    'Median Of Deal Age',
    '5Th Percentile Of Deal Age',
    '25Th Percentile Of Deal Age',
    '75Th Percentile Of Deal Age',
    '95Th Percentile Of Deal Age',
    '% Of Won Deals',
    '% Of Lost Deals',
    '% Of Still Pending Deals',
    '% Deal Won With Leadsource',
    '% Of Won Deals With Existing Client',
    'Average Of Deal Size',
    'Median Of Deal Size',
    '5Th Percentile Of Deal Size',
    '25Th Percentile Of Deal Size',
    '75Th Percentile Of Deal Size',
    '95Th Percentile Of Deal Size'
    
    
]

# Save the DataFrame to a CSV file
quarterly_deal_stats.to_csv('Quarterly_Deal_Size_Age_and_Existing_Client_Combined_Table.csv', index=False)
print("Data has been mapped and saved to 'Quarterly Stats Table.csv'.")

# Display the updated DataFrame
print(quarterly_deal_stats.head())
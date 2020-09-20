import pandas as pd
import numpy as np


# Read data
raw_data = pd.read_csv('olx.csv')


# raw data contains rows with all null
# many unrelated data other than cars are present 
# Column with urls, item title and description has to be removed
# Price is in string format with rupees symbol
# distance driven is in string format
# 


# Clean up useless null rows
raw_data = raw_data[raw_data['value_make']!='-1']

# Removing irrelevant brands
raw_data = raw_data[~raw_data['value_make'].isin(['Ashok Leyland', 'Bharat Benz', 'Eicher', 'New Holland',
                                                'Force Motors Ltd', 'John Deere', 'Mi', 'Lenovo', 'Motorola', 'Asus',
                                                'Realme', 'Nokia', 'Other Mobiles', 'Samsung', 'KTM', 
                                                'John Deere','SML', 'Messey Ferguson', 'Others', 'Other Brands',
                                                'Premier', 'Piaggio', 'TAFE', 'TATA Motors'])]

# removing unnecessary columns
raw_data = raw_data.drop(['link', ], axis=1)

# Converting price as integer
raw_data['itemPrice'] = raw_data['itemPrice'].apply(lambda x: int(x[2:].replace(',', '')))

# Converting distance driven in to integer
raw_data['value_mileage'] = raw_data['value_mileage'].apply(lambda x: int(x.split(' ')[0].replace(',', '')))

# replacing -1 with Nan
raw_data.replace('-1', np.nan, inplace=True)

# splitting place data into 3 seperate columns and appending them to raw_data
place = raw_data['itemLocation'].str.split(',', expand=True)
place = place.rename(columns = {0: 'locality',1: 'district', 2: 'State'})
raw_data = pd.concat([raw_data, place], axis=1)
raw_data = raw_data.drop(['itemLocation'], axis=1)

raw_data.to_csv("data_cleaned.csv", index=False, header=True)

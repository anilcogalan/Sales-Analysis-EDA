import pandas as pd
import os
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter(action='ignore', category=Warning)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.max_rows', None)

# all csv files in a file

all_months_data = pd.DataFrame()

files = [file for file in os.listdir("./Sales_Data")]

for file in files:
    df = pd.read_csv("./Sales_Data/" + file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv("all_data.csv", index=False)

all_data = pd.read_csv("all_data.csv")
all_data.head()

# data cleaning

nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()
all_data = all_data.dropna(how='all')
all_data.head()

all_data = all_data[all_data["Order Date"].str[0:2] != 'Or']

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()
all_data.tail()

# convert columns to the correct type

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

# Add a sales column

all_data['sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()

# What was the best month for sales? How much was earned that month?

results = all_data.groupby("Month").sum()

months = range(1, 13)

plt.bar(months, results['sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# What city had the highest number of sales?

def get_city(address):
    return address.split(',')[1]


def get_state(address):
    return address.split(',')[2].split(' ')[1]


all_data['city'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
all_data.head()

results = all_data.groupby('city').sum()
results

cities = [city for city, df in all_data.groupby('city')]
print(cities)

# cities1 = all_data['city'].unique()  #değerler sıralı gelmiyor fakat aşağıda cities, results['sales'] yaptığımızda, .unique() aldığımızda resulttaki gibi sıralı olmuyor.
# print(cities1)

plt.bar(cities, results['sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City Name')
plt.show()

# What time should we display advertisements to maximize likelihood of costumer's buying product?

all_data.head()

all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

all_data['hour'] = all_data['Order Date'].dt.hour
all_data['minute'] = all_data['Order Date'].dt.minute
all_data.head()

hours = [hour for hour, df in all_data.groupby('hour')]

plt.plot(hours, all_data.groupby(['hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()

# What products are most often sold together?

df = all_data[all_data['Order ID'].duplicated(keep=False)]

# df.head(20)

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()

from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key, value)

# What product sold the most? Why do you think it sold the most?

product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]

plt.bar(products, quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.xticks(products, rotation='vertical', size=8)
plt.tight_layout()
plt.show()

prices = all_data.groupby('Product').mean()['Price Each']

fig, ax = plt.subplots()

ax2 = ax.twinx()
ax.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, 'b-')

ax.set_xlabel('Product Name')
ax.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price', color='b')
ax.set_xticklabels(products, rotation='vertical', size=8)
plt.tight_layout()
plt.show()

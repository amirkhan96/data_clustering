import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import math

segmentation = pd.read_excel('technology_sale.xls')
segmentation = segmentation.replace(0, np.nan)
segmentation = segmentation.replace(0.0, np.nan)

# calulate growth 
growth = list()
growth_defferent_year = list()
average_growth_rate = list()
for i in range(0, segmentation.shape[0]):
    
    earlier_sale = 0
    latest_sale = 0
    
    earlier_year = 0
    latest_year = 0
    
    # calculate start date
    for start_year in range(1988, 2012):
        year = str(start_year)
        if not math.isnan(segmentation.loc[i, year]):
            earlier_sale = segmentation.loc[i, year]
            earlier_year = start_year
            break
    # calculate latest data
    for finish_data in range(2012, 1989, -1):
        year = str(finish_data)
        if not math.isnan(segmentation.loc[i, year]):
            latest_sale = segmentation.loc[i, year]
            latest_year = finish_data
            break
            
    if not math.isnan(earlier_sale) and  earlier_sale != 0:
        growth.append((latest_sale - earlier_sale) / earlier_sale)
        growth_defferent_year.append(latest_year - earlier_year)
        average_growth_rate.append(growth[i] / growth_defferent_year[i])
    else:
        growth.append(np.nan)
        growth_defferent_year.append(np.nan)
        average_growth_rate.append(np.nan)

segmentation['growth rate'] = growth
segmentation['growth rate per year'] = average_growth_rate

segmentation = segmentation.sort_values(by=['growth rate per year'])
segmentation = segmentation.dropna(subset=['growth rate per year'])

segmentation.index = pd.RangeIndex(start=0, stop=segmentation.shape[0], step=1)

# Because countris (Belize,Turkmenistan) are very different against other countries we delete them
segmentation = segmentation.loc[:200, :]

filter_data = segmentation.dropna(subset=['growth rate'])
filter_data = segmentation.dropna(subset=['growth rate per year'])

clustering_filter_data = filter_data.filter(items=['growth rate per year'])

model_fit = KMeans(n_clusters=4).fit(clustering_filter_data)
cluster_list = model_fit.predict(clustering_filter_data)

filter_data['cluster code'] = cluster_list

empty_list = list()
for i  in range(0, filter_data.shape[0]):
    empty_list.append(0)


plt.figure(figsize=(15,9))
plt.scatter(filter_data.loc[:, 'growth rate per year'], empty_list,c=cluster_list, s=50, cmap='viridis')
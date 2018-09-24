import os
import json
import time
import python_http_client
import pandas as pd
from pandas.io.json import json_normalize

# initialize client
with open(os.path.join(os.path.realpath('/Users/fronk/.creds'), 'sendgrid_creds.json'), 'r') as f:
    config = json.load(f)
api_key = config['key']
host = 'https://api.sendgrid.com'
request_headers = {'Authorization': 'Bearer {0}'.format(api_key)}
version = 3
client = python_http_client.Client(
	host=host,
	request_headers=request_headers,
	version=version
)

# get all categories
category_list = pd.DataFrame(eval(client.categories.get().body))['category'].tolist()

# get stats loop
results = []
for c in category_list:

	# set parameters
	params = {
		'start_date': '2018-09-01', 
		'end_date': '2018-09-21', 
		'aggregated_by': 'month', 
		'limit': 1,
		'offset': 1
	}
	params['categories'] = c

	# grab data
	df = pd.DataFrame(eval(client.categories.stats.get(query_params=params).body))

	# clean up to dataframe
	date_col = pd.to_datetime(df['date']).reset_index(0)
	stats = json_normalize(df['stats'].apply(lambda x: x[0])).reset_index(0)
	final = date_col.merge(stats, on='index', how='inner')
	final = final[['name', 'date', 'metrics.clicks', 'metrics.opens', 'metrics.unique_clicks', 'metrics.unique_opens', 'metrics.delivered']]
	final['ctr'] = final['metrics.unique_clicks'] / final['metrics.unique_opens']
	final['read_rate'] = final['metrics.unique_opens'] / final['metrics.delivered']
	results.append(final)
	time.sleep(2)

# concat and save final results
final_result = pd.concat(results)
final_result = final_result.sort_values(['ctr'], ascending=False)	
final_result.to_csv('email_performance.csv')

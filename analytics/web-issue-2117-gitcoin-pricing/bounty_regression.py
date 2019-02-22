import pandas as pd
import numpy as np
from sklearn import linear_model

# load
df = pd.read_csv('bounty_features.csv')

# clean
df = df[
    (df['bounty_type'] != 'Andere') &
    (df['project_length_category'] != 'Tage') &
    (df['experience_level'] != 'Mittlere')
]

# descriptive stats
ds = df
ds.loc[:, 'hourly_rate_distribution'] = ds['value_in_usdt'] / ds['fulfiller_hours_worked']
ds = ds[[
    'time_alloted_days', 'time_to_bounty_start_days', 'time_to_bounty_completion_days',
    'bounty_type', 'project_length_category', 'experience_level',
    'value_in_usdt', 'value_usd_db', 'value_in_usdt_now', 'hourly_rate_distribution'
]]

ds.groupby('bounty_type')['value_in_usdt'].median()
ds.groupby('project_length_category')['value_in_usdt'].median()
ds.groupby('experience_level')['value_in_usdt'].median()

# bounty_type
# Bug               49.920
# Code Review       37.865
# Documentation    121.660
# Feature           95.265
# Improvement      105.220
# Other             60.000
# Security          72.370

# project_length_category
# Days       145.805
# Hours       66.885
# Months     143.260
# Unknown     91.240
# Weeks      149.400

# experience_level
# Advanced        166.340
# Beginner         37.590
# Intermediate    103.425

# dummy-ize and clean
ddf = pd.get_dummies(df)
ddf = ddf.fillna(0)  # does this affect the regression?

# remove outliers
conts = [
    'time_alloted_days',
    'time_to_bounty_start_days',
    'time_to_bounty_completion_days',
    'fulfiller_hours_worked'
]
ddf[conts].mean()
ddf[conts].median()

ddf = ddf[
    (ddf['time_alloted_days'] < 400) &  # 3 removed
    (ddf['time_to_bounty_start_days'] < 150)  # 1 removed
]

# create features
ddf.loc[:, 'hourly_rate_distribution'] = ddf['value_in_usdt'] / ddf['fulfiller_hours_worked']

# filter features
ddf = ddf[ddf['fulfiller_hours_worked'] > 0]

# select features
ddf = ddf[
    [
        'time_alloted_days',
        'time_to_bounty_start_days',
        'time_to_bounty_completion_days',
        # 'fulfiller_hours_worked',
        # 'accepted',
        # 'num_fulfillments',
        # 'payout_token_AION',
        # 'payout_token_ANT',
        # 'payout_token_AVO',
        # 'payout_token_CLN',
        # 'payout_token_DAI',
        # 'payout_token_DAT',
        # 'payout_token_ETH',
        # 'payout_token_LPT',
        # 'payout_token_MANA',
        # 'payout_token_TUSD',
        # 'payout_token_WYV',
        # 'payout_token_ZRX',
        # 'project_type_contest',
        # 'project_type_cooperative',
        # 'project_type_traditional',
        # 'permission_type_approval',
        # 'permission_type_permissionless',
        'bounty_type_Bug',
        'bounty_type_Code Review',
        'bounty_type_Documentation',
        'bounty_type_Feature',
        'bounty_type_Improvement',
        'bounty_type_Other',
        'bounty_type_Security',
        'project_length_category_Days',
        'project_length_category_Hours',
        'project_length_category_Months',
        'project_length_category_Unknown',
        'project_length_category_Weeks',
        'experience_level_Advanced',
        'experience_level_Beginner',
        'experience_level_Intermediate',
        # 'meta_status_abandoned',
        # 'meta_status_at risk',
        # 'meta_status_cancelled',
        # 'meta_status_done',
        # 'meta_status_expired',
        # 'meta_status_in progress',
        # 'meta_status_open',
        # 'meta_status_stale',
        # 'meta_status_submitted',
        'value_in_usdt',
        'value_usd_db',
        'value_in_usdt_now',
        'hourly_rate_distribution'
    ]
]

# feature prep
features = np.array(
    ddf.drop(
        ['value_in_usdt_now', 'value_in_usdt', 'value_usd_db', 'hourly_rate_distribution'],
        axis=1
    )
)

response = np.array(ddf['value_in_usdt'])
# response = np.array(ddf['hourly_rate_distribution'])
# response = np.array(ddf['value_in_usdt_now'])
# response = np.array(ddf['value_usd_db'])

# regression
reg = linear_model.LinearRegression()
reg.fit(features, response)

# results
drop_cols = ['value_in_usdt_now', 'value_in_usdt', 'value_usd_db', 'hourly_rate_distribution']
for idx, feature_name in enumerate(ddf.drop(drop_cols, axis=1).columns):
    print('feature: {}, coeff: {}'.format(feature_name, reg.coef_[idx]))

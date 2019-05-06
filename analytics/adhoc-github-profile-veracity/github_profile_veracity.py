import pandas as pd 
import numpy as np
from pandas.io.json import json_normalize
import os, requests, json, time
from github import Github


def handle_check(github_instance, _filename):
    """
    Checks veracity of Github handles
    @input: github instance and details csv (https://metabase.gitcoin.co/question/383), filename in user downloads folder
    @output: results with status column
    """
    df_dir = os.path.join(os.path.expanduser('~'),'Downloads', _filename)
    df = pd.read_csv(df_dir)
    # handles = [x.lower() for x in ['frankchen07', 'nemris']]
    handles = [x.lower() for x in list(set(df.handle))]
    handle_dict = {}
    for handle in handles:
        handle_dict[handle] = [i.login.lower() for i in github_instance.search_users(handle)]
        time.sleep(1)
    results = pd.DataFrame(handle_dict.items())
    results.columns = ['handle', 'query'] 
    results.loc[:, 'ghp_veracity'] = results.apply(
        lambda x: True if len([i for i in x['query'] if x['handle'] == i]) > 0 else False, axis=1
    )
    final = pd.merge(df, results, on='handle', how='left')
    return final


def initialize_github():
    """
    Initializes the Github API
    @input: none
    @output: github instance
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.creds')
    with open(os.path.join(credential_dir, 'github_pat.json')) as f:
        creds = json.load(f)
    token = creds['token']
    g = Github(token)
    return g


if __name__ == "__main__":
    g = initialize_github()
    r = handle_check(g, 'gitcoin_clr_2_details.csv')
    print r.head()
    r.to_csv('gitcoin_clr_2_details_gh_check.csv')

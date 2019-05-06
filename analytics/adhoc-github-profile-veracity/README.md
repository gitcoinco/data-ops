### github profile veracity

1. a crendentials file is necessary to run this script
2. `cd ~`
3. `mkdir .creds`
4. `touch github_pat.json`

```
{
    "token": "YOUR_GITHUB_TOKEN"
}
```

5. go to https://metabase.gitcoin.co/question/38 and download a csv
6. name it `gitcoin_clr_2_details.csv`, and place it in `~/Downloads`
7. `python github_profile_veracity.py`
8. returns a csv with github profile veracity
9. runtime could be improved


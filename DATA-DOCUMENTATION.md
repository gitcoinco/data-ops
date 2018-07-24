# Data Documentation 

## Schemas

Data schemas can be found in `models.py` for each Django app in [gitcoinco/web/app](https://github.com/gitcoinco/web/tree/master/app). Some commonly used ones are found below.

1. [Dashboard Bounty](https://github.com/gitcoinco/web/blob/master/app/dashboard/models.py#L156-L220)

2. [Dashboard Bounty Fulfillment](https://github.com/gitcoinco/web/blob/master/app/dashboard/models.py#L802-L811)

3. [Dashboard Bounty Tip](https://github.com/gitcoinco/web/blob/master/app/dashboard/models.py#L867-L894)

4. [Dashboard Activity](https://github.com/gitcoinco/web/blob/master/app/dashboard/models.py#L1097-L1116)

5. [Dashboard Profile](https://github.com/gitcoinco/web/blob/master/app/dashboard/models.py#L1135-L1162)

6. [Dashboard User Action](https://github.com/gitcoinco/web/blob/master/app/dashboard/models.py#L1943-L1955)

7. [Marketing Email Subscribers](https://github.com/gitcoinco/web/blob/master/app/marketing/models.py#L48-L62)

8. [Marketing Slack Users](https://github.com/gitcoinco/web/blob/master/app/marketing/models.py#L210-L216)

9. [Auth User]()

## Data Tips

1. When working with `dashboard_bounty`, you'll universally want to apply `current_bounty=True`, except if you're working with historical snapshots.

2. When working with `dashboard_bounty`, constraining `idx_status` to a subset of `open`, `started`, `submitted`, and `done` is most accurate. 

3. When working with `auth_user`, some filters to keep in mind to grab current and active (but not in the sense of engagement) are `active_user=True`, `is_staff=False`, and adjusting `date_joined` and `last_login` to ensure you are getting legitimate accounts.

4. When working with `dashboard_bounty`, the timeline flow is generally `web3_created` -> `created_on` -> `fulfillment_started_on` -> `fulfillment_submitted_on` -> `fulfillment_accepted_on`. The `web3_created` time and `created_on` time should be similar (within 30 minutes)

5. When working with `dashboard_bounty`, `_val_usd_db` is the value at the time of bounty creation in USDT, `value_in_usdt_now` is the value now. (What about `value_in_usdt`?)

6. The `dashboard_bountyfulfillment` table contains fulfillment addresses and information on the user who is fulfilling a bounty.


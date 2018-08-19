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

Generally, if you have access to Metabase, check out how each metric is composed to get an understanding of what each Gitcoin table is used for. Additional tips below!

1. When working with `dashboard_bounty`, you'll universally want to apply `current_bounty=True`, except if you're working with historical snapshots.

2. When working with `dashboard_bounty`, constraining `idx_status` to a subset of `open`, `started`, `submitted`, and `done` is most accurate. 

3. When working with `auth_user`, some filters to keep in mind to grab current and active (but not in the sense of engagement) are `active_user=True`, `is_staff=False`, and adjusting `date_joined` and `last_login` to ensure you are getting legitimate accounts.

4. When working with `dashboard_bounty`, the timeline flow is generally `web3_created` -> `created_on` -> `fulfillment_started_on` -> `fulfillment_submitted_on` -> `fulfillment_accepted_on`. The `web3_created` time and `created_on` time should be similar (within 30 minutes).

5. When working with `dashboard_bounty`, `_val_usd_db` is the value at the time of bounty creation in USDT, `value_in_usdt_now` is the value now. **What about `value_in_usdt`?**

6. The `dashboard_bountyfulfillment` table contains fulfillment addresses and information on the user who is fulfilling a bounty.

7. `dashboard_interest` denotes that a bounty has been started. **How does this compare with "started" on `dashboard_bounty`?**

8. In `marketing_stat`, an "active" Slack user is someone who is online now (at the `created_on` time)

9. In `marketing_stat` for twitter related `key`s the difference between `twitter_followers` and `twitter_followers_gitcoinfeed` is the former is the main account (getgitcoin) and the latter is a firehose gitcoinfeed account.

10. In `marketing_stat`, an active email subscriber is someone who has not unsubscribed, compared to a regular email subscriber.

11. In `marketing_stat`, there may be data loss for particular keys from end of January to March 1st due to production pushes.

12. In `auth_users`, we may not have join information before April, taking a look at `dashboard_profile` might be useful.

13. `dashboard_profile` was in use before `auth_user`, there might be a need to port a `joined_date` to `auth_user`

14. The rules for open bounties are different for traditional bounties versus competitive and contest bounties (which stay open no matter how many fulfillments).

```sql
select
    *
from 
    (select db.id, db.created_on, db.fulfillment_started_on, db.idx_status from dashboard_bounty db where db.idx_status = 'open') a
left join (
    select dbf.profile_id, dbf.bounty_id, dbf.fulfiller_address, dbf.created_on fulfilled_on from dashboard_bountyfulfillment dbf
) b
on 
    a.id = b.bounty_id 
where
    a.id in (4453, 3855, 1087, 3519)
;
```

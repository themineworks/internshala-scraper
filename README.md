# Internshala Scraper: Internships & Fresher Jobs, No Login

Scrape Internshala's internships, jobs, and fresher-job boards: title, company, stipend/salary parsed to numbers, duration, skills, location, and posting date. Location, stipend, and duration filters are applied server-side. No login, no browser required.

**Run it on Apify:** [apify.com/themineworks/internshala-jobs-scraper](https://apify.com/themineworks/internshala-jobs-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/internshala-jobs-scraper](https://themineworks.com/actors/internshala-jobs-scraper/)

**Price:** From $1.20 per 1,000 listings on Apify's higher plans ($2.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Covers all three boards: internships, jobs, and fresher jobs
* Stipend/salary parsed into numeric min/max and unit
* Server-side filters: location, WFH, part-time, stipend, duration
* Monitor mode bills only for listings posted since last run
* No login, no captcha, no browser

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/internshala-jobs-scraper").call(run_input={
    "searchKeywords": [
        "digital marketing"
    ],
    "category": "digital-marketing",
    "location": "bangalore"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/internshala-jobs-scraper').call({
    "searchKeywords": [
        "digital marketing"
    ],
    "category": "digital-marketing",
    "location": "bangalore"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~internshala-jobs-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchKeywords": ["digital marketing"], "category": "digital-marketing", "location": "bangalore"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 internshala_scraper.py --token YOUR_APIFY_TOKEN --search-keywords "digital marketing" --category "digital-marketing" --location "bangalore"
node internshala_scraper.mjs --token YOUR_APIFY_TOKEN --search-keywords "digital marketing" --category "digital-marketing" --location "bangalore"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `searchKeywords` | array |  | One or more free-text keywords (role, skill or company), for example 'digital marketing', 'python' |
| `employmentType` | string | `"internship"` | Which Internshala board to search |
| `category` | string |  | Internshala profile/category slug, for example 'computer-science', 'digital-marketing', 'human-resources'… |
| `location` | string |  | City name, for example 'bangalore', 'mumbai', 'delhi', 'pune' |
| `workFromHome` | boolean | `false` | Only return remote / work-from-home listings |
| `partTime` | boolean | `false` | Only return part-time listings |
| `maxResults` | integer | `5` | Maximum number of listings to scrape across all keywords |
| `includeDescription` | boolean | `false` | If true, include the full listing description text |
| `monitorMode` | boolean | `false` | Run on a schedule and deliver ONLY results not seen in a previous run |
| `stipendMin` | integer |  | Minimum monthly stipend in INR for internships, or minimum annual salary in INR for jobs |
| `durationMaxMonths` | integer |  | Only for internships |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `listing_id` | string | Internshala internal listing ID |
| `employment_type` | string | internship, job, or fresher_job |
| `title` | string | Listing title |
| `company` | string | Company name |
| `company_logo` | string | Company logo image URL |
| `actively_hiring` | boolean | Whether Internshala shows the 'Actively hiring' badge |
| `location` | string | Location text as shown on the listing (city name(s) or 'Work from home') |
| `work_from_home` | boolean | True if the listing is remote / work from home |
| `compensation_text` | string | Raw stipend (internship) or salary (job) string from Internshala |
| `compensation_min_inr` | number | Minimum stipend/salary in INR |
| `compensation_max_inr` | number | Maximum stipend/salary in INR |
| `compensation_unit` | string | month (internship stipend), year (job/fresher_job salary), or lump_sum |
| `is_unpaid` | boolean | True if the internship is explicitly marked Unpaid |
| `duration_text` | string | Raw internship duration text (for example '6 Months') |
| `duration_months` | number | Internship duration normalised to months |
| `experience_text` | string | Raw experience requirement text |
| `experience_min_years` | number | Minimum years of experience required |
| `experience_max_years` | number | Maximum years of experience required |
| `skills` | array | Required skills list |
| `description` | string | Listing description text (truncated to 400 chars unless includeDescription=true) |
| `apply_url` | string | URL to the Internshala listing detail / apply page |
| `posted_text` | string | Raw posted-time text from Internshala (for example '5 days ago', 'Few hours ago') |
| `posted_days_ago` | number | Approximate number of days since the listing was posted |
| `scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/internshala-jobs-scraper
```

## FAQ

### Does it log in to Internshala?

No. The actor works from public search endpoints only. No account, no cookies, no captcha.

### Why do some listings show Unpaid with no numeric stipend?

Internshala allows unpaid internships. is_unpaid is set to true and the numeric stipend fields are omitted rather than set to zero.

### Can I search jobs and fresher jobs, not just internships?

Yes. Set employmentType to job or fresher_job. Those carry an experience band instead of a duration field.

### What does monitor mode do?

Remembers every listing_id delivered under the same input, so a scheduled run charges only for listings posted since the last one.

### Can I use it in an AI agent?

Yes. It's exposed as an MCP tool.

### Which filters run server side?

Location, work from home, part time, stipend and duration. They are applied by Internshala before results come back, so you are not billed for rows you would discard.

### How much does the Internshala Scraper cost?

From $1.20 per 1,000 listings on Apify's higher plans ($2.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Foundit Jobs Scraper](https://themineworks.com/actors/foundit-jobs-scraper/): Foundit.in (Monster India): 20 fields, monitor mode
* [Hirist Jobs Scraper](https://themineworks.com/actors/hirist-jobs-scraper/): India IT jobs across 147 locations, 19 fields
* [Naukri Jobs Scraper](https://themineworks.com/actors/naukri-jobs/): India's largest job board structured as clean JSON

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works

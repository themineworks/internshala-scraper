#!/usr/bin/env python3
"""Internships & early-career jobs, 24 fields. Python, Node.js and cURL clients for the Internshala Scraper on Apify, pay per result.

Command-line client for the themineworks/internshala-jobs-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/internshala-jobs-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/internshala-jobs-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--search-keywords", help="Comma-separated. One or more free-text keywords (role, skill or company), for example 'digital marketing'…")
    ap.add_argument("--employment-type", help="Which Internshala board to search")
    ap.add_argument("--category", help="Internshala profile/category slug, for example 'computer-science', 'digital-marketing'…")
    ap.add_argument("--location", help="City name, for example 'bangalore', 'mumbai', 'delhi', 'pune'")
    ap.add_argument("--work-from-home", action=argparse.BooleanOptionalAction, help="Only return remote / work-from-home listings")
    ap.add_argument("--part-time", action=argparse.BooleanOptionalAction, help="Only return part-time listings")
    ap.add_argument("--max-results", type=int, help="Maximum number of listings to scrape across all keywords")
    ap.add_argument("--include-description", action=argparse.BooleanOptionalAction, help="If true, include the full listing description text")
    ap.add_argument("--monitor-mode", action=argparse.BooleanOptionalAction, help="Run on a schedule and deliver ONLY results not seen in a previous run")
    ap.add_argument("--stipend-min", type=int, help="Minimum monthly stipend in INR for internships, or minimum annual salary in INR for jobs")
    ap.add_argument("--duration-max-months", type=int, help="Only for internships")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.search_keywords: run_input["searchKeywords"] = [s.strip() for s in a.search_keywords.split(",") if s.strip()]
    if a.employment_type is not None: run_input["employmentType"] = a.employment_type
    if a.category is not None: run_input["category"] = a.category
    if a.location is not None: run_input["location"] = a.location
    if a.work_from_home is not None: run_input["workFromHome"] = a.work_from_home
    if a.part_time is not None: run_input["partTime"] = a.part_time
    if a.max_results is not None: run_input["maxResults"] = a.max_results
    if a.include_description is not None: run_input["includeDescription"] = a.include_description
    if a.monitor_mode is not None: run_input["monitorMode"] = a.monitor_mode
    if a.stipend_min is not None: run_input["stipendMin"] = a.stipend_min
    if a.duration_max_months is not None: run_input["durationMaxMonths"] = a.duration_max_months

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()

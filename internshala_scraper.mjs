#!/usr/bin/env node
// Node.js client for the themineworks/internshala-jobs-scraper actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/internshala-jobs-scraper/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/internshala-jobs-scraper';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['search-keywords'] !== undefined) runInput.searchKeywords = String(args['search-keywords']).split(',').map((s) => s.trim());
if (args['employment-type'] !== undefined) runInput.employmentType = String(args['employment-type']);
if (args['category'] !== undefined) runInput.category = String(args['category']);
if (args['location'] !== undefined) runInput.location = String(args['location']);
if (args['work-from-home'] !== undefined) runInput.workFromHome = args['work-from-home'] === true || args['work-from-home'] === 'true';
if (args['part-time'] !== undefined) runInput.partTime = args['part-time'] === true || args['part-time'] === 'true';
if (args['max-results'] !== undefined) runInput.maxResults = parseInt(args['max-results'], 10);
if (args['include-description'] !== undefined) runInput.includeDescription = args['include-description'] === true || args['include-description'] === 'true';
if (args['monitor-mode'] !== undefined) runInput.monitorMode = args['monitor-mode'] === true || args['monitor-mode'] === 'true';
if (args['stipend-min'] !== undefined) runInput.stipendMin = parseInt(args['stipend-min'], 10);
if (args['duration-max-months'] !== undefined) runInput.durationMaxMonths = parseInt(args['duration-max-months'], 10);

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);

import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import config from '../config.json';
import sstubs from '../dataset/sstubsLarge.json';

const GITHUB_TOKEN = config.sstubsTokenMim;
const BASE_URL = 'https://api.github.com';
const HEADERS = {
  'Authorization': `token ${GITHUB_TOKEN}`,
  'accept': 'application/vnd.github.v3+json',
}

const ITERATION = 128;
const PAGE_SIZE = 500;

const CACHE = {};

async function run() {
  const authorLoadPromises = [];
  const offset = ITERATION * PAGE_SIZE;
  let saveCount = 0;
  for (let i = offset; i < sstubs.length; i++) {
    if (i === offset + PAGE_SIZE) {
      break;
    }
    const entry = sstubs[i];

    if (entry.fixCommitSHA1 in CACHE) {
      saveCount++;
      continue;
    }
    // temporarily causing `entry.fixCommitSHA1 in CACHE` to be true
    CACHE[entry.fixCommitSHA1] = null;

    const url = `${BASE_URL}/repos/${entry.projectName.replace('.', '/')}/commits/${entry.fixCommitSHA1}`
    const responsePromise = axios
      .get(url, { headers: HEADERS })
      .then((response) => {
        // setting the actual value of CACHE[entry.fixCommitSHA1]
        CACHE[entry.fixCommitSHA1] = response;
        return response;
      })
      .catch((error) => {
        const response = error.response;
        console.log(`Failed ${sstubs[i].fixCommitSHA1}. ${response.status} ${response ? JSON.stringify(response.data) : response}`);
        return response;
      });
    authorLoadPromises.push(responsePromise);
  }

  console.log('Promise Generation Complete');

  const responses = await Promise.all(authorLoadPromises);

  const data = [];
  for (let i = offset; i < sstubs.length; i++) {
    if (i === offset + PAGE_SIZE) {
      break;
    }
    const entry = sstubs[i];
    const response = CACHE[entry.fixCommitSHA1];
    if (!response) {
      data.push({
        error: 'Request failed',
        i,
        ...sstubs[i],
      });
      continue;
    }
    let commit;
    if (typeof response.data === "string") {
      const commitIndex = response.data.indexOf('"commit"');
      const commitPayload = response.data.substring(commitIndex, response.data.indexOf(',"tree"'));
      commit = JSON.parse(`{${commitPayload}}}`).commit;
    } else {
      commit = response.data.commit;
    }
    if (!commit) {
      console.log('Commit is empty', sstubs[i].fixCommitSHA1, typeof response.data, response.data, '\n');
      data.push({
        error: 'Commit is empty',
        i,
        ...sstubs[i],
      });
      continue;
    }

    data.push({
      i,
      ...sstubs[i],
      author: commit.author.name,
      email: commit.author.email,
      date: commit.author.date,
    });
  }

  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const url = path.join(__dirname, '..', 'dataset', `sstubsLargeWithAuthors${ITERATION}.json`);
  fs.writeFileSync(url, JSON.stringify(data, null, 2));
  console.log('Iteration', ITERATION);
  console.log('Written', data.length, 'entries.', offset, 'to', offset + PAGE_SIZE);
  console.log('Saved', saveCount, 'requests');
  let headers = (responses.slice(-1)[0] || {}).headers;
  console.log('Remaining Requests:', headers && headers['x-ratelimit-remaining']);
}

run()
  .then(() => {
    console.log('Done');
  })
  .catch((error) => {
    console.log(error);
    process.exit(1);
  });

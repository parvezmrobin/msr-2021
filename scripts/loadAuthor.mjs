import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import config from '../config.json';
import sstubs from '../dataset/sstubsLarge.json';

const GITHUB_TOKEN = config.sstubsTokenAbu;
const BASE_URL = 'https://api.github.com';
const HEADERS = {
  'Authorization': `token ${GITHUB_TOKEN}`,
  'accept': 'application/vnd.github.v3+json',
}

const ITERATION = 5;
const PAGE_SIZE = 1000;

async function run() {
  const authorLoadPromises = [];
  const offset = ITERATION * PAGE_SIZE;
  for (let i = offset; i < sstubs.length; i++) {
    if (i === offset + PAGE_SIZE) {
      break;
    }
    const entry = sstubs[i];
    const url = `${BASE_URL}/repos/${entry.projectName.replace('.', '/')}/commits/${entry.fixCommitSHA1}`
    const responsePromise = axios.get(url, {
      headers: HEADERS,
    });
    authorLoadPromises.push(responsePromise);
  }

  console.log('Promise Generation Complete');

  const responses = await Promise.allSettled(authorLoadPromises);
  const data = responses.map(({ status, value, reason }, i) => {
    if (status === 'rejected') {
      const response = reason.response;
      console.log(`Failed ${sstubs[i].fixCommitSHA1}. ${response ? response.data.message : response}`);
      return null;
    }
    const commit = value.data.commit;
    if (!commit) {
      console.log('Commit is empty', sstubs[i].fixCommitSHA1, typeof value.data, value.data, '\n');
      return null;
    }
    return {
      i: offset + i,
      ...sstubs[offset + i],
      author: commit.author.name,
      email: commit.author.email,
      date: commit.author.date,
    };
  })

  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const url = path.join(__dirname, '..', 'dataset', `sstubsLargeWithAuthors${ITERATION}.json`);
  fs.writeFileSync(url, JSON.stringify(data, null, 2));
  console.log('Written', data.length, 'entries');
}

run()
  .then(() => {
    console.log('Done');
  })
  .catch((error) => {
    console.log(error);
    process.exit(1);
  });

const CDLI = require('cdli-api-client');
const fs = require('fs');
const path = require('path');

const host = process.argv[2] || process.env.CDLI_HOST || 'https://cdli.earth/';
const outFile = process.argv[3] || 'cdli/data/all.nt';

// full list of entities from the CLI example
const entities = [
  'abbreviations','archives','artifacts','artifact-assets',
  'artifacts-external-resources','artifacts-materials','authors','collections',
  'dynasties','entities-external-resources','entities-names','external-resources',
  'genres','inscriptions','journals','languages','locations','materials',
  'material-aspects','material-colors','periods','places','proveniences',
  'publications','regions','rulers'
];

// ensure output directory exists
fs.mkdirSync(path.dirname(outFile), { recursive: true });

const client = new CDLI.Client(host);

// process logging
client.on('log', msg => process.stderr.write(msg + '\n'));

// request export — pass a single options object with entities + outputFile + format
client.export({ entities, outputFile: outFile, format: 'ntriples' })
  .then(results => {
    const rejected = results.filter(r => r.status === 'rejected');
    if (rejected.length) {
      rejected.forEach(r => console.error(r.reason));
      process.exit(1);
    } else {
      console.log('Export finished:', outFile);
      process.exit(0);
    }
  })
  .catch(err => {
    console.error('Export error:', err);
    process.exit(2);
  });
const chokidar = require('chokidar');
const pdf = require('./pdf')
const fs = require('fs');
require('dotenv').config()

const mailgun = require('mailgun.js');
const mg = mailgun.client({ username: 'api', key: process.env.MAILGUN_KEY || 'key-yourkeyhere' });

chokidar.watch('.', {
    ignored: /(^|[\/\\])\../, // ignore dotfiles
    persistent: true,
    ignoreInitial: true,
    cwd: './dataset',
}).on('add', path => {
    pdf.parse(path.split(".")[0])
});

chokidar.watch('.', {
    ignored: /(^|[\/\\])\../, // ignore dotfiles
    persistent: true,
    ignoreInitial: true,
    cwd: './results',
}).on('add', path => {
    // read the json
    const obj = JSON.parse(fs.readFileSync(`./results/${path}`, 'utf8'));
    console.log(obj)

    mg.messages.create('sandbox63c93d12ad14430b94a045351e329c88.mailgun.org', {
        from: "Mailgun Sandbox <postmaster@sandbox63c93d12ad14430b94a045351e329c88.mailgun.org>",
        to: ["j.zhao2k19@gmail.com", "itsrishikothari@gmail.com"],
        subject: "Welcome to Ligest!",
        text: "Some Dummy Text",
        html: `
            <h1>Here's whats new from the world around you</h1>
            <p>${obj.summary}</p>

            <h3>Categories</h3>
            <ul>
                ${obj.categories.map(c => `<li>${c}</li>`)}
            </ul>
        `
    })
        .then(msg => console.log(msg)) // logs response data
        .catch(err => console.log(err)); // logs any error
});
const fs = require('fs');
const pdf = require('./pdf')

function readAllFiles(path) {
    const filesInDir = fs.readdirSync(path).map(d => d.split(".")[0]);
    return filesInDir;
}

async function proc(list, exclude) {
    console.log(exclude)
    for (var i = 0; i < list.length; i++) {
        if (exclude.includes(list[i])) {
            console.log(`skipping ${list[i]}...`)
        } else {
            await pdf.parse(list[i])
        }
    }
}

proc(readAllFiles("./dataset"), readAllFiles("./results"))
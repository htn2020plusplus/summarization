const chokidar = require('chokidar');
const pdf = require('./pdf')

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
});
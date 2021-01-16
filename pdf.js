const fs = require('fs');
const pdf = require('pdf-parse');

let dataBuffer = fs.readFileSync('./testing/test-senior.pdf');

// turn arr into 'chunks' of chunkSize
function chunk(arr, chunkSize) {
	var res = [];
	for (var i = 0, len = arr.length; i < len; i += chunkSize)
		res.push(arr.slice(i, i + chunkSize));
	return res;
}


const MAX_TOK_SIZE = 4096
const TOK_SCALE = 2
pdf(dataBuffer).then(function(data) {
	cleanedText = data.text.replace(/(\r\n|\n|\r)/gm,"")
	tokens = cleanedText.split(" ")
	chunks = chunk(tokens, Math.round(MAX_TOK_SIZE / TOK_SCALE)).map(c => c.join(" "))
	console.log(chunks);
	console.log(chunks.length) 
        
});

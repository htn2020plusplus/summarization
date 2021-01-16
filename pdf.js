const fs = require('fs');
const pdf = require('pdf-parse');
const axios = require('axios');
const querystring = require('querystring');

const api_url = "http://localhost:5000/api/summarize"
let dataBuffer = fs.readFileSync('./testing/test-senior.pdf');

// turn arr into 'chunks' of chunkSize
function chunk(arr, chunkSize) {
	var res = [];
	for (var i = 0, len = arr.length; i < len; i += chunkSize)
		res.push(arr.slice(i, i + chunkSize));
	return res;
}


const MAX_TOK_SIZE = 4096
const TOK_SCALE = 8
pdf(dataBuffer).then(function(data) {
	cleanedText = data.text.replace(/(\r\n|\n|\r)/gm,"")
	tokens = cleanedText.split(" ")
	chunks = chunk(tokens, Math.round(MAX_TOK_SIZE / TOK_SCALE)).map(c => c.join(" "))

	// post to api
	// console.log(chunks[0].length)
	reqs = chunks.map(chunk => axios.post(api_url, querystring.stringify({ text: chunk })))
	Promise.all(reqs).then(vals => console.log(vals)).catch(err => console.error(err))
})

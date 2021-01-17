const fs = require('fs');
const pdf = require('pdf-parse');
const axios = require('axios');
const querystring = require('querystring');

const api_url = "http://localhost:5000/api"

// turn arr into 'chunks' of chunkSize
function chunk(arr, chunkSize) {
	var res = [];
	for (var i = 0, len = arr.length; i < len; i += chunkSize)
		res.push(arr.slice(i, i + chunkSize));
	return res;
}

async function parse(name) {
	let dataBuffer = fs.readFileSync(`./dataset/${name}.pdf`);
	const MAX_TOK_SIZE = 512
	const data = await pdf(dataBuffer)

	cleanedText = data.text.replace(/(\r\n|\n|\r)/gm, "")
	tokens = cleanedText.split(" ")
	chunks = chunk(tokens, Math.round(MAX_TOK_SIZE)).map(c => c.join(" "))

	// post to api
	console.log(`sending ${chunks.length} requests to back end for inference...`)
	const res = []

	for (var i = 0; i < chunks.length; i++) {
		try {
			const r = await axios.post(api_url + "/summarize", querystring.stringify({ text: chunks[i] }))
			const t = r.data.summary
			console.log(`[${i}] -> ${t}`)
			res.push(t)
		} catch (e) {
			console.log(`uhoh: ${e}`)
		}
	}

	try {
		console.log("performing named entity recognition...")
		const full = res.join(" ")
		const r = await axios.post(api_url + "/ner", querystring.stringify({ text: full }))

		const CATEGORY_THRESH = 0.4
		const c = await axios.post(api_url + "/categorize", querystring.stringify({ text: full }))
		console.log(c)
		const categories = Object.keys(c.data).filter(cat => c.data[cat] > CATEGORY_THRESH)

		const retData = JSON.stringify({
			named_entities: r.data,
			categories: categories,
			summary: full,
		}, null, 4)

		fs.writeFile(`./results/${name}.json`, retData, (err) => {
			if (err) {
				console.log(err);
			}
		});
	} catch (e) {
		console.log(`uhoh: ${e} (most likely not enough text)`)
	}

}

exports.parse = parse
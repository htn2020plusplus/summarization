const fs = require('fs');
const pdf = require('pdf-parse');

let dataBuffer = fs.readFileSync('/Users/ansonyu/Projects/summarization/testing/test.pdf');

pdf(dataBuffer).then(function(data) {

	cleanedText = data.text.replace(/(\r\n|\n|\r)/gm,"")
	console.log(cleanedText); 
        
});

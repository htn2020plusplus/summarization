from flask import request
from flask import jsonify
import flask
import logging

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def healthCheck():
    logging.info("Health check ping received")
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/summarize', methods=['POST'])
def parseIntent():
    data = flask.request.form  # is a dictionary
    text = data['text']
    logging.info(f"got pred request of length {len(text)}")

    answer = summarizer(text, max_length=500,
                        min_length=30, do_sample=False)

    # process
    # get first rest
    # get summary text result
    # replace leading space before period
    answer = answer[0]['summary_text'].replace(" .", ".")

    logging.info(f"processed summary: {answer}")

    return jsonify({'summary': answer}), 200

if __name__ == '__main__':
    logging.info("Starting server...")

    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    summarizer = pipeline("summarization")

    app.run(host="0.0.0.0", port=5000)


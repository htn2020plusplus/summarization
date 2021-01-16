from flask import request
from flask import jsonify
import flask
import logging
import os
import torch

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForTokenClassification

app = flask.Flask(__name__)

ner_labels = [
    "O",       # Outside of a named entity
    "B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity
    "I-MISC",  # Miscellaneous entity
    "B-PER",   # Beginning of a person's name right after another person's name
    "I-PER",   # Person's name
    "B-ORG",   # Beginning of an organisation right after another organisation
    "I-ORG",   # Organisation
    "B-LOC",   # Beginning of a location right after another location
    "I-LOC"    # Location
]


@app.route('/', methods=['GET'])
def healthCheck():
    logging.info("Health check ping received")
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = flask.request.form  # is a dictionary
    text = data['text']
    logging.info(f"got summarization request of length {len(text)}")

    answer = summarizer(text, max_length=4096,
                        min_length=30, do_sample=False)

    # process
    # get first rest
    # get summary text result
    # replace leading space before period
    answer = answer[0]['summary_text'].replace(" .", ".")

    logging.info(f"processed summary: {answer}")

    return jsonify({'summary': answer}), 200


@app.route('/api/ner', methods=['POST'])
def ner():
    data = flask.request.form  # is a dictionary
    text = data['text']
    logging.info(f"got ner request of length {len(text)}")

    tokens = ner_tokenizer.tokenize(
        ner_tokenizer.decode(tokenizer.encode(text)))
    inputs = ner_tokenizer.encode(text, return_tensors="pt")
    outputs = ner_model(inputs)[0]
    predictions = torch.argmax(outputs, dim=2)

    return jsonify({'tokens': [(token, ner_labels[prediction]) for token, prediction in zip(tokens, predictions[0].tolist())]}), 200

if __name__ == '__main__':
    logging.info("Starting server...")

    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    ner_model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    ner_tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    summarizer = pipeline("summarization")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


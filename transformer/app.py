from werkzeug.utils import secure_filename
from flask import request, jsonify, request, redirect, url_for
import flask
import logging
import os
import torch
import requests

from dotenv import load_dotenv
load_dotenv()

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForTokenClassification

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = "../dataset"
ALLOWED_EXTENSIONS = {'pdf'}

# ner_labels = [
#     "O",       # Outside of a named entity
#     "B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity
#     "I-MISC",  # Miscellaneous entity
#     "B-PER",   # Beginning of a person's name right after another person's name
#     "I-PER",   # Person's name
#     "B-ORG",   # Beginning of an organisation right after another organisation
#     "I-ORG",   # Organisation
#     "B-LOC",   # Beginning of a location right after another location
#     "I-LOC"    # Location
# ]

@app.route('/', methods=['GET'])
def healthCheck():
    logging.info("Health check ping received")
    return jsonify({'status': 'healthy'}), 200


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "no file part", 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return "no selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "success", 200


@app.route('/api/summarize', methods=['POST'])
def summarizeReq():
    data = flask.request.form  # is a dictionary
    text = data['text']
    print(f"got summarization request of length {len(text)}")

    if len(text) < 10:
        return "too short", 400

    answer = _summarize(text)
    logging.info(f"processed summary: {answer}")

    return jsonify({'summary': answer}), 200

def _summarize(text):
    answer = summarizer(text, max_length=150,
                            min_length=15, do_sample=False)

    # process
    # get first rest
    # get summary text result
    # replace leading space before period
    answer = answer[0]['summary_text'].replace(" .", ".")
    return answer

@app.route('/api/categorize', methods=['POST'])
def categorize():


    data = flask.request.form  # is a dictionary
    text = data['text']
    print(f"got categorization request of length {len(text)}")

    if len(text) < 10:
        return "too short", 400

    res_proc = _categorize(text)
    return jsonify(res_proc), 200

def _categorize(text):
    categories = [
        "environmental",
        "defence",
        "education",
        "economy",
        "legal",
        "energy",
        "social development",
        "healthcare",
        "indigenous",
        "technology",
        "parliament",
        "infrastructure",
        "transportation",
        "agriculture",
        "media"
    ]

    res = classifier(text, categories, multi_class=True)
    res_proc = dict((key, value)
                    for key, value in zip(res['labels'], res['scores']))
    return res_proc

@app.route('/api/ner', methods=['POST'])
def nerReq():
    data = flask.request.form  # is a dictionary
    text = data['text']
    print(f"got ner request of length {len(text)}")

    if len(text) < 10:
        return "too short", 400

    # tokens = ner_tokenizer.tokenize(
    #     ner_tokenizer.decode(ner_tokenizer.encode(text)))
    # inputs = ner_tokenizer.encode(text, return_tensors="pt")
    # outputs = ner_model(inputs)[0]
    # predictions = torch.argmax(outputs, dim=2)

    # tok_pred_iter = zip(tokens, predictions[0].tolist())

    # # filter
    # res = [(token, ner_labels[prediction]) if prediction != 0 for token, prediction in tok_pred_iter]

    ner_label_mappings = {
        "MISC": "misc",
        "ORG": "organization",
        "PER": "person",
        "LOC": "location",
    }

    NER_THRESH = float(request.args.get('ner_thres', '0.7'))
    DISCARD_MISC = request.args.get('discard_misc', 'yes')
    DISCARD_MISC = DISCARD_MISC == 'yes'

    ners = ner(text)
    filtered_ners = []
    for entity in ners:

        # perform mapping
        entity["entity_group"] = ner_label_mappings[entity["entity_group"]]

        # cast np int64 back to python float for json dump
        entity["score"] = float(entity["score"])
        entity["start"] = int(entity["start"])
        entity["end"] = int(entity["end"])

        # filtering
        valid_score = entity["score"] > NER_THRESH
        should_discard = DISCARD_MISC and entity["entity_group"] == 'misc'

        if valid_score and not should_discard and len(entity["word"]) > 1:
            filtered_ners.append(entity)

    return jsonify({"entities": filtered_ners}), 200

logging.info("Starting server...")

# tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
# model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
ner_model = AutoModelForTokenClassification.from_pretrained(
    "dbmdz/bert-large-cased-finetuned-conll03-english")
ner_tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

summarizer = pipeline("summarization")
ner = pipeline("ner", model=ner_model,
                tokenizer=ner_tokenizer, grouped_entities=True)
classifier = pipeline("zero-shot-classification")

logging.info("Models loaded.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

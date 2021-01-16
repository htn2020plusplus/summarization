# 🏛 Legist
## ML and Data Pipelines

This repository contains the files and modules do
* Text summarization (DistilBART-CNN)
* Named entity recognition (BERT-Large)
  * Can identiy organizations, people, locations, and misc.
* PDF-to-text parsing

You can find our ML models in the `/transformer` folder. Within it, the `app.py` is our actual API server. It can be started via Docker container too!

## API Docs

### NER -- `/api/ner`
**Query Parameters**
1. `ner_thres=0.7` any entities with a confidence level below this threshold will be discarded.
2. `discard_misc=yes` any entities with a MISC entity_group will be discarded.

```bash
$ curl -X POST localhost:5000/api/ner --form 'text=...'

{
    "entities": [
        {
            "end": 69,
            "entity_group": "organization",
            "score": 0.7794190943241119,
            "start": 66,
            "word": "CSA"
        },
        {
            "end": 1230,
            "entity_group": "organization",
            "score": 0.7414421737194061,
            "start": 1227,
            "word": "EDI"
        },
        {
            "end": 1506,
            "entity_group": "organization",
            "score": 0.985912412405014,
            "start": 1502,
            "word": "CBSA"
        },
        {
            "end": 2055,
            "entity_group": "location",
            "score": 0.9944024085998535,
            "start": 2049,
            "word": "Canada"
        }
    ]
}
```



### Text Summarization -- `/api/summarization`
```bash
$ curl -X POST localhost:5000/api/summarization --form 'text=...'

{
    "summary": " This memorandum has been revised to include the obligations of CSA Carriers regarding the transmission of Advanced Commercial Information (ACI) This includes information regarding procedures for clients who strictly use the paper method of reporting CSA shipments as well as for participants that utilize the current CSA electronic reporting method."
}
```

todo: more details
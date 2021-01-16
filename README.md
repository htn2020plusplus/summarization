# 🏛 Legist
## ML and Data Pipelines

This repository contains the files and modules do
* Text summarization (DistilBART-CNN)
* Named entity recognition (BERT-Large)
  * Can identiy organizations, people, locations, and misc.
* Zero-shot Categorization (BART-Large)
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

### Zero-shot classification -- `/api/categorization`
```bash
$ curl -X POST localhost:5000/api/categorization --form 'text=...'

{
    "agriculture": 0.024784492328763008,
    "defence": 0.1793070286512375,
    "economy": 0.48788025975227356,
    "education": 0.05529370158910751,
    "energy": 0.1122642457485199,
    "environmental": 0.026572316884994507,
    "healthcare": 0.04257747530937195,
    "indigenous": 0.11204517632722855,
    "infrastructure": 0.1094297543168068,
    "legal": 0.5790539383888245,
    "media": 0.23331807553768158,
    "parliament": 0.11976903676986694,
    "social development": 0.6372514963150024,
    "technology": 0.07259909063577652
}
```
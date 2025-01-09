# SpaCy Keyword Extraction API

Provides an API to extract keywords from a text. It using [SpaCy](https://spacy.io/) to find noun chunks and some additional post-processing.

## API

### `/v1/batch-extract-keywords`

Example Input:

```json
{
  "data": [
    {
      "type": "extract-keyword-request",
      "id": "doc-1",
      "attributes": {
        "content": "I am interested in biochemistry and neuroscience."
      },
      "meta": {
        "extra_id": "doc-1/v1"
      }
    }
  ]
}
```

Required fields: `type` and `attributes.content`

The `id` and `meta` fields are optional. When provided, they will also be included in the response.

Example response:

```json
{
  "data": [
    {
      "type": "extract-keyword-result",
      "attributes": {
        "keywords": [
          {
            "keyword": "biochemistry",
            "count": 1
          },
          {
            "keyword": "neuroscience",
            "count": 1
          }
        ]
      },
      "id": "doc-1",
      "meta": {
        "extra_id": "doc-1/v1"
      }
    }
  ],
  "meta": {
    "spacy_version": "2.3.9",
    "spacy_language_model_name": "en_core_web_lg",
    "python_version": "3.11.11",
    "revision": "6ec060c861a133ec986d883e86404a43bcd32930"
  }
}
```

## Development Using Virtual Environment

### Pre-requisites (Virtual Environment)

* Python, ideally using `pyenv` (see `.python-version`)

### First Setup (Virtual Environment)

```bash
make dev-venv
```

### Update Dependencies (Virtual Environment)

```bash
make dev-install
```

### Run Tests (Virtual Environment)

```bash
make dev-test
```


### Start Server (Virtual Environment)

```bash
make dev-start
```

The server will be available on port 8000.

You can access the API Docs via http://localhost:8000/docs


## Development Using Docker

### Pre-requisites (Docker)

* Docker

### Run Tests (Docker)

```bash
make build-dev test
```

### Start Server (Docker)

```bash
make build start logs
```

The server will be available on port 8000.

You can access the API Docs via http://localhost:8000/docs

### Stop Server (Docker)

```bash
make stop
```

# SpaCy Keyword Extraction API

Provides an API to extract keywords from a text. It using [SpaCy](https://spacy.io/) to find noun chunks and some additional post-processing.

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

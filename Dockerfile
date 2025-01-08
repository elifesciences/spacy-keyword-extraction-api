FROM python:3.9-slim

RUN apt-get update \
    && apt-get install --assume-yes --quiet --quiet \
      gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.build.txt ./
RUN pip install --disable-pip-version-check \
    -r requirements.build.txt

# install spaCy separately to allow better caching of large language model download
COPY requirements.spacy.txt ./
RUN pip install --disable-pip-version-check -r requirements.spacy.txt

# download spaCy language models
RUN python -m spacy download en_core_web_lg

COPY requirements.txt ./
RUN pip install --disable-pip-version-check \
    -r requirements.spacy.txt \
    -r requirements.txt

COPY requirements.dev.txt ./
ARG install_dev=n
RUN if [ "${install_dev}" = "y" ]; then \
    pip install --disable-pip-version-check --user \
        -r requirements.spacy.txt \
        -r requirements.txt \
        -r requirements.dev.txt; \
    fi

COPY spacy_keyword_extraction_api ./spacy_keyword_extraction_api
COPY static ./static
COPY config ./config

COPY tests ./tests
COPY .flake8 .pylintrc pyproject.toml ./

CMD ["python3", "-m", "uvicorn", "spacy_keyword_extraction_api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--log-config=config/logging.yaml"]

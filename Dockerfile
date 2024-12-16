FROM python:3.8-slim

COPY requirements.build.txt ./
RUN pip install --disable-pip-version-check \
    -r requirements.build.txt

COPY requirements.txt ./
RUN pip install --disable-pip-version-check \
    -r requirements.txt

COPY spacy_keyword_extraction_api ./spacy_keyword_extraction_api
COPY static ./static

CMD ["python3", "-m", "uvicorn", "spacy_keyword_extraction_api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.8-slim
ARG install_dev=n

COPY requirements.build.txt ./
RUN pip install --disable-pip-version-check \
    -r requirements.build.txt

COPY requirements.txt ./
RUN pip install --disable-pip-version-check \
    -r requirements.txt

COPY requirements.dev.txt ./
RUN if [ "${install_dev}" = "y" ]; then \
    pip install --disable-pip-version-check --user \
        -r requirements.txt \
        -r requirements.dev.txt; \
    fi

COPY spacy_keyword_extraction_api ./spacy_keyword_extraction_api
COPY static ./static
COPY tests ./tests

COPY .flake8 .pylintrc ./

CMD ["python3", "-m", "uvicorn", "spacy_keyword_extraction_api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

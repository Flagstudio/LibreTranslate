FROM python:3.8.12-slim-bullseye

ARG with_models=false
ARG models=

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq \
  && apt-get -qqq install --no-install-recommends -y libicu-dev pkg-config gcc g++ \
  && apt-get clean \
  && rm -rf /var/lib/apt

RUN pip install --upgrade pip

COPY . .

COPY LibreTranslate /root/.local/share/LibreTranslate

RUN if [ "$with_models" = "true" ]; then  \
        # install only the dependencies first
        pip install -e .;  \
        # initialize the language models
        if [ ! -z "$models" ]; then \
                  ./install_models.py --load_only_lang_codes "$models";   \
        else \
                  ./install_models.py;  \
        fi \
    fi
# Install package from source code
RUN pip install . \
  && pip cache purge

EXPOSE 5000
ENTRYPOINT [ "libretranslate", "--host", "0.0.0.0" ]

ARG python_image_v="python:3.10"
# python3.10のイメージをダウンロード
FROM ${python_image_v}

ARG work_dir="/app"

# コンテナにアクセスした際のデフォルトディレクトリ
WORKDIR ${work_dir}

# poetryのインストール先の指定
ENV POETRY_VERSION=1.2.2
# poetryインストール
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python - --version ${POETRY_VERSION} && \
# シンボリックによるpathへのpoetryコマンドの追加
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
# 仮想環境を作成しない設定(コンテナ前提のため，仮想環境を作らない)
    poetry config virtualenvs.create false

COPY ./app/pyproject.toml ./app/poetry.lock* /app/
# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"


COPY ./app /app
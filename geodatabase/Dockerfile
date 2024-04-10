FROM debian:11 as builder
ADD https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh .
RUN sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda
ENV PATH=/opt/conda/bin:${PATH}
RUN apt-get update && apt-get install -y curl gnupg

RUN conda update -n base -c defaults conda
RUN conda config --add channels conda-forge
COPY conda_requirements.txt ./
RUN conda install --file conda_requirements.txt

# ===========================================
# DEPLOYMENT STAGE -- install and run the microservice
# Note that python-bjoern is running in Debian Bullseye
FROM tecktron/python-bjoern as deployed
COPY --from=builder /opt/conda /opt/conda
ENV PATH=/opt/conda/bin:${PATH}

# TODO I readlly want to move the driver install up into the builder stage   
# Add the ODBC driver so we can talk to SQL Server
# https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#microsoft-odbc-driver-13-for-sql-server
ENV ACCEPT_EULA=y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -  && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    apt-get install -y msodbcsql18

ENV PYTHONPATH /app
WORKDIR /app
COPY prestart.sh .
COPY app app

RUN useradd --uid 1000 --create-home --home-dir /srv/arctic arctic && \
    chfn --full-name "Arctic" arctic
USER arctic
WORKDIR /srv/arctic

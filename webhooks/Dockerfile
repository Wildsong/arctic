FROM wildsong/flask:latest
LABEL maintainer="Brian Wilson <brian@wildsong.biz>"
LABEL version="1.0"
LABEL biz.wildsong.name="arctic_webhooks"

ENV SERVER_BASE /srv

USER app
WORKDIR /home/app

# Install the packages that this project needs.
COPY project_requirements.txt .
RUN conda install -y --file project_requirements.txt

WORKDIR $SERVER_BASE

EXPOSE 9443
VOLUME /srv


FROM python:3

RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP

WORKDIR /usr/src/insta-unfollower-beak

COPY unfollower-beak.py requirements.txt /usr/src/insta-unfollower-beak/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-u", "unfollower-beak.py"]

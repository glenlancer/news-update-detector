# news-update-detector

This repo provides a demo program for [isentia](https://www.isentia.com/) interview process. Task description can be found [here](https://bitbucket.org/isentia/coding-challenge-news-update-backend/src/master/).

## How to run the program

### Run in local environment

```bash
python3 -m venv news_update_detector_venv
source news_update_detector_venv/bin/activate
pip install -r requirements.txt
python src/news-update-detector.py
```

Or enter, `$ ./run.sh`

### Run using docker-ce

1. Build docker image:
    - `sudo docker build -t detector_image .`
2. Run built docker image:
    - `sudo docker run detector_image`

## How the program works

This program collects news from the front page of [news.com.au](https://www.news.com.au/)

## Unit tests
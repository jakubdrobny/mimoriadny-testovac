# mimoriadny-testovac

online judge with code isolation, async judging using redis-queue + learning resources


# run this locally
1. you need git lfs
2. git lfs pull in ulohy folder
3. pip install -r requirements.txt (in root folder)
4. install redis using digitalocean tutorial
5. set environment variables from .env file
6. pip install rq
7. flask run in root folder
8. rq worker testovac-judge
6. have fun :)

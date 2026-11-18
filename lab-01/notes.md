FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]

((.venv) ) alina@MacBook-Air-Alina lab-01 % docker build --no-cache --progress=plain -t lab1:bad . 2>&1 | grep "transferring context"  
#4 transferring context: 2B done
#6 transferring context: 42.19MB 1.5s done

((.venv) ) alina@MacBook-Air-Alina lab-01 % docker build --no-cache --progress=plain -t lab1:bad . 2>&1 | grep "transferring context"
#3 transferring context: 78B done
#6 transferring context: 875B 0.1s done

EXPOSE лише документація, порт відкриває -p. failed

docker build --no-cache -t lab1:bad . 0.41s user 0.33s system 6% cpu 11.653 total
docker build -t lab1:bad . 0.40s user 0.26s system 5% cpu 12.213 total

FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]

docker build --no-cache -t lab1:good . 0.52s user 0.58s system 9% cpu 11.965 total
docker build -t lab1:good . 0.46s user 0.23s system 50% cpu 1.376 total

((.venv) ) alina@MacBook-Air-Alina lab-01 % docker images lab1 --format "{{.Tag}}\t{{.Size}}"
final 249MB
slim 264MB
good 1.67GB
full 1.67GB
bad 1.67GB

((.venv) ) alina@MacBook-Air-Alina lab-01 % docker run --rm lab1:full which gcc
/usr/bin/gcc
((.venv) ) alina@MacBook-Air-Alina lab-01 % docker run --rm lab1:final which gcc
((.venv) ) alina@MacBook-Air-Alina lab-01 %

((.venv) ) alina@MacBook-Air-Alina lab-01 % docker run --rm lab1:final which gcc
((.venv) ) alina@MacBook-Air-Alina lab-01 % docker run --rm lab1:final id
uid=10001(appuser) gid=999(appuser) groups=999(appuser)
((.venv) ) alina@MacBook-Air-Alina lab-01 % docker run --rm -e PORT=80 lab1:final
cat shop up on 80 / store=/data/visits.txt

- Serving Flask app 'app'
- Debug mode: off
  WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
- Running on all addresses (0.0.0.0)
- Running on http://127.0.0.1:80
- Running on http://172.17.0.2:80
  Press CTRL+C to quit

- You will find advice online that chaining install commands with `&&` makes images smaller. That is
  mostly a myth. **Give the two reasons it actually matters** — then the counter-pressure: why
  putting everything in one enormous `RUN` is also wrong.

1. every run creates a layer, but deleting a file in the next layer does not make it smaller, bacause file is still in the previous one. that is why create and remove must be in one RUN
2. apt-get update in a separate RUN caches separately from install and can remain old. and through `&&` they always go together

counter-pressure: one enormous `RUN` breaks cache, bevause every change reruns everything. so grouping together we must what must change together

conds (healthy) 5432/tcp
((.venv) ) alina@MacBook-Air-Alina lab-01 % curl localhost:8080/visits
{"store":"postgres","visits":1}
((.venv) ) alina@MacBook-Air-Alina lab-01 % curl localhost:8080/visits
{"store":"postgres","visits":2}

(.venv) ) alina@MacBook-Air-Alina lab-01 % curl localhost:8080/visits
{"store":"postgres","visits":5}
((.venv) ) alina@MacBook-Air-Alina lab-01 % docker compose down -v

[+] down 4/4
✔ Container lab-01-app-1 Removed 1.2s
✔ Container lab-01-db-1 Removed 0.1s
✔ Network lab-01_default Removed 0.2s
✔ Volume lab-01_pgdata Removed 0.0s
((.venv) ) alina@MacBook-Air-Alina lab-01 % docker compose up -d app
[+] up 4/4
✔ Network lab-01_default Created 0.0s
✔ Volume lab-01_pgdata Created 0.0s
✔ Container lab-01-db-1 Healthy 4.4s
✔ Container lab-01-app-1 Started 4.4s
((.venv) ) alina@MacBook-Air-Alina lab-01 % sleep 10
((.venv) ) alina@MacBook-Air-Alina lab-01 % curl localhost:8080/visits
{"store":"postgres","visits":1}
((.venv) ) alina@MacBook-Air-Alina lab-01 %

{"store":"postgres","visits":4}
[+] down 3/3
✔ Container lab-01-app-1 Removed 1.3s
✔ Container lab-01-db-1 Removed 0.4s
✔ Network lab-01_default Removed 0.5s
[+] up 3/3
✔ Network lab-01_default Created 0.1s
✔ Container lab-01-db-1 Healthy 4.6s
✔ Container lab-01-app-1 Started 4.5s
{"store":"postgres","visits":5}
((.venv) ) alina@MacBook-Air-Alina lab-01 %

((.venv) ) alina@MacBook-Air-Alina lab-01 % docker compose down -v
docker compose up -d app
docker compose logs app
[+] down 4/4
✔ Container lab-01-app-1 Removed 1.2s
✔ Container lab-01-db-1 Removed 0.1s
✔ Volume lab-01_pgdata Removed 0.0s
✔ Network lab-01_default Removed 0.1s
[+] up 4/4
✔ Network lab-01_default Created 0.0s
✔ Volume lab-01_pgdata Created 0.0s
✔ Container lab-01-db-1 Started 0.3s
✔ Container lab-01-app-1 Started 0.3s
((.venv) ) alina@MacBook-Air-Alina lab-01 %

- One paragraph: a named volume versus a bind mount, and when you would reach for each.
Named volume is managed by Docker, and does not depend on other pathes on host, faster, and is correct for DBs.
Bind mount binds particular folder to host, which is comfortable, when we need to see and refactor files from host (code during development, configs, as init-db).
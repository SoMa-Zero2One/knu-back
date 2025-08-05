# knu-grade
경북대 교환학생 성적 비교 서비스


## Run dev
```
uv run uvicorn app.main:app --reload
uv run uvicorn app.main:app --reload --host 0.0.0.0
```


### Run prod
```
docker build -t knu-server .
docker run -d -p 8000:8000 --name knu-server knu-server
docker run -p 8000:8000 --name knu-server knu-server
```

# knu-grade
경북대 교환학생 성적 비교 서비스


## Run dev
```
uv run uvicorn app.main:app --reload
```


### Run prod
```
docker build -t knu-grade .
docker run -d -p 80:80 knu-grade
```

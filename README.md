# Data-Contracts
Data contracts as code: схемы, версии, breaking changes, CI-валидация.

Data Contracts as Code: YAML-схемы, валидация, версионирование, breaking changes.

## Пример
```bash
uvicorn api.main:app --reload
curl localhost:8000/contracts
curl -F "file=@data.csv" localhost:8000/contracts/customers/validate
```

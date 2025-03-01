# Тестовое заданние от Dimatech

## Развертывание проекта

### Копируем репозиторий
```bash
git clone https://github.com/romich995/dimatech_test.git
```

### Создаем папку data
```bash
cd ./dimatech_test
mkdir data
```

### Билдим проект
```bash
docker compose build
```

### Запуск проекта 
```bash
docker compose up
```

### Проводим миграцию при первом запуске
```bash
docker exec -i -t dimatech_test-web-1 python ./migrate.py
```

## Тестовые профили пользователей

### Администратор

```shell
email: "admin@test.test"
password: "admin"
```


### Пользователь

```shell
email: "test@test.test"
password: "test"
```

## Примеры запросов:

request_examples.html



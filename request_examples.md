```python
import requests
```


```python
res = requests.post('http://0.0.0.0:12340/user/login', json={"email": "test@test.test", "password": "test"})
```


```python
print(res.text)
```

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJ0ZXN0QHRlc3QudGVzdCJ9.5wCXQXONXjt5WQfrU_YyoIElPgWqf1tXD9i8EnL99B0



```python
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJ0ZXN0QHRlc3QudGVzdCJ9.5wCXQXONXjt5WQfrU_YyoIElPgWqf1tXD9i8EnL99B0'
```


```python
res = requests.get('http://127.0.0.0:12340/user/1',)
```


```python
print(res.text)
```

    ⚠️ 404 — Not Found
    ==================
    Requested URL /user/1 not found
    
    



```python
res = requests.get('http://127.0.0.0:12340/user', 
                   headers = {"Authorization": f"Bearer {jwt_token}"})
```


```python
print(res.text)
```

    {"id":1,"email":"test@test.test","full_name":"test"}



```python
res = requests.get('http://127.0.0.0:12340/user/accounts', 
                   headers = {"Authorization": f"Bearer {jwt_token}"})
```


```python
print(res.text)
```

    [{"id":1,"balance":0.0,"user_id":1}]



```python
res = requests.get('http://127.0.0.0:12340/user/replenishments', 
                   headers = {"Authorization": f"Bearer {jwt_token}"})
```


```python
print(res.text)
```

    []



```python
res = requests.post('http://127.0.0.0:12340/user/login', json={"email": "admin@mail.ru", "password": "admin"})
```


```python

```


```python

```


```python
res = requests.post('http://127.0.0.0:12340/administrator/login', json={"email": "admin@test.test", "password": "admin"})
```


```python
print(res.text)
```

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkB0ZXN0LnRlc3QifQ.1JVsKS4Fxh26bduabIgDygXkUQqkHIjd_lGo249Tsfk



```python
jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkB0ZXN0LnRlc3QifQ.1JVsKS4Fxh26bduabIgDygXkUQqkHIjd_lGo249Tsfk'
                   
```


```python
res = requests.get('http://127.0.0.0:12340/administrator', 
                   headers = {"Authorization": f"Bearer {jwt_token}"})
```


```python
print(res.text)
```

    {"id":1,"email":"admin@test.test","full_name":"admin"}



```python
res = requests.post('http://127.0.0.0:12340/administrator/user', 
                    headers = {"Authorization": f"Bearer {jwt_token}"},
                    json={"email": "test@mail.ru", "password": "test" , "full_name": "test"})
```


```python
print(res.text)
```

    {"id":2,"email":"test@mail.ru","full_name":"test"}



```python
res = requests.patch('http://127.0.0.0:12340/administrator/user', 
                    headers = {"Authorization": f"Bearer {jwt_token}"},
                    json={"id":2, "email": "test2@mail.ru", "full_name": "test2", "password": "test2"})
```


```python
print(print(res.text))
```

    {"id":2,"email":"test2@mail.ru","full_name":"test2"}
    None



```python
res = requests.delete('http://127.0.0.0:12340/administrator/user', 
                    headers = {"Authorization": f"Bearer {jwt_token}"},
                    json={"id":1})
```


```python
print(res.text)
```

    Deleted



```python
res = requests.get('http://127.0.0.0:12340/administrator/users', 
                    headers = {"Authorization": f"Bearer {jwt_token}"},
                    )
```


```python
print(res.text)
```

    [{"id":2,"email":"test2@mail.ru","full_name":"test2","accounts":[]}]



```python
transaction = {
  "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
  "user_id": 2,
  "account_id": 2,
  "amount": 100,
  "signature": "294f4097f464cdb2a5b53644083eeb0e7a0771099303af81f74c2ac8a4b6e035"
}

```


```python
from hashlib import sha256
SHA256SECRETKEY = 'dsgfgfdgsd'
```


```python
def check_signature(transaction: dict):
    hsh = sha256(f"{transaction['account_id']}"
                 f"{transaction['amount']}"
                 f"{transaction['transaction_id']}"
                 f"{transaction['user_id']}"
                 f"{SHA256SECRETKEY}".encode()).hexdigest()
    print(hsh)
    return hsh == transaction['signature']

```


```python
check_signature(transaction)
```

    294f4097f464cdb2a5b53644083eeb0e7a0771099303af81f74c2ac8a4b6e035





    True




```python
res = requests.post('http://127.0.0.0:12340/transaction', 
                    json=transaction
                    )
```


```python
print(res.text)
```

    Successful



```python

```


```python

```


```python

```

a python class,operate ms sqlserver,need pymssql  

query data
```
from  msdatabase import MSDataBase
db = MSDataBase(host=host,user=username,password=password,database=database,charset='utf-8')
result = db.query('select * from users')
db.close()
```
operate data

```
from  msdatabase import MSDataBase
db = MSDataBase(host=host,user=username,password=password,database=database,charset='utf-8')
result = db.query_no_result("insert into users (username,age) values ('scaluo',45)")
db.close()
```

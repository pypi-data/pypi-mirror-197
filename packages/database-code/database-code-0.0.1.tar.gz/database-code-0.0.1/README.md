# database-code
 
SQL: `SELECT * FROM tbl`  
Python: `data = db.select(table='tbl')`

SQL: `SELECT * FROM tbl WHERE a = "a1"`  
Python: `data = db.select(table='tbl', params=['a'], values=['a1'])`

SQL: `SELECT * FROM tbl WHERE a = "a1" AND b = "b5"`  
Python: `data = db.select(table='tbl', params=['a', 'b'], values=['a1', 'b5'], operator='AND')`

SQL: `SELECT * FROM tbl WHERE a = "a1" OR b = "b5"`  
Python: `data = db.select(table='tbl', params=['a', 'b'], values=['a1', 'b5'], operator='OR')`

SQL: `SELECT * FROM tbl WHERE a != "a6" AND b = "b1"`  
Python: `data = db.select(table='tbl', params=['!a', 'b'], values=['a6', 'b1'], operator='AND')`

SQL: `SELECT _id, b FROM tbl WHERE b = "b1"`  
Python: `data = db.select(table='tbl', params=['b'], values=['b1'], fields=['_id', 'b'])`

SQL: `SELECT _id, a FROM tbl LIMIT 2`  
Python: `data = db.select(table='tbl', fields=['_id', 'a'], limit=2)`

SQL: `SELECT * FROM tbl ORDER BY _id DESC`  
Python: `data = db.select(table='tbl', order_type='DESC', order_fields='_id')`

SQL: `SELECT _id, a FROM tbl ORDER BY _id DESC LIMIT 3;`  
Python: `data = db.select(table='tbl', fields=['_id', 'a'], limit=3, order_type='DESC', order_fields='_id')`

SQL: `SELECT DISTINCT a FROM tbl;`  
Python: `data = db.select(table='tbl', distinct=True, fields=['a'])`


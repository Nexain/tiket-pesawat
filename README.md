# tiket-pesawat
tugas besar sistem terdistribusi | penerapan konsep rpc menggunakan RESTful API pada back-end sistem ticketing pesawat

**Endpoints :**

Customer Service Endpoints
Method | URI | Deskkripsi | Parameter / Request JSON 
--- | --- | --- | ---
`GET` | */rpc/passenger* | Mengambil semua data passenger | None 
`POST` | */rpc/passenger* | Menambah data passenger | id_passenger, name, address, username, password
`PUT` | */rpc/passenger/{id}* | Mengupdate data passenger dengan id tertentu | id_passenger, name, address, username, password
`DELETE` | */rpc/passenger/{id}* | Menghapus data passenger dengan id tertentu | None 
`POST` | */rpc/passenger/verify* | Verifikasi passenger, dapatkan informasi passenger tertentu (id_passenger, name, address) | username, password
# API Flask Web Showroom
---
### 1. Clone Repository

```bash
git clone https://github.com/deojhoniantara/api_flask_showroom_detail.git
cd api_flask_showroom_detail
```  

### 2. Setup Environment

```bash
python -m venv venv
.\venv\Scripts\activate        
pip install -r requirements.txt
```  

### 3. Setting Environment Variable
```bask
export FLASK_APP=app.py
export FLASK_ENV=development
```

### 4. Import File Database SQL (Folder stuff/)
Jalankan web server lokal (Laragon / XAMPP)  
Buka phpMyAdmin  
Buat Database "db_showroom" → Import  
Pilih file .sql dari folder stuff/  

### 5. Import Postman Collection (Folder stuff/) - Opsional
Buka Postman → Import  
Pilih file .json dari folder stuff/  

### 6. Jalankan Flask
```bash
flask run --debug
```

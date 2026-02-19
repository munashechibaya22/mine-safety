# MySQL Setup Guide

## Step 1: Install MySQL

### Windows
1. Download MySQL Installer: https://dev.mysql.com/downloads/installer/
2. Run installer and choose "Developer Default"
3. Set root password during installation
4. Complete the installation

### Alternative: XAMPP (Easier for beginners)
1. Download XAMPP: https://www.apachefriends.org/
2. Install XAMPP
3. Start MySQL from XAMPP Control Panel

## Step 2: Create Database

Open MySQL command line or phpMyAdmin (if using XAMPP):

```sql
CREATE DATABASE mine_safety CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or create a user with permissions:

```sql
CREATE DATABASE mine_safety;
CREATE USER 'mineuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON mine_safety.* TO 'mineuser'@'localhost';
FLUSH PRIVILEGES;
```

## Step 3: Update .env File

Edit your `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Comment out SQLite
# DATABASE_URL=sqlite:///./mine_safety.db

# Use MySQL
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/mine_safety
```

Replace:
- `root` with your MySQL username
- `your_password` with your MySQL password
- `localhost` with your MySQL host (usually localhost)
- `3306` with your MySQL port (default is 3306)
- `mine_safety` with your database name

## Step 4: Install MySQL Dependencies

```bash
pip install pymysql cryptography
```

Or reinstall all requirements:

```bash
pip install -r requirements.txt
```

## Step 5: Run the Application

The tables will be created automatically when you start the server:

```bash
uvicorn main:app --reload
```

## Verify Connection

Check the console output when starting the server. If there are no errors, the connection is successful!

## Troubleshooting

### Error: "Can't connect to MySQL server"
- Make sure MySQL service is running
- Check if the port is correct (default: 3306)
- Verify username and password

### Error: "Access denied for user"
- Check your username and password in .env
- Make sure the user has permissions on the database

### Error: "Unknown database"
- Create the database first using the SQL command above

## Viewing MySQL Data

### Option 1: phpMyAdmin (if using XAMPP)
- Open http://localhost/phpmyadmin
- Login with your MySQL credentials
- Select `mine_safety` database

### Option 2: MySQL Workbench
- Download: https://dev.mysql.com/downloads/workbench/
- Connect using your credentials
- Browse the `mine_safety` database

### Option 3: Command Line
```bash
mysql -u root -p
USE mine_safety;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM detections;
```

## Advantages of MySQL over SQLite

1. Better for production environments
2. Supports concurrent writes
3. Better performance for large datasets
4. Network access (can be on different server)
5. More robust for multi-user applications
6. Better backup and recovery options

# New PC Setup Guide

This guide explains how to move `AccountManager_2026` to a new Windows computer and start it safely.

If you double-click `launch_local.bat` and nothing seems to happen, the usual cause is that Python, the virtual environment, or the project dependencies are not ready yet. Follow this guide in order.

## 1. What You Need On The New PC

Install these first:

- Python 3.10 or newer
- Git, if you are cloning the project from a repository
- A browser such as Chrome or Edge
- A code editor such as VS Code, if you want to inspect files

During Python installation, make sure:

- `Add Python to PATH` is checked
- `pip` is included

## 2. Copy The Project Folder

Copy the full project folder to the new machine, for example:

```text
D:\Jatin\AccountManager_2026
```

Keep the folder structure intact.

The important files and folders are:

- `AccountManager/`
- `Software/`
- `templates/`
- `static/`
- `logo/`
- `media/`
- `db.sqlite3`
- `requirements.txt`
- `launch_local.bat`

## 3. Open The Folder

Open PowerShell or Command Prompt inside the project folder.

You should be in the same folder that contains `manage.py`.

## 4. Create A Virtual Environment

Run:

```powershell
py -3 -m venv .venv
```

If `py` is not available, use:

```powershell
python -m venv .venv
```

Then activate it:

```powershell
.venv\Scripts\activate
```

If activation is blocked in PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope Process RemoteSigned
```

and activate again.

## 5. Install Dependencies

Upgrade pip and install the project packages:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If a package fails, install the missing one manually and rerun the command.

## 6. Prepare The Database

Apply migrations:

```powershell
python manage.py migrate
```

If the copied database is already present, migrate still keeps the schema in sync with the code.

If this is a brand-new database, create a login user:

```powershell
python manage.py createsuperuser
```

If you already have the admin user and only need a password reset:

```powershell
python manage.py changepassword admin
```

## 7. Start The App Manually First

Before using the batch file, confirm the server works:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Then open:

```text
http://127.0.0.1:8000/login/
```

If this works, the project is installed correctly.

## 8. Use The One-Click Launcher

Double-click:

```text
launch_local.bat
```

What it does:

- starts the Django server in the background
- waits a few seconds
- opens the login page in the browser
- writes logs to:
  - `server.log`
  - `server.err.log`

If the browser does not open or the page does not load, check those log files.

## 9. Why `launch_local.bat` Might Show Nothing

The most common reasons are:

### A. Python is not installed

Fix:

- install Python 3.10+
- make sure it is added to PATH

Test:

```powershell
python --version
```

or

```powershell
py --version
```

### B. The virtual environment does not exist

Fix:

```powershell
py -3 -m venv .venv
.venv\Scripts\activate
```

### C. Dependencies are missing

Fix:

```powershell
python -m pip install -r requirements.txt
```

### D. Migrations are missing

Fix:

```powershell
python manage.py migrate
```

### E. Port 8000 is already in use

Fix:

```powershell
netstat -ano | findstr :8000
```

Then stop the other process or run:

```powershell
python manage.py runserver 127.0.0.1:8001
```

### F. The BAT file was launched from the wrong folder

Fix:

- make sure the BAT is run from the project folder
- or keep the launcher in the project root

### G. The browser opened, but the app is not ready yet

Fix:

- wait a few more seconds
- check `server.err.log`

## 10. First Login Checklist

After the app opens, do this:

1. Log in
2. Open `Settings`
3. Confirm firm name, address, GSTIN, contact number, logo, and bank details
4. Create or verify clients
5. Create or verify agents
6. Create sizes
7. Start billing

## 11. Backup And Restore On A New PC

The maintenance page is here:

```text
/maintenance/
```

Use it to:

- download a backup
- restore a backup
- remove invoice/payment/product data when you want a clean reset

Important:

- always keep a backup before making changes
- restore will overwrite the local database state

## 12. Common URLs

- `/login/` - login page
- `/logout/` - logout
- `/` - dashboard
- `/clients/` - clients
- `/agents/` - agents
- `/sizes/` - sizes
- `/invoices/` - invoices
- `/payments/` - payments
- `/reports/` - reports and exports
- `/firm-settings/` - settings
- `/maintenance/` - backup and cleanup

## 13. Quick Health Check

If something seems wrong, run:

```powershell
python manage.py check
```

If you want to verify the server is actually working, open:

```text
http://127.0.0.1:8000/login/
```

If that page loads, the installation is good.


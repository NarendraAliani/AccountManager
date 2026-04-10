# New PC Setup Checklist

Print this page and tick each step as you complete it.

## Before You Start

- [ ] Copy the full `AccountManager_2026` folder to the new PC
- [ ] Install Python 3.10 or newer
- [ ] Make sure Python is added to PATH
- [ ] Install Git if you need to clone updates later

## Project Setup

- [ ] Open PowerShell inside the project folder
- [ ] Create the virtual environment:

```powershell
py -3 -m venv .venv
```

- [ ] Activate it:

```powershell
.venv\Scripts\activate
```

- [ ] Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- [ ] Run database migrations:

```powershell
python manage.py migrate
```

- [ ] Create or reset the login user:

```powershell
python manage.py createsuperuser
```

or

```powershell
python manage.py changepassword admin
```

## First Run

- [ ] Start the app once manually:

```powershell
python manage.py runserver 127.0.0.1:8000
```

- [ ] Open:

```text
http://127.0.0.1:8000/login/
```

- [ ] Confirm the login page opens
- [ ] Check the firm logo and settings

## One-Click Launcher

- [ ] Double-click `launch_local.bat`
- [ ] Wait a few seconds for the browser to open
- [ ] If nothing happens, check:
  - `server.log`
  - `server.err.log`

## If It Does Not Start

- [ ] Check Python is installed:

```powershell
python --version
```

- [ ] Recreate `.venv` if needed
- [ ] Reinstall requirements if needed
- [ ] Run `python manage.py migrate`
- [ ] Check port `8000` is free

## After Login

- [ ] Open `Settings`
- [ ] Verify firm name, address, GSTIN, and contact details
- [ ] Verify the logo
- [ ] Create or verify clients
- [ ] Create or verify agents
- [ ] Create sizes
- [ ] Start billing

## Useful Links

- [Detailed new PC guide](NEW_PC_SETUP.md)
- `/login/`
- `/`
- `/clients/`
- `/invoices/`
- `/payments/`
- `/reports/`
- `/maintenance/`


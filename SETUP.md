# Setup Guide For A New PC

This guide is written for a non-technical office user.

## What You Need

- A Windows PC
- Python 3.10 or newer installed
- The full `AccountManager_2026` folder copied on the PC

You do not need Git to start the app if the folder is already copied.

## One-Click Setup

For a new PC, just double-click:

```text
Start Setup.bat
```

That single button will:

- create the virtual environment
- install all dependencies
- run the database migrations
- create or reset the default login user
- start the local server
- open the login page in the browser

Default login:

- username: `admin`
- password: `admin1234`

## Optional Desktop Icons

If you want neat desktop icons instead of batch files, double-click:

```text
Create Desktop Shortcuts.bat
```

This creates:

- `AccountManager - Start Setup`
- `AccountManager - Launch App`

Both shortcuts use the project icon so they look cleaner on the desktop.

## If You Want To Start The App Later

After the setup is done, you can also double-click:

```text
launch_local.bat
```

This starts the app and opens the login page.

## If Nothing Happens

If the button does not seem to do anything:

1. Check that Python is installed
2. Make sure the full project folder is copied
3. Confirm the `Start Setup.bat` file is inside the project folder
4. Wait a few seconds for the browser to open
5. Check `server.log` and `server.err.log` in the project folder

## Quick Manual Check

If you want to test the app manually, open PowerShell in the project folder and run:

```powershell
python manage.py runserver 127.0.0.1:8000
```

Then open:

```text
http://127.0.0.1:8000/login/
```

## After Login

Once logged in, the normal order is:

1. Check `Settings`
2. Confirm the logo, address, GSTIN, and contact details
3. Create clients if needed
4. Create agents if needed
5. Create sizes if needed
6. Start billing

## Help Pages

- [Detailed setup guide](NEW_PC_SETUP.md)
- [Printable checklist](NEW_PC_CHECKLIST.md)

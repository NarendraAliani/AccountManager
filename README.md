# AccountManager 2026

`AccountManager_2026` is a Django-based billing and ledger app for Gurukrupa Enterprise. It is built around a small accounting workflow:

- maintain clients, agents, products, and sizes
- create taxable and non-taxable invoices
- record payments against clients
- track debit balance per client
- view ledgers by client, agent, and product
- print invoice formats for the shop

## What It Does

### Core records

- **Clients** store name, address, mobile, GSTIN, state code, and running debit balance.
- **Agents** store the sales/commission agent name and mobile number.
- **Products** store item names and optional HSN codes.
- **Sizes** store size labels used on invoice line items.

### Billing

- Create invoices with multiple line items.
- Mark invoices as taxable or non-taxable.
- Auto-generate invoice numbers with `Tx###` or `Nt###` prefixes.
- Apply invoice-level discounts.
- Compute CGST, SGST, IGST, and final totals.
- Update client debit balance when invoices and payments are saved.

### Payments

- Record client payments with amount, method, and description.
- Update the client debit balance when payments are posted or edited.

### Ledgers and reporting

- Client ledger shows bills and payments together.
- Agent ledger shows all bills linked to that agent.
- Product ledger shows every invoice line item containing that product.
- Main list pages support DataTables sorting, searching, scrolling, and CSV export.

### Status toggles

- Invoice and payment rows can be toggled between pending and cleared from the UI.
- These toggles are handled through small AJAX endpoints.

### Printing

- The invoice detail page includes a dedicated print layout.
- The print view is split into pages when item counts exceed the per-page limit.

### Maintenance and backup

- The app includes a maintenance screen at `/maintenance/`.
- You can download a full ZIP backup of the SQLite database and media files.
- You can restore from a previously downloaded ZIP backup.
- You can also truncate all company data from the maintenance page after a strong confirmation prompt.
- `launch_local.bat` starts the local server and opens the browser for single-click use on office PCs.

## Tech Stack

- **Backend:** Django
- **Database:** SQLite (`db.sqlite3`)
- **Frontend:** Bootstrap, Paper Dashboard, jQuery, DataTables, Selectize, Font Awesome

## Project Layout

- `AccountManager/` - Django project settings, URLs, and WSGI entry point
- `Software/` - main billing app, models, forms, views, admin registration, migrations
- `templates/` - all HTML templates for the UI
- `static/` - local CSS, JS, fonts, and favicon assets
- `db.sqlite3` - bundled SQLite database

## Setup

See the full setup guide in [SETUP.md](SETUP.md).
If you are moving the app to a new machine, follow [NEW_PC_SETUP.md](NEW_PC_SETUP.md) for the exact copy/install/start steps, or print [NEW_PC_CHECKLIST.md](NEW_PC_CHECKLIST.md) for an office-friendly step list.

For a true one-click first-time install on a new PC, double-click [Start Setup.bat](Start%20Setup.bat).

Quick start:

1. Create and activate a virtual environment.
2. Install the project dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a login account if the database is new:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the local server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
6. Open `http://127.0.0.1:8000/` and log in.

## Notes

- This codebase started as an older Django 1.x project, but it has been updated to run on modern Django.
- The project now includes a local `selectize.min.js` asset so the searchable dropdowns work without an external dependency.
- `manage.py check` passes in the current workspace.
- The database is empty in this checkout, so you will need to create clients, products, sizes, agents, invoices, and payments before the ledgers become meaningful.

## Main Routes

- `/invoices/` - invoice list
- `/invoices/new` - create invoice
- `/invoices/<id>` - invoice detail and print view
- `/clients/` - client list
- `/clients/new` - create client
- `/clients/<id>` - client ledger
- `/clients/<id>/edit` - edit client
- `/agents/` - agent list
- `/agents/new` - create agent
- `/agents/<id>` - agent ledger
- `/products/` - product list
- `/products/new` - create product
- `/products/<id>` - product ledger
- `/payments/` - payment list
- `/payments/new` - create payment
- `/payments/<id>` - payment detail
- `/payments/<id>/edit` - edit payment
- `/sizes/` - size master
- `/reports/` - reporting dashboard and exports
- `/maintenance/` - backup and restore screen
- `/admin/` - Django admin


## Users

- username: admin
- password: admin1234

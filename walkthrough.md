# Walkthrough

This walkthrough follows the normal accounting flow in the app from master data setup to invoice printing and ledger review.

## 1. Log In

- Open the site and sign in through Django admin authentication.
- The sidebar only becomes fully useful after login.
- If you are not logged in, the base layout shows a login prompt.

## 2. Create Master Data

Before invoices and payments, create the reference records the app uses:

- **Clients** at `/clients/new`
- **Agents** at `/agents/new`
- **Products** at `/products/new`
- **Sizes** at `/sizes/`

You can also create products and sizes during invoice entry using the searchable dropdowns.

### Client fields

- Name
- Address
- State
- Mobile
- GSTIN

### Agent fields

- Name
- Mobile

### Product fields

- Item name
- HSN code

### Size fields

- Size label only

## 3. Create an Invoice

Go to `/invoices/new`.

### Header section

- Pick a client.
- Enter delivery date.
- Add place of supply.
- Add transport mode.
- Add vehicle number.
- Pick or type an agent.
- Enter optional parcel digits.
- Mark the invoice taxable if needed.

The client dropdown is searchable, and the page fills in client name, address, state, mobile, and GSTIN after selection.

### Line items

- Add one or more rows using the formset.
- Each row needs:
  - product
  - size
  - quantity
  - rate

The UI calculates line totals, quantity total, discount value, and discounted amount before submission.

### Saving behavior

- Invoice numbers are auto-generated with a taxable or non-taxable prefix.
- Invoice totals are calculated in the view, not in the template.
- Client debit balance increases by the invoice total.
- Product, size, and agent names can be created on the fly if they do not already exist.

## 4. Review the Invoice

Open `/invoices/<id>` after saving.

This page shows:

- invoice metadata
- client details
- shipping and transport details
- itemized invoice table
- tax summary
- total in words

You can also:

- print the invoice
- edit the invoice
- add a payment
- jump to the client ledger

## 5. Print the Invoice

Use the **Print Invoice** button on the invoice detail page.

The print layout includes:

- shop name and address
- invoice header
- line items
- tax breakdown
- totals in words

The print template automatically inserts a page break when item counts exceed the page limit.

## 6. Record a Payment

Go to `/payments/new`.

Enter:

- client
- amount
- payment method
- description

When saved:

- the payment is stored
- the client debit balance decreases by the payment amount

## 7. Check the Client Ledger

Open `/clients/<id>`.

The ledger combines:

- all bills for that client
- all payments for that client

The page also calculates the current debit balance from the visible bills and payments.

### Status toggles

- Click the status icon in a bill or payment row to mark it cleared or pending.
- The change happens through the AJAX endpoint under `/api/...`.

### Useful actions

- export ledger data to CSV
- go to the edit client form
- open the payment form

## 8. Check the Agent Ledger

Open `/agents/<id>`.

This view lists all bills associated with the agent and supports CSV export plus quick navigation to client records.

## 9. Check the Product Ledger

Open `/products/<id>`.

This view shows every invoice line item that uses the product, grouped as a ledger-style table.

## 10. Manage Sizes

Open `/sizes/`.

This page is both:

- a master-data entry form for adding new sizes
- a list of all current sizes

## Data Flow Summary

- **Invoice created** -> client debit increases
- **Payment created** -> client debit decreases
- **Invoice/payment cleared toggle** -> status icon changes without a full form submit
- **Ledger pages** -> summarize the stored bills and payments

## API Endpoints Used by the UI

- `/api/client/<id>` - returns client details for invoice and payment forms
- `/api/product/<name>` - creates or finds a product for inline entry
- `/api/size/<name>` - creates or finds a size for inline entry
- `/api/invoices/<id>` - toggles invoice cleared status
- `/api/payments/<id>` - toggles payment cleared status

## Practical Notes

- The app is designed for a small, local billing workflow rather than a multi-tenant SaaS setup.
- Most business logic lives in the Django views and model helper methods.
- The SQLite database bundled in the repo is empty in this checkout, so the first useful step is usually creating master records.


import frappe
from frappe.utils import nowdate, getdate, formatdate
from frappe.utils.background_jobs import enqueue

def update_ticket_gate_numbers(flight_name, new_gate_number):
    # Fetch and update all tickets related to this flight
    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight_name}, fields=["name"])
    
    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", new_gate_number)
    
    frappe.db.commit()
def generate_rent_payments():
    today = getdate()
    current_month = today.strftime("%b")  # Jan, Feb, etc.

    tenants = frappe.get_all("Tenant", fields=["name", "shop"])
    rent = frappe.db.get_single_value("Airport Settings", "default_rent_amount")

    for tenant in tenants:
        exists = frappe.db.exists("Rent Payment", {
            "tenant": tenant.name,
            "payment_month": current_month
        })

        if not exists:
            payment = frappe.get_doc({
                "doctype": "Rent Payment",
                "tenant": tenant.name,
                "shop": tenant.shop,
                "payment_month": current_month,
                "amount_paid": rent
            })
            payment.insert()
            payment.submit()

            # Email reminder if enabled
            if frappe.db.get_single_value("Airport Settings", "enable_reminders"):
                send_rent_reminder(tenant.name, tenant.shop, rent, current_month)

def send_rent_reminder(tenant_name, shop_name, amount, month):
    tenant_doc = frappe.get_doc("Tenant", tenant_name)
    email = tenant_doc.email_id
    if not email:
        return

    subject = f"Rent Due Reminder for {month}"
    message = f"""Dear {tenant_doc.tenant_name},<br><br>
Your rent of ₹{amount} for shop <b>{shop_name}</b> is due for the month of {month}.<br>
Please make the payment at your earliest convenience.<br><br>
Regards,<br>Airport Admin"""

    frappe.sendmail(
        recipients=[email],
        subject=subject,
        message=message
    )

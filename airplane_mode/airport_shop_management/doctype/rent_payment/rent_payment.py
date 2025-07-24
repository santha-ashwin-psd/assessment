# Copyright (c) 2025, Santha Ashwin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
	def validate(self):
		if not self.amount_paid:
			self.amount_paid = frappe.db.get_single_value("Airplane Mode Settings", "default_rent_amount") or 0


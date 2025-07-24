# Copyright (c) 2025, Santha Ashwin and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.naming import make_autoname
from frappe.utils.background_jobs import enqueue

class AirplaneFlight(WebsiteGenerator):
	def before_submit(self):
		self.status = "Completed"
	def on_update(self):
		old_doc = self.get_doc_before_save()
		if old_doc and old_doc.gate_number != self.gate_number:
			enqueue(
				"airplane_mode.utils.update_ticket_gate_numbers",
				flight_name=self.name,
				new_gate_number=self.gate_number,
				queue='default'
			)
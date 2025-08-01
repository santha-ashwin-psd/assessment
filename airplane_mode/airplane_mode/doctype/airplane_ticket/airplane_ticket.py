# Copyright (c) 2025, Santha Ashwin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random

class AirplaneTicket(Document):
	def before_insert(self):
		self.populate_seat()
	def validate(self):
		b = [i.item for i in self.add_ons]
		for j in b:
			if b.count(j) > 1:
				frappe.throw("You can't buy the same item twice")

		if not self.flight:
			return  # no flight selected yet

		# Fix: get airplane through flight
		flight_doc = frappe.get_doc("Airplane Flight", self.flight)
		airplane = frappe.get_doc("Airplane", flight_doc.airplane)
		capacity = airplane.capacity

		# Count existing tickets
		existing_tickets = frappe.get_all(
			"Airplane Ticket",
			filters={
				"flight": self.flight,
				"name": ["!=", self.name]
			},
			limit=0
		)

		if len(existing_tickets) >= capacity:
			frappe.throw(f"Cannot book ticket: Flight {self.flight} has reached its maximum capacity of {capacity} seats.")
	def before_save(self):
		total=0
		for i in self.add_ons:
			total += i.amount
		self.total_price = self.flight_price + total
	def before_submit(self):
		if self.status == "Boarded":
			pass
		else:
			frappe.throw("You can't submit without boarded")
	def populate_seat(self):
		ran_no = random.randint(10,99)
		ran_let = random.choice(["A","B","C","D","E","F"])
		self.seat = f"{ran_no}{ran_let}"
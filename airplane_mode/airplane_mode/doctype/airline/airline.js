// Copyright (c) 2025, Santha Ashwin and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airline", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Airline', {
    refresh(frm) {
        if (frm.doc.website) {
            frm.add_custom_button('Visit Website', () => {
                window.open(frm.doc.website, '_blank');
            }).addClass('btn-primary');
        }
    }
});
// Copyright (c) 2025, Santha Ashwin and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Flight", {
// 	refresh(frm) {
// Api secret731a23c88ae9360  Api key e2c311840f8904e
// 	},
// });
frappe.ui.form.on('Flight Crew Member', {
    form_render: function(frm, cdt, cdn) {
        // Set query when the row is rendered
        frappe.meta.get_docfield("Flight Crew Member", "crew_member", frm.doc.name).get_query = function() {
            return {
                query: "frappe.core.doctype.user.user.user_query",
                filters: {
                    'role': 'Flight Crew Member'
                }
            };
        };
    }
});
frappe.ready(function() {
	frappe.call({
    method: 'frappe.client.get',
    args: {
        doctype: 'Shop',
        name: shop
    },
    callback: function(r) {
        if (r.message) {
        frappe.web_form.set_value('shop_name', r.message.shop_name);
        frappe.web_form.set_value('shop_number', r.message.name);
        frappe.web_form.set_value('area', r.message.area);
        frappe.web_form.set_value('airport', r.message.airport);
        }
    }
    });

})
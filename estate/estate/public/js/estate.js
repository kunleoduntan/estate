frappe.ui.form.on('ScanCreate', {
    refresh: function(frm) {
        frm.add_custom_button(__('Scan Doc'), function() {
            // Call the server-side function with the document (frm.doc) and method
            frappe.call({
                method: "estate.tasks.extract_text_from_file", // Make sure to use the correct path
                args: {
                    doc: frm.doc,  // Pass the current document
                    method: 'extract_text_from_file'
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__('Scan completed successfully!'));
                    }
                },
                error: function(error) {
                    frappe.msgprint(__('Error while scanning document.'));
                }
            });
        });
    }
});


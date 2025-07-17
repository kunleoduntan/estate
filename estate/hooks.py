from . import __version__ as app_version

app_name = "estate"
app_title = "Estate Management"
app_publisher = "Kunle Oduntan	"
app_description = "Estate Management App"
app_email = "Kunleoduntan@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/estate/css/estate.css"
# app_include_js = "/assets/estate/js/estate.js"

# include js, css files in header of web template
# web_include_css = "/assets/estate/css/estate.css"
# web_include_js = "/assets/estate/js/estate.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "estate/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}


# include js in doctype views
doctype_js = {"ScanCreate" : "public/js/estate.js"}
#doctype_js = {"Bank Reconciliation" : "public/js/estate.js"}
#doctype_list_js = {"Sales Invoice" : "public/js/insurance_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "estate.utils.jinja_methods",
#	"filters": "estate.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "estate.install.before_install"
# after_install = "estate.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "estate.uninstall.before_uninstall"
# after_uninstall = "estate.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "estate.utils.before_app_install"
# after_app_install = "estate.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "estate.utils.before_app_uninstall"
# after_app_uninstall = "estate.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "estate.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events




doc_events = {
    "ScanCreate": {
        
        "validate": "estate.tasks.scan_document",
        
        #"validate": "estate.tasks.parse_pdf_text",
        #"validate": "estate.tasks.extract_text_from_pdf",
        #"validate": "estate.tasks.parse_pdf_text",
        "validate": "estate.tasks.create_document_from_scan",
        #"validate": "estate.tasks.extract_text_from_pdf",
       # "on_submit": "estate.tasks.make_jv",
        
    }
    
    
}




# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "*/2 * * * *": [
            "estate.tasks.upload_attendance",
            "estate.tasks.update_exchange_rates_from_xe"
        ]
    }
}


# scheduler_events = {
#	"all": [
#		"estate.tasks.all"
#	],
#	"daily": [
#		"estate.tasks.daily"
#	],
#	"hourly": [
#		"estate.tasks.hourly"
#	],
#	"weekly": [
#		"estate.tasks.weekly"
#	],
#	"monthly": [
#		"estate.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "estate.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "estate.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "estate.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["estate.utils.before_request"]
# after_request = ["estate.utils.after_request"]

# Job Events
# ----------
# before_job = ["estate.utils.before_job"]
# after_job = ["estate.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"estate.auth.validate"
# ]

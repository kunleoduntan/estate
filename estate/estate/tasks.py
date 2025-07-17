

import frappe
from frappe import _
import pdfplumber
import PyPDF2
import re
import os
from io import BytesIO
from datetime import datetime
import dateutil.parser
import frappe
import requests
from bs4 import BeautifulSoup
from frappe.utils import get_url
import requests
import pandas as pd
import pyodbc
from frappe.utils.background_jobs import enqueue

    
import frappe
from frappe.utils.file_manager import get_file
from frappe.utils import getdate, cstr
import openpyxl


# Your OCR.Space API Key
OCR_SPACE_API_KEY = 'K85231999088957'  # Replace with your actual OCR.Space API Key

@frappe.whitelist()

def _extract_text_from_file(full_file_url):
    """Internal function to use OCR.Space API to extract text from a file URL."""
    try:
        api_url = 'https://api.ocr.space/parse/imageurl'

        payload = {
            'url': full_file_url,
            'apikey': OCR_SPACE_API_KEY,
            'language': 'eng',
            'isOverlayRequired': False,
        }

        response = requests.post(api_url, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        result = response.json()

        if result.get('IsErroredOnProcessing'):
            frappe.log_error(f"OCR Error: {result.get('ErrorMessage')}")
            return None

        parsed_results = result.get('ParsedResults')
        if not parsed_results:
            return None

        return parsed_results[0]['ParsedText']

    except requests.exceptions.RequestException as e:
        frappe.log_error(f"OCR API request failed: {str(e)}")
        return None


@frappe.whitelist()
def extract_text_from_file(full_file_url):
    """Whitelisted version for API calls"""
    return _extract_text_from_file(full_file_url)


def parse_main_document_info(text):
    """Parse main document fields from extracted OCR text."""
    return {
        'partner_name': extract_partner_name(text),
        'invoice_number': extract_invoice_number(text),
        'invoice_date': extract_invoice_date(text),
        'grand_total': extract_grand_total(text)
    }


def extract_partner_name(text):
    """Extract partner name from the document text."""
    lines = text.split('\n')
    for line in lines:
        if any(keyword in line for keyword in ["Ltd", "Inc", "Company", "LLC", "Corp"]):
            return line.strip()
    return lines[0].strip() if lines else ''


def extract_invoice_number(text):
    """Find a line containing Invoice Number."""
    lines = text.split('\n')
    for line in lines:
        if "Invoice" in line and any(char.isdigit() for char in line):
            numbers = re.findall(r'(?:Invoice|INV|#)\s*[:#]?\s*([A-Z0-9-]+)', line, re.IGNORECASE)
            if numbers:
                return numbers[0]
    return ''


def extract_invoice_date(text):
    """Find a line containing a date."""
    date_patterns = [
        r'\d{2}[/-]\d{2}[/-]\d{4}',  # DD/MM/YYYY or DD-MM-YYYY
        r'\d{4}[/-]\d{2}[/-]\d{2}',  # YYYY/MM/DD or YYYY-MM-DD
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'  # Month Day, Year
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return ''


def extract_grand_total(text):
    """Find a line with Grand Total or Total."""
    lines = text.split('\n')
    total_patterns = [
        r'(?:Grand\s*Total|Total\s*Amount|Amount\s*Due)\D*([\d,]+\.\d{2})',
        r'(?:Total)\D*([\d,]+\.\d{2})'
    ]
    for line in lines:
        for pattern in total_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).replace(',', '')
    return ''

"""
@frappe.whitelist()
def upload_attendance():
    # Path to the Excel file
    file_path = "C:\Users\PC\Documents\VIC/Attendance Test Document.xlsx"

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Process each row in the Excel file
    for index, row in df.iterrows():
        # Check if an attendance record already exists for the employee and date
        attendance = frappe.get_value("Attendance", {"employee": row["Employee ID"], "attendance_date": row["Date"]}, "name")

        if attendance:
            # Update the existing attendance record
            attendance_doc = frappe.get_doc("Attendance", attendance)
            attendance_doc.attendance_date = row["Date"]
            attendance_doc.in_time = row["Time In"]
            attendance_doc.out_time = row["Time Out"]
            attendance_doc.save(ignore_permissions=True)
        else:
            # Create a new attendance record
            attendance_doc = frappe.get_doc({
                "doctype": "Attendance",
                "employee": row["Employee ID"],
                "attendance_date": row["Date"],
                "status": row["Status"],
                "in_time": row["Time In"],
                "out_time": row["Time Out"]
            })
            attendance_doc.insert(ignore_permissions=True)

        frappe.db.commit()

    return "Attendance records created and updated successfully."
"""

@frappe.whitelist()
def upload_attendance():
    server = "Server=DESKTOP-2VPR9IB\\BCDEMO;"
    database = 'agility'
    #username = 'YOUR_USERNAME'
    #password = 'YOUR_PASSWORD'
    driver = '{ODBC Driver 17 for SQL Server}'
    "Trusted_Connection=yes;"

    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT employee_id, attendance_date, status, time_in, time_out
        FROM Attendance
    """)
    rows = cursor.fetchall()

    for row in rows:
        employee_id = row.employee_id
        attendance_date = row.attendance_date
        status = row.status
        time_in = row.time_in
        time_out = row.time_out

        attendance = frappe.get_value(
            "Attendance",
            {"employee": employee_id, "attendance_date": attendance_date},
            "name"
        )

        if attendance:
            attendance_doc = frappe.get_doc("Attendance", attendance)
            attendance_doc.attendance_date = attendance_date
            attendance_doc.in_time = time_in
            attendance_doc.out_time = time_out
            attendance_doc.save(ignore_permissions=True)
        else:
            attendance_doc = frappe.get_doc({
                "doctype": "Attendance",
                "employee": employee_id,
                "attendance_date": attendance_date,
                "status": status,
                "in_time": time_in,
                "out_time": time_out
            })
            attendance_doc.insert(ignore_permissions=True)

        frappe.db.commit()

    cursor.close()
    conn.close()

    frappe.logger().info("Attendance records created and updated successfully.")

    
    

@frappe.whitelist()
def update_exchange_rates_from_xe():
    url = "https://www.xe.com/currencytables/?from=NGN&date=2025-05-02#table-section"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table section
        table = soup.find("table", class_="currencytables__Table-sc-1xq0k7p-1")
        if not table:
            frappe.throw("Could not find exchange rate table on XE.com")

        rows = table.find_all("tr")[1:]  # Skip header row

        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 4:
                continue  # Skip malformed rows

            currency = cols[0].text.strip()
            name = cols[1].text.strip()
            units_per_ngn = float(cols[2].text.strip().replace(",", ""))
            ngn_per_unit = float(cols[3].text.strip().replace(",", ""))

            # Check if already exists (optional)
            if not frappe.db.exists("Exchange Rate", {"currency": currency}):
                exchange_rate = frappe.new_doc("Exchange Rate")
                exchange_rate.currency = currency
                exchange_rate.name1 = name  # if your field is `name`, ERPNext may treat it as primary key
                exchange_rate.units_per_ngn = units_per_ngn
                exchange_rate.ngn_per_unit = ngn_per_unit
                exchange_rate.insert()
                frappe.db.commit()
            else:
                # Optional: update if already exists
                doc = frappe.get_doc("Exchange Rate", {"currency": currency})
                doc.units_per_ngn = units_per_ngn
                doc.ngn_per_unit = ngn_per_unit
                doc.save()
                frappe.db.commit()

        frappe.msgprint("Exchange Rates updated successfully from XE.com")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "XE Exchange Rate Sync Failed")
        #frappe.throw(f"Failed to update exchange rates: {str(e)}")


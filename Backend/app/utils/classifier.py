# Simple rule-based classifier for column names to categorize them into types of data. 
# This is a basic implementation and can be expanded with more rules or using machine learning for better accuracy.
# The function takes a column name as input and returns a category based on the presence of certain keywords in the column name.
# For example, if the column name contains "name", it is classified as "Personal Data". If it contains "email", it is classified as "Contact Data", and so on.

import re


# Column name classification
def classify_column(column_name):

    column_name = column_name.lower()

    if "name" in column_name:
        return "Personal Data"

    elif "email" in column_name:
        return "Contact Data"

    elif "phone" in column_name:
        return "Contact Data"

    elif "salary" in column_name:
        return "Financial Data"

    elif "country" in column_name:
        return "Location Data"

    else:
        return "General Data"


# Sensitive data detection from sample value
def detect_sensitive_data(value):

    if value is None:
        return "Unknown"

    value = str(value)

    # Email
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        return "Email"

    # Phone number
    if re.match(r'^\d{10}$', value):
        return "Phone Number"

    # PAN
    if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', value):
        return "PAN Number"

    # Aadhaar
    if re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', value):
        return "Aadhaar Number"

    # Credit Card
    if re.match(r'^\d{16}$', value):
        return "Credit Card"

    # IP Address
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', value):
        return "IP Address"

    return "General Data"
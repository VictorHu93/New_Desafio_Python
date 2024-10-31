# services.py
from datetime import date

def calculate_fees(loan_date, return_date=None):
    if not return_date:
        return_date = date.today()
    days_late = (return_date - loan_date).days - 3

    if days_late <= 0:
        return {"multa": 0, "juros": 0}
    elif days_late <= 3:
        return {"multa": 3, "juros": 0.2}
    elif days_late <= 5:
        return {"multa": 5, "juros": 0.4}
    else:
        return {"multa": 7, "juros": 0.6}


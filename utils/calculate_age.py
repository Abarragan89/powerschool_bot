import datetime

def calculate_age(birth_date):
    # Assuming birth_date is in "MM/DD/YYYY" format
    birth_month, __, birth_year = map(int, birth_date.split("/"))
    
    # School reference date: August of the current year
    current_year = datetime.datetime.now().year
    reference_month = 8  # August

    # If it's before August, use last year's school year
    if datetime.datetime.now().month < reference_month:
        current_year -= 1  

    # Calculate age in years
    age_years = current_year - birth_year

    # Calculate months from last August
    if birth_month > reference_month:  # Born after August
        age_years -= 1
        age_months = (12 - birth_month) + reference_month
    else:  # Born in August or before
        age_months = reference_month - birth_month

    return f"{age_years}.{age_months}"
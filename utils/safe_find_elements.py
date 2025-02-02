from selenium.webdriver.common.by import By

def safe_find_element_value(parent, by, value):
    """Tries to find an element and return its text or attribute. Returns None if not found."""
    try:
        element = parent.find_element(by, value)
        return element.text if by == By.TAG_NAME else element.get_attribute("value")
    except Exception:  # Catch NoSuchElementException or other errors
        return None
    
def safe_find_element(parent, by, value):
    """Tries to find an element. Returns None if not found."""
    try:
        return parent.find_element(by, value)
    except Exception:  # Catch NoSuchElementException or other errors
        return None
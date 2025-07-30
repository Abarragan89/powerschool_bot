from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import get_data_file
from utils.safe_find_elements import safe_find_element_value, safe_find_element
from utils.cryption import encrypt_and_save_credentials, load_and_decrypt_credentials
import time
import json 

def get_student_demographics(username='', password='', controller=None):
    """Save & encrypt credentials and initialize class"""
    if not username or not password:
        try:
            username, password = load_and_decrypt_credentials()
        except:
            return
    
    if not username or not password:
        return

    encrypt_and_save_credentials(username, password)

    CLASS_DEMOGRAPHICS_JSON = {}

    # Keep Chrome Browser open after program finishes
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://villagecharter.powerschool.com/teachers/pw.html")


    username_field = driver.find_element(By.NAME, value='username')
    password_field = driver.find_element(By.NAME, value='password')
    submit_btn = driver.find_element(By.ID, value='btnEnter')

    username_field.send_keys(username)
    password_field.send_keys(password)
    submit_btn.click()

    # Wait for the PowerTeacherPro link to be clickable
    power_teacher_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'navPowerTeacherPro'))
    )
    # click into attendance
    power_teacher_link.click()

    # Wait for the modal backdrop to disappear
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'modal-backdrop'))
    )
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-backdrop"))
    )
    # Use JavaScript to hide all modal backdrops
    driver.execute_script("""
        var backdrops = document.getElementsByClassName('modal-backdrop');
        for (var i = 0; i < backdrops.length; i++) {
            backdrops[i].style.display = 'none';
        }
    """)

    time.sleep(1)

    # Wait for the students side nave link to be clickable
    student_side_nav_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'sidebar-charms-students'))
    )
    # click into student side nav view
    student_side_nav_link.click()
    
    # Click on demographics to see first student data
    driver.find_element(By.ID, 'students-psx.html.teachers_powerteacherpro_students.demo.demographics-link').click()

    is_scraping = True
    # This will be the logic that loops collects data and clicks next arrow
    while is_scraping:
        time.sleep(1)
        # Get the div that the student deomgraphics is located
        student_demo_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'student-demographics-accordion-group'))
        )
        student_number = student_demo_div.find_element(By.ID, 'demo_student_studentnum').get_attribute('value'),
        
        ## return if it already went all the way around
        if CLASS_DEMOGRAPHICS_JSON.get(student_number[0]):
            is_scraping = False
            continue

        student_data = {
            "name": safe_find_element_value(student_demo_div, By.ID, 'demo_student_name'),
            "gender": safe_find_element_value(student_demo_div, By.ID, 'demo_student_gender'),
            "age": safe_find_element_value(student_demo_div, By.ID, 'demo_student_age'),
            "dob": safe_find_element_value(student_demo_div, By.ID, 'demo_student_dob'),
            "street": safe_find_element_value(student_demo_div, By.ID, 'demo_student_address_street'),
            "city": safe_find_element_value(student_demo_div, By.ID, 'demo_student_address_city'),
            "state": safe_find_element_value(student_demo_div, By.ID, 'demo_student_address_state'),
            "zip": safe_find_element_value(student_demo_div, By.ID, 'demo_student_address_zip'),
            "phone": safe_find_element_value(student_demo_div, By.ID, 'demo_student_phone'),
            "contact_one": {},
            "contact_two": {}
        }

        # Get first contact accordion
        contact_one_accordion = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'student-contacts-accordion-0'))
        )

        # Safely fetching contact_one data
        student_data['contact_one'] = {
            "name": safe_find_element_value(contact_one_accordion, By.TAG_NAME, 'h3'),
            "relationship": safe_find_element_value(contact_one_accordion, By.ID, 'contact-relationship-0'),
            "phone": safe_find_element_value(contact_one_accordion, By.ID, 'contact-phone-0-0'),
            "email": safe_find_element_value(contact_one_accordion, By.ID, 'contact-email-0-0'),
        }

        # only get second contact if it exists
        contact_two_accordion = safe_find_element(driver, By.ID, 'student-contacts-accordion-1')
    
        if contact_two_accordion:
            contact_two_accordion.find_element(By.CLASS_NAME, "accordion-toggle").click()
            student_data['contact_two'] = {
                "name": safe_find_element_value(contact_two_accordion, By.TAG_NAME, 'h3'),
                "relationship": safe_find_element_value(contact_two_accordion, By.ID, 'contact-relationship-1'),
                "phone": safe_find_element_value(contact_two_accordion, By.ID, 'contact-phone-1-0'),
                "email": safe_find_element_value(contact_two_accordion, By.ID, 'contact-email-1-0'),
            }
        else:
            student_data['contact_two'] = None  

        CLASS_DEMOGRAPHICS_JSON[student_number[0]] = student_data

        # Click Next Button
        driver.find_element(By.ID, 'studentJumpNext').click()
    
    with open(get_data_file('data/class_demo.txt'), 'w') as file:
        json.dump(CLASS_DEMOGRAPHICS_JSON, file, indent=4)
    
    if controller:
        controller.show_frame("Dashboard")
    driver.quit()


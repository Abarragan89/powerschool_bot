from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from utils.cryption import load_and_decrypt_credentials
import time

def take_attendance(tardies, absences):
    # Get user credentials
    USERNAME, PASSWORD = load_and_decrypt_credentials()

    # Keep Chrome Browser open after program finishes
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://villagecharter.powerschool.com/teachers/pw.html")


    username_field = driver.find_element(By.NAME, value='username')
    password_field = driver.find_element(By.NAME, value='password')
    submit_btn = driver.find_element(By.ID, value='btnEnter')

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    submit_btn.click()

    # Wait for the attendance link to be clickable
    take_attendance_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'attLink474'))
    )
    # click into attendance
    take_attendance_link.click()
    student_table_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="attendance-table"]/tbody'))
    )

    student_rows = student_table_el.find_elements(By.CLASS_NAME, value='studentrow')

    for student_row in student_rows:
        student_name = student_row.find_element(By.CLASS_NAME, value='cvDemarcation').text
        
        # need to click on this input first to show the select
        try:
            input_field = student_row.find_element(By.CLASS_NAME, value='left').find_element(By.TAG_NAME, value='input')
            # if not found, attendance is already set and saved, no input button visible
            if not input_field:
                continue
            else:
                input_field.click()
        except:
            continue

        # I need to wait until select is there
        drop_down = WebDriverWait(student_row, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'select'))
        )

        # Create drop_down
        drop_down = Select(drop_down)

        # select tardy
        if student_name in tardies:
            drop_down.select_by_value('T')
        elif student_name in absences:
            drop_down.select_by_value('UA')
        else:
            drop_down.select_by_value('P')

    confirm_attendance = driver.find_element(By.ID, value='btnSubmit')
    confirm_attendance.click()

    time.sleep(5)

    driver.quit()
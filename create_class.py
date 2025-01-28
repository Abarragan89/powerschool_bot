from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import os

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")

def create_class():
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

    # get student rows
    student_rows = student_table_el.find_elements(By.CLASS_NAME, value='studentrow')

    # collect student names
    with open('class_roster.txt', 'w') as file:
        for num, student_row in enumerate(student_rows):
            student_name = student_row.find_element(By.CLASS_NAME, value='cvDemarcation').text
            if num == len(student_rows) - 1:
                file.write(f"{student_name}")
            else:
                file.write(f"{student_name}\n")
    driver.quit()

create_class()
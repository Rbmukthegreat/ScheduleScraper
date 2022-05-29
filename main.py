from selenium import webdriver
from time import sleep
from class_skeleton import ClassList
from class_skeleton import Class

def main():
    driver = webdriver.Chrome()
    
    URL_BASE = "https://myplan.uw.edu/course/#/courses/"
    CLASS = "MATH441"
    QUARTER = "Autumn" # NOTE: First letter must be uppercase, the rest must be lowercase. Options: Summer, Autumn, Winter, Spring

    driver.get(URL_BASE + CLASS)

    sleep(4)

    quarters = driver.find_elements_by_xpath("//*[@class=\"mb-0 table table-borderless\"]")
    
    quarter = None
    for i in range(len(quarters)):
        if QUARTER in quarters[i].find_element_by_xpath('.//caption').text:
            quarter = quarters[i].find_elements_by_xpath(".//tbody")

    if quarter is None:
        print("This course isn't offered this quarter!")
        quit()

    c = ClassList(CLASS, quarter) 
    print(len(c.classlist))
    print(c.to_string())

    driver.close()

def format_string(s: str) -> str:
    s = s[:-3]
    if (len(s) < 5):
        s = "0" + s
    return s

if __name__ == "__main__":
    main()

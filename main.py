from selenium import webdriver
from time import sleep
from class_skeleton import ClassList
from class_skeleton import Class
import multiprocessing as mp

URL_BASE = "https://myplan.uw.edu/course/#/courses/"
QUARTER = "Autumn" # Summer, Autumn, Winter, Spring

def search_classes(CLASS):
    driver = webdriver.Chrome()

 #   for (CLASS, type) in CLASSES:
    driver.get(URL_BASE + CLASS[0])
 
    sleep(6)
  
    quarters = driver.find_elements_by_xpath("//*[@class=\"mb-0 table table-borderless\"]")
    
    quarter = None
    for i in range(len(quarters)):
        if QUARTER in quarters[i].find_element_by_xpath('.//caption').text:
            quarter = quarters[i].find_elements_by_xpath(".//tbody")
  
    if quarter is None:
        print("This course isn't offered this quarter!")
        quit()
  
    c = ClassList(CLASS[0], quarter, CLASS[1]) 
    print(len(c.classlist))
    print(c.to_string() + "\n\n\n")
 
    driver.close()
    return

def main():
    CLASSES = [("MATH334", ""), ("ENGL182", ""), ("PHYS121", "LECTURE"), ("PHYS121", "QUIZ"), ("PHYS121", "LABORATORY"), ("CSE143", "")]

#    CLASSES_LIST = []
#    for i in range(0, len(CLASSES) - 1, 2):
#        CLASSES_LIST.append(CLASSES[i:i+2])
#    if len(CLASSES) % 2 == 1:
#        CLASSES_LIST.append([CLASSES[len(CLASSES) - 1]])

    num_processes = len(CLASSES)
    mp.set_start_method("spawn")
#    q = mp.Queue()
    for i in range(num_processes):
       p = mp.Process(target=search_classes, args=(CLASSES[i],)) 
       p.start()

if __name__ == "__main__":
    main()

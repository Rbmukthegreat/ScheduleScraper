def format_string(s: str) -> str:
    s = s[:-3]
    if (len(s) < 5):
        s = "0" + s
    return s

def get_times(quarter):
    times = { "Monday": {"start": "00:00", "end": "00:00"}, 
             "Tuesday": {"start": "00:00", "end": "00:00"}, 
             "Wednesday": {"start": "00:00", "end": "00:00"}, 
             "Thursday": {"start": "00:00", "end": "00:00"}, 
             "Friday": {"start": "00:00", "end": "00:00"} }
    for i in range(len(quarter)):
        currTimes = quarter[i].find_elements_by_xpath(".//tr[1]/td[4]/div/div")
        for j in range(len(currTimes)):
            days = currTimes[j].find_element_by_xpath(".//div[1]/span").get_attribute("aria-label")
            print(days)
            print("-----------------------" + "\n")

class Class:
    times = { "Monday": {"start": "00:00", "end": "00:00"}, 
             "Tuesday": {"start": "00:00", "end": "00:00"}, 
             "Wednesday": {"start": "00:00", "end": "00:00"}, 
             "Thursday": {"start": "00:00", "end": "00:00"}, 
             "Friday": {"start": "00:00", "end": "00:00"} }
    timeStart = None
    timeEnd = None
    SLN = None
    def __init__(self, timeStart: str, timeEnd: str, SLN: int):
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.SLN = SLN


class ClassList:
    classlist = []
    name = None


    def __init__(self, name, classes):
        self.name = name
        classlist = []
        for i in range(len(classes)):
            times = classes[i].find_elements_by_xpath(".//tr[1]/td[4]/div/div/div[2]/time")
            timeStart = format_string(times[0].text)
            timeEnd = format_string(times[1].text)
            get_times(classes)
            SLN = classes[i].find_element_by_xpath(".//tr[1]/td[6]").text[-5:]
            self.classlist.append(Class(timeStart, timeEnd, SLN))

    def to_string(self) -> str:
        class_info = ""
        for x in self.classlist:
            class_info += self.name + " goes from " + x.timeStart + " to " + x.timeEnd + ", SLN: " + x.SLN + "\n"
        return class_info


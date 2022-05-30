class Class:
    times = { "Monday": {"start": "00:00", "end": "00:00"}, 
             "Tuesday": {"start": "00:00", "end": "00:00"}, 
             "Wednesday": {"start": "00:00", "end": "00:00"}, 
             "Thursday": {"start": "00:00", "end": "00:00"}, 
             "Friday": {"start": "00:00", "end": "00:00"} }
    timeStart = None
    timeEnd = None
    SLN = None
    def __init__(self, times: dict, SLN: int):
        self.times = times
        self.SLN = SLN

def get_times(section) -> dict:
    times = { "Monday": {"start": "00:00", "end": "00:00"}, 
             "Tuesday": {"start": "00:00", "end": "00:00"}, 
             "Wednesday": {"start": "00:00", "end": "00:00"}, 
             "Thursday": {"start": "00:00", "end": "00:00"}, 
             "Friday": {"start": "00:00", "end": "00:00"} }
    week = section.find_elements_by_xpath(".//tr[1]/td[4]/div/div")
    for x in week:
        days = x.find_element_by_xpath(".//div[1]/span").get_attribute("aria-label").split(", ")
        timez = x.find_elements_by_xpath(".//div[2]/time")
        for day in days:
            times[day] = {"start": timez[0].get_attribute("datetime"), "end": timez[1].get_attribute("datetime")}
    return times

def ret_times(times: dict) -> str:
    ret = ""
    if times["Monday"]["start"] != "00:00":
        ret += "Monday: " + times["Monday"]["start"] + "-" + times["Monday"]["end"] + "\n"
    if times["Tuesday"]["start"] != "00:00":
        ret += "Tuesday: " + times["Tuesday"]["start"] + "-" + times["Tuesday"]["end"] + "\n"
    if times["Wednesday"]["start"] != "00:00":
        ret += "Wednesday: " + times["Wednesday"]["start"] + "-" + times["Wednesday"]["end"] + "\n"
    if times["Thursday"]["start"] != "00:00":
        ret += "Thursday: " + times["Thursday"]["start"] + "-" + times["Thursday"]["end"] + "\n"
    if times["Friday"]["start"] != "00:00":
        ret += "Friday: " + times["Friday"]["start"] + "-" + times["Friday"]["end"] + "\n"
    return ret

class ClassList:
    classlist = []
    name = None

    def __init__(self, name, quarter):
        self.name = name
        classlist = []
        for section in quarter:
            times = get_times(section)
            SLN = section.find_element_by_xpath(".//tr[1]/td[6]").text[-5:]
            self.classlist.append(Class(times, SLN))

    def to_string(self) -> str:
        class_info = ""
        for x in self.classlist:
            class_info += self.name + ":\n" + ret_times(x.times) + "SLN: " + x.SLN + "\n\n"
        return class_info


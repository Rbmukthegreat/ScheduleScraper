class Class(object):
    def __init__(self, times: dict, SLN: int, section_id: str):
        self.times = times
        self.SLN = SLN
        self.section_id = section_id



class ClassList(object):
    def __init__(self, name, quarter, type):
        self.name = name
        self.type = type
        self.classlist = []
        classlist = []
        for section in quarter:
            if self.found_key(section):
                continue
            if self.class_full(section):
                continue
            if not self.right_type(section):
                continue

            times = self.get_times(section)
            SLN = section.find_element_by_xpath(".//tr[1]/td[6]").text[-5:]
            section_id = ""
            try:
                section_id = section.find_element_by_xpath(".//tr[1]/td[2]/div/span[2]").text
            except:
                section_id = section.find_element_by_xpath(".//tr[1]/td[2]/div/div/span[2]").text
            self.classlist.append(Class(times, SLN, section_id))

    def found_key(self, section) -> bool:
        key = ""
        try: 
            key = section.find_element_by_xpath(".//tr[1]/td[2]/div/div/span[3]").text[0:8]
        except:
            return False
        return ("Add code" == key)
    
    def class_full(self, section) -> bool:
       return [ int(s) for s in section.find_element_by_xpath(".//tr[1]/td[7]/small").text.split() if s.isdigit() ][0] <= 0

    def right_type(self, section) -> bool:
       if self.type == "":
           return True 
       thistype = section.find_element_by_xpath(".//tr[1]/td[3]/span").text.split(" ")[0].upper() 
       return (thistype==self.type)

    def to_string(self) -> str:
        class_info = ""
        for x in self.classlist:
            class_info += self.name + " " + self.type + " " + x.section_id + ":\n" + self.ret_times(x.times) + "SLN: " + x.SLN + "\n\n"
        return class_info

    def get_times(self, section) -> dict:
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
    
    def ret_times(self, times: dict) -> str:
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

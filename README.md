# Classes and Get_Classes 
## Introduction
This is (hopefully obviously) where you get the class information for the separate classes that you want to take.
For example, let's say you want to take a math class, an english class, etc. you would specify that in this file.

## University of Washington Example
As I will be going to the University of Washington this summer, I made this project for that university.
Obviously, if you go to a different university, the [classes.py](classes.py) and [get_classes.py](get_classes.py) wouldn't work for that.
So I will now explain what you need to do in your file (if you fork this repo), and how mine works.
### What classes.json looks like
classes.json is a large list of all the classes. 
It is structured in this way so that I can loop through it, and it is necessary to make sure that [test.py](test.py) works.
An exmaple class would look something like this:
```json
[
    {
        "CLASS": "EXAMPLE",
        "TYPE": "",
        "ITEMS": [
            {
                "SECTION_ID": "A",
                "SLN": "999999",
                "TIMES": [
                    "12:30-14:20",
                    "00:00-00:00",
                    "12:30-14:20",
                    "00:00-00:00",
                    "12:30-13:20"
                ]
            }
        ]
    }
]
```
Now this might look very complicated, but I will try to break it down. 
So the first thing that is the class name. That is what "CLASS" is. 
The second thing is type--this might not look super intuitive, and that's because it's not.
This program will treat a physics lecture/quiz/laboratory as three separate classes. 
This is because UW treats these quiz sections/labs as different classes--they are not tied to the lecture.
So my solution is to just copy that. 
SECTION_ID is self explanatory, SLN is the number that you need to add the class to your schedule.
Finally, times is a list of length 5 to represent the 5 days of the week.
One thing to note, however, is that 00:00 represents having no class on that day.

### How I do it
If you go look into [classes.py](classes.py), you can see that there are two separate to_dict() functions:
one for the ClassList, and the other for just the class. 
I do it this way so I can simply loop through self.classlist, which is the motivation for having "ITEMS" be be a list (in the json).
It looks like this:
```python
    def to_dict_entry(self):
        entry = {"CLASS": self.name, "TYPE": self.type, "ITEMS": [ x.to_dict_entry() for x in self.classlist ] }
        return entry
```
For the class object, the thing that is being looped through, it's to_dict looks like this:
```python
def to_dict_entry(self) -> dict:
    return { "SECTION_ID": self.section_id, "SLN": self.SLN, "TIMES": self.times }
```

## How I Get "Correct" Classes
You will notice three functions that look like this:
```python
if function:
    continue
```
These make sure that I don't get any classes that won't work. 
How I determine if classes are "wrong" is like this:
If there is a key next to the class, that means the class is locked--and that I can't sign up for it, so don't include that.
If the class is full, don't include that.
Finally, if the class is the wrong type--e.g. it should be a quiz section but it returned a lecture, ignore that.
The last thing to notice is that my way of getting around having to type "LECTURE" for everything is simply saying if there is no specified type, just ignore the right_type function.
 
# test.py and draw_schedule.py
These are the two files that you don't have to design yourself. 
These files only speak to classes.json--which is why all you have to do is design your own files for your own school to generate this file, and test.py will take care of everything else from there.

There are five fields at the top of test.py that you will notice: `count`, `TIME_BETWEEN_CLASSES`, `CONSTRAINTS`, `LUNCH`, `LEN_LUNCH`.
`count` is really just there for me (or you!) to see how many schedule possibilities there are. You could disable this behavior if you like.

`TIME_BETWEEN_CLASSES` is the minimum time that you want between classes. For example, a value of 20/60 = 1/3 would guarentee that you have at least 20 minutes between all your classes.

`CONSTRAINTS` is a list of intervals where you don't want any classes. For example, suppose that you don't want any classes from 8:30 to 9:30. Then you would add "08:30-09:30" to this list.

`LUNCH` is an interval of the earliest time when you want lunch to start, and the latest time you want lunch to end. This interval should be BIGGER than how long you actually want lunch to be, if you want reasonable results.

`LEN_LUCH` is how long you want lunch to be, in hours. For example, 40/60 would be 40 minutes.

[draw_schedule.py](draw_schedule.py) simply draws a picture of the schedule, and displays it to the screen. 
The last thing to note is that after test.py is finished finding schedules that work, all it does is pick a random schedule, and displays it to the screen. I have not yet found a better way of doing this, so this is how it is for now. 
If you want, you can remove/comment out all the print() statements in test.py because all of them are just for me to see if things are working. 
The last thing that I will note is that it prints the SLNs (add codes) to a file, called `classes_out.txt`. 
I do this so when I actually need to add these to my schedule, it will be in a nice list. 

# Running the Program
You have to run two files, in this order.
After you are done setting up all the fields, you are going to want to run
[get_classes.py](get_classes.py). Once that finishes up, you should run [test.py](test.py) to both find a schedule that works, and to visualzie it.

TODO: write about fields in get_classes.py

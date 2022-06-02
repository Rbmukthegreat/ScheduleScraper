import os, sys
from PIL import Image, ImageDraw, ImageFont

def get_height(start, end, typ):
    height = int((int(72*(start - 8))+174+int(72*(end - 8)))/2) - 15
    if typ != "":
        height -= 10
    return height

def draw_class(classname, typ, times, img1, fnt, n):
    colors = {0: "red", 1: "orange", 2: "yellow", 3: "green", 4: "blue", 5: "purple", 6: "magenta", 7: "cyan"}
    for i in range(len(times)):
        if (times[i]=="00:00-00:00"):
            continue
        start, end = times[i][0], times[i][1]
        shape = ((150 + 344*i, int(72*(start - 8))+87), (150+344*(i+1), int(72*(end - 8)) + 87)) 
        img1.rectangle(shape, fill=colors[n], outline="black")
        img1.multiline_text((344*i+300, get_height(start, end, typ)), classname+"\n"+typ, font=fnt, fill=(0, 0, 0, 128))

def draw_schedule(classes):
    w, h, = 1920, 1080
    img = Image.new("RGB", (w, h), (255, 255, 255, 128))
    
    fnt = ImageFont.truetype("Meslo LG S Regular 400.ttf", 20)
    img1 = ImageDraw.Draw(img)
    days = {0: "M", 1: "T", 2: "W", 3: "Th", 4: "F"}
    time = {0: "8:00", 1: "9:00", 2: "10:00", 3: "11:00", 4: "12:00", 5: "1:00", 6: "2:00", 7: "3:00", 8: "4:00", 9: "5:00", 10: "6:00", 11: "7:00", 12: "8:00", 13: "9:00"}
    for i in range(14):
        img1.text((30, 72*i+75), time[i], font=fnt, fill=(0, 0, 0, 128))  
        img1.line(((100, 72*i + 87), (1920, 72*i + 87)), fill="black", width=2)
    for i in range(5):
        img1.text((344*i+300, 30), days[i], font=fnt, fill=(0, 0, 0, 128))
 
    for i in range(len(classes)):
        draw_class(classes[i][0], classes[i][2], classes[i][1]["TIMES"], img1, fnt, i) 

    img.show()

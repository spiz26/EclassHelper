import time
import requests
import sys
import tkinter.messagebox
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from tkinter import *
from UserFunctions import *

#Variables
yourID = ""
yourPW = ""
option = -1
subject_order = -1

def Log_in():
    global yourID
    global yourPW
    global window1
    yourID = ID_ent.get()
    yourPW = PW_ent.get()
    window1.destroy()

def Verify():
    global option
    global window2
    global subject_order
    option = opt.get()
    try:
        subject_order = int(sub_ent.get())
    except:
        pass
    window2.destroy()

#window1
window1 = Tk()
window1.title("Hello! Lazy!")
window1.geometry("400x300")
window1.option_add("*Font","굴림 20")

img = PhotoImage(file="Seoultech_logo.PNG", master = window1)
img = img.subsample(4)

logo = Label(window1)
logo.config(image=img)

ID_label = Label(window1)
ID_label.config(text="ID")

PW_label = Label(window1)
PW_label.config(text="Password")

btn1 = Button(window1)
btn1.config(text="Log In", command=Log_in)

ID_ent = Entry(window1)
PW_ent = Entry(window1)
PW_ent.config(show="*")

logo.pack()
ID_label.pack()
ID_ent.pack()
PW_label.pack()
PW_ent.pack()
btn1.pack()
window1.mainloop()

#window2
window2 = Tk()
window2.title("Select Options")
window2.geometry("300x150")

opt = IntVar()
r1 = Radiobutton(window2, text='전체', variable=opt, value=0)
r2 = Radiobutton(window2, text='1과목', variable=opt, value=1)

sub_label = Label(window2)
sub_label.config(text="Subject order")

def clear(event):
    global sub_ent
    sub_ent.delete(0, len("전체 옵션은 불필요"))

sub_ent = Entry(window2)
sub_ent.insert(0,"전체 옵션은 불필요")

sub_ent.bind("<Button-1>", clear)
btn2 = Button(window2)
btn2.config(text="Verify", command=Verify)

r1.pack()
r2.pack()
sub_label.pack()
sub_ent.pack()
btn2.pack()
window2.mainloop()

#main
eclass_link = "https://eclass.seoultech.ac.kr/ilos/main/member/login_form.acl"

res = requests.get(eclass_link)
if res.status_code == requests.codes.ok:
    print("e-class ping 정상")

browser = webdriver.Chrome("./chromedriver.exe")
browser.get(eclass_link)
browser.maximize_window()

try:
    #log in
    browser.find_element_by_id("usr_id").send_keys(yourID)
    browser.find_element_by_id("usr_pwd").send_keys(yourPW)
    browser.find_element_by_class_name("btntype").click()

    #subjects
    subjects = browser.find_elements_by_class_name("sub_open")
    num_subjects = len(subjects)

except:
    time.sleep(0.2)
    tkinter.messagebox.showinfo("Login Error", "Invalid ID or PW!")
    sys.exit(0)
try:
    for i in range(num_subjects):
        browser.find_element_by_id("logo_link").click()
        subjects = browser.find_elements_by_class_name("sub_open")
        select_subject = subjects[i]
        print(f"subject : {select_subject.text}")
        select_subject.click()
    
        #lecture room
        browser.find_element_by_id("menu_lecture_weeks").click()
        lectures_weeks = browser.find_elements_by_class_name("wb-week")

        week_list = []

        for week in lectures_weeks:
            week_list.append(week.text.replace("주", ""))

        def week_initialize(browser):
            lectures_per_week = browser.find_elements_by_class_name("site-mouseover-color")
            return lectures_per_week

        for week in week_list:
            #enter the week
            print(f"Cheking {week}week lectures")
            browser.find_element_by_id(f"week-{week}").click()
            time.sleep(0.3)

            #Checking lectures_per_week, complete
            lectures_per_week = week_initialize(browser)
            num_lectures = len(lectures_per_week)
            completes = browser.find_elements_by_id("per_text")
            rest_time = browser.find_elements_by_xpath("//*[@style=\"float: left;margin-left: 7px;margin-top:3px;\"]")
            rest_time_list = []
            complete_list = []

            for com in completes:
                complete_list.append(com.text)

            for lec_time_iter in rest_time:
                rest_time_list.append(lec_time_iter.text)

            num_sub = 1
            for i in range(num_lectures):
                lectures_per_week = week_initialize(browser)
                if num_sub == 1:
                    pass
                else:
                    num_sub -= 1
                    continue

                if int(complete_list[i].split("%")[0]) < 100:
                    lec_time = RestTime(rest_time_list[i])
                    try:
                        lectures_per_week[i].click()
                        time.sleep(0.3)
                        #물 건너간 강의의 alert
                        #alert_accept(browser)
                        close_button = browser.find_element_by_id("close_")
                        time.sleep(0.3)
                        print(f"{lec_time // 60}min, {lec_time % 60}seconds left.")
                        time.sleep(lec_time)#lec_time

                        sub_mini_lec = browser.find_elements_by_class_name("item-title-lesson")
                        num_sub = len(sub_mini_lec)
                        print(f"num_sub : {num_sub}")

                        if num_sub > 1:
                            for sub in range(1, num_sub):
                                sub_mini_lec = browser.find_elements_by_class_name("item-title-lesson")
                                sub_mini_lec[sub].click()
                                time.sleep(0.3)
                                #강의 시간 전 빠져나올 때의 alert
                                #alert_accept(browser)
                                lec_time = RestTime(rest_time_list[i+1])
                                time.sleep(lec_time) #lec_time
                                print(f"{lec_time // 60}min, {lec_time % 60}seconds left.")
                        
                            close_button = browser.find_element_by_id("close_")

                        else:
                            pass

                        close_button.click()
                        time.sleep(0.3)
                        #강의 시간 전 빠져나올 때의 alert
                        #alert_accept(browser)
                    except:
                        print(f"{week}week-{i+1}은 이미 늦었습니다 ㅠㅠ. 강의는 제때 들으셔야죠.")
                else:
                    print(f"{week}week-{i+1} have done.")
            print("\n")
            time.sleep(0.3)

except:
    time.sleep(0.2)
    tkinter.messagebox.showinfo("Program Error", "Yon can't use this program. Wait next version plz.")
    sys.exit(0)

print("모든 학습이 끝났습니다!")
browser.quit()
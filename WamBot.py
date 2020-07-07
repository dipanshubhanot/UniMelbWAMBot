from selenium import webdriver
from time import sleep
import sqlite3 as sql
from twilio.rest import Client
import os


class WamBot:
    def __init__(self, usrname, name, password, phonenum):
        self.driver = webdriver.Chrome()
        self.usrname = usrname
        self.name = name
        self.password = password
        self.conn = sql.connect('wambase.db')
        self.cursor = self.conn.cursor()
        self.phonenum = 'whatsapp:'+phonenum
        self.from_whatsapp_number = 'whatsapp:+14155238886'
        try:
            self.conn.execute("CREATE TABLE " + self.name +
                              " (datetime TEXT NOT NULL, WAM REAL NOT NULL) ")
        except sql.OperationalError:
            # filller
            self.cursor = self.conn.cursor()

    def login(self):
        self.driver.get('https://my.unimelb.edu.au')

        sleep(3)

        usrNameField = self.driver.find_element_by_xpath('//*[@id="usernameInput"]')
        passField = self.driver.find_element_by_xpath('//*[@id="passwordInput"]')
        loginBtn = self.driver.find_element_by_xpath('//*[@id="top"]/div[2]/div/section/form/div[2]/button')

        # Select and enter username and password
        usrNameField.click()
        usrNameField.send_keys(self.usrname)
        passField.click()
        passField.send_keys(self.password)

        # press login button
        loginBtn.click()

    def open_results(self):
        navbar = self.driver.find_element_by_xpath('//*[@id="toggleMenu"]/span')
        navbar.click()
        sleep(10)
        navbardropdown = self.driver.find_element_by_xpath('//*[@id="navbarTogglerDemo02"]')
        studentAdmn = self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/a')
        # studentAdmn.submit()
        studentAdmn.click()
        examsPage = self.driver.find_element_by_xpath('//*[@id="examsresultsLink"]')
        examsPage.click()

    def open_recent_results(self):
        recentresults = self.driver.find_element_by_xpath('/html/body/main/div[2]/div[1]/div/div/ul[2]/li[1]/a')
        recentresults.click()

    def switch_wam_window(self):
        # Switching Windows while keeping the old one in memory
        base_window = self.driver.window_handles[0]
        new_window = self.driver.window_handles[1]
        client = Client()
        client.messages.create(body="You have successfully established a connectionwith WAMBot \n "+
                                    "You may relax!, until we tell you your WAM has changed! ",
                               from_=self.from_whatsapp_number,
                               to=self.phonenum)
        self.driver.switch_to.window(new_window)

    def check_wam(self):
        wam = self.driver.find_element_by_xpath('//*[@id="ctl00_Content_lblResultSummary"]/div[1]/b')
        currwam = float(wam.text)
        return currwam

    def store_wam(self, wam):
        self.conn.execute(
            "INSERT INTO " + self.name + " (datetime, WAM)  VALUES (CURRENT_TIMESTAMP, " + str(wam) + ")"
        )
        self.conn.commit()

    def send_notification(self, prevWAM, newWAM):
        client = Client()
        client.messages.create(body='Your WAM has changed from '+str(prevWAM)+' to '+str(newWAM)+'.',
                               from_ = self.from_whatsapp_number,
                               to=self.phonenum)

    def send_no_change_notif(self):
        client=Client()
        client.messages.create(body="Your WAM hasn't changed since the last message",
                               from_=self.from_whatsapp_number,
                               to=self.phonenum)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("Sailee's Bot")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.hindi.greetings",
    "chatterbot.corpus.hindi.coversations",
              "chatterbot.corpus.marathi.greetings"

              )


#opening_web_app
driver = webdriver.Chrome('C:/Users/User/Downloads/chromedriver.exe')
driver.get('https://web.whatsapp.com/')
time.sleep(10)
people_list = ["Moomy"]
'''
search_bar = driver.find_element_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]')
search_bar.send_keys("Moomy")
time.sleep(8)
if_unread = driver.find_element_by_css_selector('span[title="Moomy"]')
parent = if_unread.find_element_by_xpath("..")

parent = parent.find_element_by_xpath("..")
parent = parent.find_element_by_xpath("..")
parent = parent.find_element_by_xpath("..")
print(parent.get_attribute("class"))
parent = parent.find_element_by_xpath("/div[@class='_1582E']/div[@class='m61XR']/span").text
print(parent)
#message_receieved = driver.find_element_by_css_selector('.message-in:last-child ._3sKvP ._274yw .copyable-text .eRacY ._3Whw5 span').text
#print(message_receieved)
#total = driver.find_elements_by_css_selector('.message-in')
#print(len(total))

'''
def check_new_messages(whatsapp_connection_success,people_list):
    while(not whatsapp_connection_success):
        try:
            search_bar = driver.find_element_by_xpath('//div[@class="_1awRl copyable-text selectable-text"]')
        except:
            whatsapp_connection_success = False
        else:
            whatsapp_connection_success = True
    for name in people_list:
        time.sleep(5)
        search_bar.send_keys(name+Keys.ENTER)

        check_new_msg = driver.find_elements_by_xpath('//div[@class="XFAMv focusable-list-item"]')
        if (len(check_new_msg)!=0):
             return name

    return check_new_messages(not whatsapp_connection_success,people_list)

def greeting(name,message_box,message_and_replies):
    driver.implicitly_wait(2)
    recieved_no = driver.find_elements_by_css_selector('.message-in')
    old_messages_recieved =len(recieved_no)

    driver.implicitly_wait(1)
    message_box.send_keys('Hello'+Keys.ENTER)
    driver.implicitly_wait(1)
    message_box.send_keys("I am an automated message sent by Sailee's bot. Type 'quit' to end chat."+Keys.ENTER)
    driver.implicitly_wait(2)


    start_time = 0

    def waiting_for_message(start_time,old_messages_recieved,message_box,message_and_replies):
        start_time = 0
        while(old_messages_recieved == len(driver.find_elements_by_xpath('//div[@class="_1RAno message-in focusable-list-item"]')) and start_time!=25):
            start_time +=1
            time.sleep(1)
            #print("waiting")

        if(start_time==15):
            name = check_new_messages(False,people_list)
            message_box = driver.find_element_by_xpath('//div[@class="DuUXI"]')
            return greeting(name,message_box,message_and_replies)
        else:
            try:
                recieved_no = driver.find_elements_by_css_selector('.message-in')

                #recieved_no = driver.find_elements_by_xpath('//div[@class="_2hqOq message-in focusable-list-item"]')
                #recieved_no_28_class = driver.find_elements_by_xpath('//div[@class="_2hqOq _28DtS message-in focusable-list-item"]')
                old_messages_recieved = len(recieved_no)

                message_receieved = driver.find_element_by_css_selector('.message-in:last-child ._1ij5F ._2XJpe ._1dB-m .copyable-text ._1wlJG ._1VzZY span').text
                msg = chatbot.get_response(message_receieved)
            except:
                return waiting_for_message(start_time, old_messages_recieved, message_box, message_and_replies)
            fined_tune_replies = list(filter(lambda x: message_receieved.lower() in x, message_and_replies.keys()))
            print(fined_tune_replies)

            if ("quit" in message_receieved or "QUIT" in message_receieved or "Quit" in message_receieved):
                message_box.send_keys("Bye Bye" + Keys.ENTER)
                driver.implicitly_wait(8)
                start()

            elif ("time" in message_receieved):
                message_box.send_keys(str(datetime.now()) + Keys.ENTER)

            #elif (message_receieved.upper()  in message_and_replies.keys() or message_receieved.lower() in message_and_replies.keys() or message_receieved.capitalize() in message_and_replies.keys()):
             #   message_box.send_keys(message_and_replies[message_receieved.lower()] + Keys.ENTER)
            #elif(len(fined_tune_replies)!=0 and fined_tune_replies[0] in  message_and_replies.keys()):
             #   message_box.send_keys("I think you meant : "+fined_tune_replies[0]+ Keys.ENTER)
              #  message_box.send_keys(message_and_replies[fined_tune_replies[0]] + Keys.ENTER)
            else:
                message_box.send_keys(str(msg) + Keys.ENTER)
            driver.implicitly_wait(1)

            return waiting_for_message(start_time, old_messages_recieved, message_box, message_and_replies)

    wait_4response = waiting_for_message(start_time,old_messages_recieved, message_box,message_and_replies)

def start():
    whatsapp_connection_success = False
    name = check_new_messages(whatsapp_connection_success,people_list)
    message_box = driver.find_element_by_xpath('//div[@class="DuUXI"]')
    message_and_replies = {"hi":"hello","hey":"hi! have a nice day","hello":"hi! how are you?","good morning":"have a nice day",
                       "how do you do":"i am fine. wbu?","how are you":"i am fine. wbu?","thank you":"You are welcome","ty":"you are welcome",
                       "tysm":"You are welcome","thanks":"You are welcome","fine":"That's great","good":"That's great","wsup":"Nothing much!"}

    greet = greeting(name,message_box,message_and_replies)
st = start()
## got this from https://testingonprod.com/2021/10/24/how-to-send-text-messages-with-python-for-free/


import smtplib
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}
EMAIL = "kellanscoding@gmail.com"
PASSWORD = "xbxmpwpyjeibchpf"

def send_message(phone_number,message, carrier="verizon",):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, message)
 
 

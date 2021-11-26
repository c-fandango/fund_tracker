
import os
import matplotlib.pyplot as plt
import json
from datetime import date
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
funds={"":{"sdate":"","edate":None, "graph": True},"":{"sdate":"","edate":None,"graph": True},"":{"sdate":"","edate":None,"graph": True},
       "":{"sdate":"","edate":None,"graph": True},"":{"edate":None,"sdate":"","graph": True},
       "":{"sdate":"","edate":None,"graph": True},"":{"sdate":"","edate":None,"graph": True},"":{"sdate":"","edate":None,"graph": True},
       "":{"sdate":"","edate":"","graph": False},
       "":{"sdate":"","edate":None,"graph": False}}
other={"dates":{"sdate":"","edate":None,"graph": False},"total":{"values":[],"sdate":"","edate":None, "graph": True}}


for fund in funds:
    with open(f"/home/pi/pythonbotProject1/{fund}data.txt", 'r') as file:
        funds[fund]["values"] = json.load(file)
with open(f"/home/pi/pythonbotProject1/datesdata.txt", 'r') as file:
        other["dates"]["values"] = json.load(file)
print(len(funds['']['values']),len(other['dates']['values']),other['dates']['values'][-1])

for fund in funds:
    a=other["dates"]["values"].index(funds[fund]["sdate"])
    funds[fund]["zero"]=[0]*a + funds[fund]["values"]

    if funds[fund]["edate"] is not None:
        c=len(other["dates"]["values"]) - other["dates"]["values"].index(funds[fund]["edate"])
        funds[fund]["zero"]= funds[fund]["zero"]+[0]*(c+10)

totalzero=[]
for i in range(len(other["dates"]["values"])):
    b=0
    for fund in funds:
        if funds[fund]["sdate"] is not None:   
                        b=funds[fund]["zero"][i]+b
    totalzero.append(b)
    

for i in range(len(other["dates"]["values"])):
    other["total"]["values"].append(round(totalzero[i],2))

funds.update(other)

def past(fnd,x):
    return(funds[fnd]["values"][-x:])


def pc(fnd,x):
    lst=past(fnd,x)
    return(round((lst[-1]-lst[0])*100*lst[0]**(-1),1))


def graph(fnd,x):
    plt.figure()
    plt.plot(past("dates",x), past(fnd,x))
    plt.xticks(rotation=30)
    plt.title(f"{fnd} Value Over The Last {x} Days")
    ax = plt.gca()
    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % (x//5) != 0:
            label.set_visible(False)
    plt.savefig(f"/home/pi/pythonbotProject1/{fnd}{x}-{date.today()}.png", bbox_inches= 'tight')
    plt.close()
    return ()

      

for fund in funds:
    if funds[fund]["sdate"] is not None:
        if len(funds[fund]["values"])>143:
            print(graph(fund,10))
            print(graph(fund,143))
        else:
            print(graph(fund,len(funds[fund]["values"])))


port = 465  
subject = f"Analysis {datetime.date.today()}"
body = f""

sender_email = ""
receiver_email = ""
password = ''

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

message.attach(MIMEText(body, "plain"))

def attach(y,x):
        filename=f"/home/pi/pythonbotProject1/{y}{x}-{date.today()}.png"
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",'attachment',filename= f"{y}.jpg")
        message.attach(part)
        return()

for fund in funds:
    if funds[fund]["graph"]:
        if len(funds[fund]["values"])>143:
            print(attach(fund,10))
            print(attach(fund,143))
        else:
            print(attach(fund,len(funds[fund]["values"])))
    
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

print("email sent")
for file in os.listdir('/home/pi/pythonbotProject1/'):
    if file.endswith('.png'):
        os.remove('/home/pi/pythonbotProject1/' + file)

print("cleanup complete")


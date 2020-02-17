import time
from threading import Timer
import subprocess
import webbrowser
import smtplib
from tkinter import *
import shelve
from datetime import datetime as dt

class Open_Web:
  def __init__(self, time,page):
    self.time=time
    self.page=page
    save_obj(self)
  def run_on_time(self):
    Timer(self.time.timestamp()-time.time(), webbrowser.open, args=(self.page,)).start()
    
class Open_File:    
  def __init__(self, time,file,programm='start'):
    self.time=time
    self.file=file
    self.programm=programm
    save_obj(self)
  def run_on_time(self):
    Timer(self.time.timestamp()-time.time(), subprocess.run, args=((self.programm, self.file, self.file),),
    kwargs={'shell':True}).start()

class Send_Email:
  mail_clients={'gmail' : 'smtp.gmail.com', 'outlook.com': 'smtp-mail.outlook.com',
  'hotmail.com':'smtp-mail.outlook.com' ,'yahoo': 'smtp.mail.yahoo.com'}
  def __init__(self, time, mail_client, mail_login, mail_to_send , password, message):
    self.time=time
    self.mail_client=type(self). mail_clients[mail_client]
    self.mail_login=mail_login
    self.mail_to_send=mail_to_send
    self.password=password
    self.message="Subject: Don't forget\n"+message
    save_obj(self)
  def send_function(self):
    obj=smtplib.SMTP(self.mail_client, 587)
    obj.ehlo()
    obj.starttls()
    obj.login(self.mail_login, self.password)
    obj.sendmail(self.mail_login, self.mail_to_send,self.message)
    obj.quit()
  def run_on_time(self):
    Timer(self.time.timestamp()-time.time(), self.send_function).start()
    
class Open_Message:
  def __init__(self, time, message):
    self.time=time
    self.message=message
    save_obj(self)
  def grafic(self):
    root=Toplevel()
    root.title('Ξεχασιάρης')
    root.geometry('800x600')
    labelfont = ('times', 20, 'bold')
    mainframe=Frame(root, borderwidth=5)
    mainframe.pack(expand=YES, fill=BOTH)
    message1=Message(mainframe,text=self.message, font=labelfont)
    message1.config(bg='black', fg='yellow', relief=RAISED)
    message1.pack(expand=YES, fill=BOTH) 
    button=Button(root,text='Το διάβασα', command=root.destroy)
    button.pack(fill=X) 
    button.focus_set()
  def run_on_time(self):
    Timer(self.time.timestamp()-time.time(), self.grafic).start()  

def save_obj(obj):
  obj_f=shelve.open('jexasiaris')
  lista=obj_f['lista']
  lista.append(obj)
  obj_f['lista']=lista
  obj_f.close()
  
def load_from_saved():
  obj_f=shelve.open('jexasiaris')
  try: 
    lista=obj_f['lista']
  except:
    obj_f['lista']=[]
  lista=obj_f['lista']
  for obj in lista:
    obj.run_on_time()
  obj_f.close()  
  
def delete_alt_objects():
  obj_f=shelve.open('jexasiaris')
  lista=obj_f['lista']
  for obj in lista[:]:
    if obj.time<dt.now():
      lista.remove(obj)
  obj_f['lista']=lista
  obj_f.close()

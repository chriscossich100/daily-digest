from tkinter import *
import sys
#import the tk themed widgets:
from tkinter import ttk

#import the DailyDigestEmail class
from dd_email import DailyDigestEmail

#import json from the python library as we are going to be reading and writing to a json file containing recipients
import json 

#callback functions assigned to different widgets:
def add_recipients():
    print(f"the recipient that was entered is: {recipient.get()}")

    #check to see if the recipient.get() is not a empty string:
    new_recipient = recipient.get()
    if new_recipient != '':
        updated_recipient_list = recipient_list.get()
        #check to see if the recipient list is going to be empty:
        if updated_recipient_list != '':
            recipient_list.set(updated_recipient_list + (new_recipient,))
        #if empty, then set the new recipient as the beginning of the list:
        else:
            recipient_list.set([new_recipient])

    #add the new recipient to the dictionary:
    recipient_data['recipients'].append(recipient.get())


#callback function to remove specified recipient(s) from the list:
#recipient_list is actually a list. Meaning we will need to call the list method to go through
#the list and delete specified recipient
def remove_recipients():
    
    recipient_list_box.curselection() #since we are using a listbox widget, we can get the selection using curselection method

    updated_recipient_list = list(recipient_list.get())

    print(f'the listbox recipients before the list method is: {recipient_list_box.curselection()}')
    print(f'the recipient list ina a python list when selecting the remove recipient button is: {list(recipient_list_box.curselection())}')
    
    #go through the list and pop out from the recipient list.
    for index in list(reversed(recipient_list_box.curselection())):
        updated_recipient_list.pop(index)
        #remove the specified index from the recipient json list.
        recipient_data['recipients'].pop(index)
        print(recipient_data['recipients'])

    #set the main recipient_list variable:
    recipient_list.set(updated_recipient_list)
    

#callback for offically updating configurations:
def update_settings():

    #write to the json file that includes the new changes to the main recipient list.
    new_recipients_list = json.dumps(recipient_data, indent=1)
    with open ("recipients.json", "w") as outfile:
        outfile.write(new_recipients_list)


def send_email():

    send_email = DailyDigestEmail()
    #conver the recipient list into a python list and set it to the recipients value in the DialyDigestEmail class:
    send_email.recipients = list(recipient_list.get())
    send_email.sender_credentials = {"email": emailgo.get(), "password" : letsgo.get()}

    send_email.send_email()


try:
    #open the json file containing the list of recipients:
    recipient_list_json = open('recipients.json')

    # returns JSON object as a dictionary to use in the gui
    recipient_data = json.load(recipient_list_json)
    print(f'the recipeint_list_json is {recipient_data}')
    print(recipient_data['recipients'])
    
except Exception as e:
    print("Error Reading File. Terminating Program!")
    sys.exit(1)

#assign the main widget:
root = Tk()

#assign title to the tkinter gui application
root.title('Daily Digest Sender')

#create some styles for the header:
style = ttk.Style()

#condfigure a style for the labels: 
style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))

main_frame = ttk.Frame(root)
main_frame.pack(padx=15, pady=15)

ttk.Label(main_frame, text='Shared Daily Digest', font='Algerian 32 bold', justify=CENTER).grid(row=0,column=0)
ttk.Label(main_frame, font = ('Arial', 15, 'bold'),text='Welcome the Daily Digest Application. Here, you can send daily emails containing configured information to the recipients specified.', wraplength=400).grid(row=1, column=0)

#CREATE THE FRAME FOR RECIPEINT INFORMATION:
recipients_frame = ttk.Frame(root)
recipients_frame.pack(padx=15, pady=15)
#create a label widget for recipeients text:
ttk.Label(recipients_frame, text='Recipients:', style='Header.TLabel').grid(row=0, column=0)

#create an entry field widget to allow users to enter a recipient:
recipient = StringVar()
ttk.Entry(recipients_frame, width=40, textvariable=recipient).grid(row=1, column=0)

#create a button that adds the recipient to the list of recipients:
ttk.Button(recipients_frame, text='Add Recipients', command=add_recipients).grid(row=2,column=0, padx=5, pady=5)

#create the recipient list variable and set it:
recipient_list = Variable()
recipient_list.set(recipient_data['recipients'])

#create a listbox of the recipients already on the list:
#remember that the list box is not a ttk widget so we will need to use a regular tkinter listbox:
recipient_list_box = Listbox(recipients_frame, listvariable=recipient_list, selectmode  = 'multiple', width = 40, height = 10)
recipient_list_box.grid(row=3, column=0, padx=10, pady=10)

#create a button to remove a recipient from the list:
ttk.Button(recipients_frame, text='Remove Recipient', command=remove_recipients).grid(row=4, column=0, padx=5, pady=5)

#CREATE THE FRAME FOR SENDER INFORMATION:
sender_frame = ttk.Frame(root)
sender_frame.pack(padx=15, pady=15)

emailgo = StringVar()
emailgo.set(recipient_data['sender']['username'])
letsgo = StringVar()
letsgo.set(recipient_data['sender']['password'])

#create the label for 'sender credentials:'
ttk.Label(sender_frame, text='Sender Credentials:', style='Header.TLabel').grid(row=0, column=0, columnspan=2)
#create a label for 'email'
ttk.Label(sender_frame, text='Email:').grid(row=1,column=0, pady=5, sticky=E)
#create a entry field widget for the email that will be typed:
ttk.Entry(sender_frame, textvariable=emailgo, width=40).grid(row=1, column=1, pady=5, sticky=W)
#create a label for 'password'
ttk.Label(sender_frame, text='Password:').grid(row=2, column=0, pady=5, sticky=E)
#create the entry field widget for the passwotd that will be typed:
ttk.Entry(sender_frame, textvariable=letsgo, width=40, show="*").grid(row=2, column=1, pady=5, sticky=W)

#CREATE THE FRAME FOR UPDATING SETTINGS AND SENDING EMAIL: 
control_frame = ttk.Frame(root)
control_frame.pack(pady=15, padx=15)

#create a button widget to update settings:
ttk.Button(control_frame, text='Update Settings', command=update_settings).grid(padx=5, pady=5, row=0, column=0)
#create a button widget to send email:
ttk.Button(control_frame, text='Send Email', command=send_email).grid(padx=5, pady=5, row=0, column=1)


root.mainloop()
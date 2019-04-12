#!/usr/bin/python
import re
import sys
import imaplib
import getpass
import email
import os


''' Python Power Cuckoo 
    By Michael Hoffman (1nd0) 
    Based off of Power Cuckoo by Nicholas Penning (napsta)
    Version 0.1
    Description: The automation pulling Malware and malicious links from emails and having Cukoo Start analysis.
'''

# Calls for Cuckoo REST API
REST = input('Enter Cuckoo Ip Address: ')
MaliciousFileREST = REST + 'tasks/create/file'
MaliciousUrlREST = REST + 'tasks/create/url'
MaliciousArchiveREST = REST +'task/create/submit'

'''
IMAP_SERVER = input('IMAP Server: ')
imap_port = input('Port: ')
imap = imaplib.IMAP4_SSL(IMAP_SERVER,imap_port)
EMAIL_ACCOUNT = input("Email Address: ")
EMAIL_FOLDER = input("Email Folder: ")
OUTPUT_DIRECTORY = 'C:/src/tmp'

Password = getpass.getpass()


'''
detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')

emailaddress = input('Enter your GMail username:')
passwd = getpass.getpass('Enter your password: ')

try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(emailaddress, passwd)
    if typ != 'OK':
        print('Not able to sign in!')
        raise

    imapSession.select('[Gmail]/All Mail')
    typ, data = imapSession.search(None, 'ALL')
    if typ != 'OK':
        print('Error searching Inbox.')
        raise

    # Iterating over all emails
    for msgId in data[0].split():
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
        if typ != 'OK':
            print('Error fetching mail.')
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_string(emailBody)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                continue
            if part.get('Content-Disposition') is None:
                # print part.as_string()
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(detach_dir, 'attachments', fileName)
                if not os.path.isfile(filePath) :
                    print(fileName)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    imapSession.close()
    imapSession.logout()
except :
    print('Not able to download all attachments.')

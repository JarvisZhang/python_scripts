import imaplib
import email
from email import parser

HOST_ADDRESS = 'imap.126.com'
USERNAME = 'gitview'
PASSWORD = 'gitviewtest'

def draft_imap():
    M = imaplib.IMAP4('imap.126.com')
    M.login('gitview', 'gitviewtest')
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
    #     print 'Message %s\n%s\n' % (num, data[0][1])
        msg=email.message_from_string(data[0][1])
        content=msg.get_payload(decode=True)
        print msg
    M.close()
    M.logout()
   

def test_imap():
    imap=imaplib.IMAP4('imap.126.com')
    imap.debug=3
    imap.login('gitview', 'gitviewtest')
    imap.select()
    result, all_data=imap.search(None,'ALL')
    for num in all_data[0].split():
        typ,data=imap.fetch(num, '(RFC822)')
        emsg=email.message_from_string(data[0][1])
        subject,ecode=email.Header.decode_header(emsg["subject"])[0]
        fromuser=email.utils.parseaddr(emsg.get("from"))[1]
        if ecode=='gb18030':
            subject=subject.decode('gb2312').encode('utf8')
        for part in emsg.walk():
            print part.get_content_type()
            if part.get_content_type()=="text/html":
                body=part.get_payload(decode=True)
                mailtype=part.get_content_charset()
                if mailtype=='gb2312' or mailtype=='gb18030':
                    body=body.decode('gb2312').encode('utf-8')
                else:
                    body=body.decode('utf-8')
                f = open('body.txt', 'w')
                f.write(body)
                print body
#                 break
    imap.logout()
    #imap.close()
    print "over"
    

class My_Imap(object):
    imap = object
    emails_body = []
    
    def __init__(self, host_address, username, password):
        try:
            self.imap = imaplib.IMAP4(host_address)
            self.imap.debug = 3
            self.imap.login(username, password)
        except Exception, error:
            print 'login failed'
            print 'error: %s' % error

    def refresh_unseen(self):
        try:
            self.imap.select()
            typ, mail_abstracts = self.imap.search(None, 'ALL')
            fetch_list = mail_abstracts[0].split(' ')
            for id in fetch_list:
                typ, mail_data = self.imap.fetch(id, '(RFC822)')
                email_msg = email.message_from_string(mail_data[0][1])
                subject, encode = email.Header.decode_header(email_msg['subject'])[0]
                if encode == 'gb18030':
                    subject = subject.decode('gb2312').encode('utf8')
                if self.is_from_jira(subject):
                    for part in email_msg.walk():
                        if part.get_content_type() == 'text/html':
                            body = part.get_payload(decode = True)
                            body_encode = part.get_content_charset()
                            if body_encode == 'gb2312' or body_encode == 'gb18030':
                                body = body.decode('gb2312')
                            else:
                                body = body.decode('utf8')
                            self.emails_body.append(body)
        except Exception, error:
            print 'failed to fetch new mails'
            print 'error: %s' % error

    def is_from_jira(self, subject):
        return True

if __name__ == '__main__':
    mail_process = My_Imap(HOST_ADDRESS, USERNAME, PASSWORD)
    mail_process.refresh_unseen()
    
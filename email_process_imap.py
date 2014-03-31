# coding: utf-8
import imaplib
import email
from HTMLParser import HTMLParser

HOST_ADDRESS = 'imap.126.com'
USERNAME = 'gitview'
PASSWORD = 'gitviewtest'
    

class My_Imap(object):
        
    def __init__(self, host_address, username, password):
        try:
            self.parser = My_JIRA_Html_Parser()
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
                if self.__is_from_jira(subject):
                    for part in email_msg.walk():
                        if part.get_content_type() == 'text/html':#part.get_content_type() == 'text/plain' or 
                            body = part.get_payload(decode = True)
#                             body_encode = part.get_content_charset()
#                             if body_encode == 'gb2312' or body_encode == 'gb18030':
#                                 body = body.decode('gb2312')
#                             elif body_encode == 'utf8':
#                                 body = body.decode('utf8')
                            break
                    self.parser.feed(body)
                    print self.parser.project_name, self.parser.issue_name, self.parser.sprint_name, self.parser.issue_status
                    self.parser.clear()
        except Exception, error:
            print 'failed to fetch new mails'   
            print 'error: %s' % error
            
    def close(self):
        self.imap.close()
        self.imap.logout()

    def __is_from_jira(self, subject):
        return True
    

class My_JIRA_Html_Parser(HTMLParser):
    project_name = ''
    issue_name = ''
    sprint_name = ''
    issue_status = ''
    table_count = 0
    read_info = 0
    read_first_table = False
    read_info_start = False
    read_project_start = False
    read_issue_start = False
    read_second_table = False
    read_detail_judge = False
    read_status_start = False
    read_detail_start = False
    read_sprint_start = False
    
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.table_count += 1
            if self.table_count == 4:
                self.read_first_table = True
            elif self.table_count == 5:
                self.read_second_table = True
        elif self.read_first_table and tag == 'td':
            self.read_info_start = True
        elif self.read_info_start and tag == 'a':
            self.read_info += 1
            if self.read_info == 1:
                self.read_project_start = True
            elif self.read_info == 3:
                self.read_issue_start = True
        elif self.read_second_table and tag == 'th':
            self.read_detail_judge = True
        elif (self.read_status_start or self.read_sprint_start) and tag == 'span':
            for attr in attrs:
                if 'diffaddedchars' in attr:
                    self.read_detail_start = True
    
    def handle_data(self, data):
        if self.read_project_start:
            self.project_name = data
            self.read_project_start = False
        elif self.read_issue_start:
            self.issue_name = data
            self.read_issue_start = False
            self.read_info_start = False
            self.read_first_table = False
        elif self.read_detail_judge:
            data = data.strip()
            if data == 'Status:':
                self.read_status_start = True
                self.read_detail_judge = False
                self.read_second_table = False
            elif data == 'Sprint:':
                self.read_sprint_start = True
                self.read_detail_judge = False
                self.read_second_table = False
        elif self.read_detail_start:
            if self.read_status_start:
                self.issue_status = data.strip()
                self.read_status_start = False
            elif self.read_sprint_start:
                self.sprint_name = data.strip()
                self.read_sprint_start = False
                
    def clear(self):
        self.project_name = ''
        self.issue_name = ''
        self.sprint_name = ''
        self.issue_status = ''
        self.table_count = 0
        self.read_info = 0
        self.read_first_table = False
        self.read_info_start = False
        self.read_project_start = False
        self.read_issue_start = False
        self.read_second_table = False
        self.read_detail_judge = False
        self.read_status_start = False
        self.read_detail_start = False
        self.read_sprint_start = False
    

if __name__ == '__main__':
    mail_process = My_Imap(HOST_ADDRESS, USERNAME, PASSWORD)
    mail_process.refresh_unseen()
    mail_process.close()
            

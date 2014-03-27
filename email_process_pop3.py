import poplib
from email import parser
import StringIO, rfc822

pop_conn = poplib.POP3_SSL('pop.126.com')
pop_conn.user('gitview')
pop_conn.pass_('gitviewtest')
#Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
#Parse message intom an email object:
# messages = [parser.Parser().parsestr(mssg) for mssg in messages]
# for message in messages:
#     message['subject']
for message in messages:
    file = StringIO.StringIO(message)
     
    message = rfc822.Message(file)
     
    for key in message:
        print key, "=", message[key]
     
    print message.fp.read()
pop_conn.quit()
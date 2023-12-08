import base64
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(host, port, sender, password, recipient_str, subject, message, attachment_paths):
    recipients = recipient_str.split(' ')

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient_str
    msg['Subject'] = subject

    
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    
    for attachment_path in attachment_paths:
        attach_file(msg, attachment_path)

    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        
        ehlo_command = f"EHLO {host}\r\n"
        sock.sendall(ehlo_command.encode('utf-8'))
        response = sock.recv(1024)
        print(response.decode('utf-8'))

        
        sock.sendall('AUTH LOGIN'.encode('utf-8') + b'\r\n')
        response = sock.recv(1024)

        
        sock.sendall(base64.b64encode(sender.encode('utf-8')) + b"\r\n")
        response = sock.recv(1024)

        sock.sendall(base64.b64encode(password.encode('utf-8')) + b'\r\n')
        response = sock.recv(1024)

        
        sock.sendall(b"MAIL FROM: <" + sender.encode('utf-8') + b">\r\n")
        response = sock.recv(1024)

        
        for recipient in recipients:
            sock.sendall(b"RCPT TO: <" + recipient.encode('utf-8') + b">\r\n")
            response = sock.recv(1024)

        
        sock.sendall("DATA".encode('utf-8') + b'\r\n')
        response = sock.recv(1024)

        
        sock.sendall(msg.as_string().encode('utf-8') + b"\r\n")

        
        sock.sendall(b"\r\n.\r\n")
        response = sock.recv(1024)

        sock.sendall(b"QUIT\r\n")

def attach_file(msg, attachment_path):
    # Mở và đọc nội dung của tệp tin đính kèm
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(attachment_path)}")
        msg.attach(part)

if __name__ == "__main__":
    sender = "lethanhvinh@gmail.com"
    recipient_str = input("To: ")
    subject = input('Subject: ')
    message = input("Message: ")

    attachment_paths = ["D:/test.txt", "D:/test.zip","D:/11.png","D:/Tai lieu do an mang may tinh/Tai_lieu_Socket/HDLT_Socket.pdf","C:/Users/LE THANH VINH/Downloads/CNXHKH.docx"]

    send_email("127.0.0.1", 2225, sender, 'your_password', recipient_str, subject, message, attachment_paths)

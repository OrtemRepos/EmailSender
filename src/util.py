from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


env = Environment(loader=FileSystemLoader("src/template"))

def generate_email(
    token:str,
    content_path: str,
    subject: str
) -> MIMEMultipart:
    template = env.get_template(content_path)
    html_content = template.render(token=token)
    
    message = MIMEMultipart()
    message['Subject'] = subject
    message.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    return message
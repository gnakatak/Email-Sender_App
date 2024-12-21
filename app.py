import streamlit as st # type: ignore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import importlib.util
import os

HOST = "smtp.gmail.com"
PORT = 587 

st.title("Formulário com Envio de E-mails")
st.subheader("Preencha as informações abaixo para enviar os dados por e-mail.")

# Carregar o módulo encrypt.pyc
spec = importlib.util.spec_from_file_location("encrypt", "__pycache__/encrypt.cpython-312.pyc")
encrypt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(encrypt)

# Definindo remetente e senha
sender = "gabrielmparrini@gmail.com"
password = encrypt.decrypt("n83f y^9e pl7z x+g7")  # Decrypt a senha do Gmail

# Coletar informações do destinatário, mensagem e arquivos
receiver = st.text_input("Escreva o e-mail para enviar", placeholder="escreva aqui")
text = st.text_area("Mensagem", placeholder="escreva a mensagem", height=200)
email = receiver.split(",")
email = [i.strip() for i in email]
file = st.file_uploader("Arquivos", type=None, accept_multiple_files=True)

# Repassar os arquivos para pastas específicas
folder = "arquivos"
os.makedirs(folder, exist_ok=True)



if st.button("Enviar Email"):
    if receiver and text:    
        servidor = smtplib.SMTP(HOST, PORT)
        servidor.starttls()
        servidor.login(sender, password)
        mensagem = MIMEMultipart()
        mensagem["From"] = sender
        mensagem["To"] = ", ".join(email)
        mensagem["Subject"] = "email sender app"
        mensagem.attach(MIMEText(text,"plain"))

        if file:
            for uploaded_file in file:
                file_name = uploaded_file.name
                file_type = file_name.split(".")[-1]
                file_type_path = os.path.join(folder,file_type)
                os.makedirs(file_type_path, exist_ok=True)
                file_path = os.path.join(file_type_path, file_name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
                part = MIMEBase("application", "octet-stream")
                part.set_payload(uploaded_file.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={uploaded_file.name}")
                mensagem.attach(part)
        
        mensagem["Cc"] = sender
        servidor.send_message(mensagem)
        st.success("E-mail enviado com sucesso!")
    else: 
        st.warning("Por favor, preencha todos os campos.")
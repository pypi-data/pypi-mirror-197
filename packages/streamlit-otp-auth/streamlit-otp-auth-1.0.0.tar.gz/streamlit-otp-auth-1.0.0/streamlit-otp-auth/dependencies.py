import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import yaml
import bcrypt
import random
import smtplib
import os
from dotenv import find_dotenv,load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
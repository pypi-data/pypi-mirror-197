from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.0'
DESCRIPTION = 'This package allows you to create an authntication system in streamlit'
LONG_DESCRIPTION = 'Streamlit Authentication System With Sign-UP,Login,Reset PAssword and OTP Verification Functions'

# Setting up
setup(
    name="streamlit-otp-auth",
    version=VERSION,
    author="Anjishnu SAw",
    author_email="anjishnusaw91@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['streamlit', 'random', 'yaml','bcrypt','smtplib','dotenv'],
    keywords=['python', 'authentication', 'signup-login', 'otp', 'secure auth', 'streamlit authenticator'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
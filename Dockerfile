# # Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# # Set the working directory to /app
WORKDIR /app

# Install Tesseract OCR and its English language data
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get install -y tesseract-ocr-eng
RUN apt-get install -y ocrmypdf


# # Copy the current directory contents into the container at /app
COPY --chown=1000:1000 . /app


# # Install any needed packages specified in requirements.txt


# # RUN pip3 install cdifflib --no-cache-dir 
# # RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# RUN apt-get update && apt-get install -y gcc libgl1-mesa-glx  libglib2.0-0 libsm6 libxrender1 libxext6
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libstdc++6 \
    python3-dev

#  && \ pip3 install --no-cache-dir -r requirements.txt
# RUN pip install ultralytics
RUN pip install transformers
RUN pip install fastapi
RUN pip install uvicorn

RUN pip install python-multipart
RUN pip install pdfplumber==0.6.0
RUN pip install pytesseract==0.3.8
RUN pip install ocrmypdf==12.7.2
RUN pip install pikepdf==2.16.1
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install streamlit

EXPOSE 8510
# # Run the command to start the app
# CMD uvicorn main:app --host 0.0.0.0
CMD streamlit run app.py

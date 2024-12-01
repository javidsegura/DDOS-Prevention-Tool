FROM python:3.11-slim

# Install necessary tools for VS Code remote development
RUN apt-get update && \
    apt-get install -y \
        nano \
        gcc \ 
        sudo 

WORKDIR /home
COPY . /home

RUN pip3 install -r defense_requirements.txt --no-cache-dir

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
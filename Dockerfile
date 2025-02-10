FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y wkhtmltopdf nodejs npm

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install nodemon
RUN npm install -g nodemon

COPY . .

CMD ["nodemon", "--ignore", "*.pdf", "--exec", "python", "app.py"]

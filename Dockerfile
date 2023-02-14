FROM python:3.10

WORKDIR /fanat_kg

COPY req.txt ./
RUN pip install --no-cache-dir -r req.txt

COPY . .

CMD [ "python", "main.py" ]



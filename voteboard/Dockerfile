FROM python:latest
ENV FLASK_APP=main.py
COPY --chown=root:root . ./voteboard
WORKDIR ./voteboard
RUN useradd -ms /bin/bash app
RUN chown -R app db/
RUN pip3 install -r requirements.txt
EXPOSE 8080
USER app
COPY flag.txt /flag.txt
CMD ["python", "main.py", "--host=0.0.0.0"]
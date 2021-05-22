# Dockerfile to host the data as FastAPI
FROM python:3.7.4-stretch

WORKDIR /home/user

# copy code
COPY bed_data.py config.py run.py st_app.py /home/user/

# install as a package
COPY setup.py requirements.txt README.md /home/user/
RUN pip install -r requirements.txt
RUN pip install -e .

# copy api code
COPY api /home/user/api
COPY data /home/user/data

EXPOSE 8000

# cmd for running the API
CMD ["gunicorn", "api.application:app",  "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "180"]

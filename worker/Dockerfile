FROM python:3.6
ENV PYTHONUNBUFFERED 1
ARG LIB_VERSION

#Docker file that pulls LigoLib package from PyPI (instead of copying source code) and
#build docker image for celery worker(s)

ENV LIB_VERSION=${LIB_VERSION}

# Docker file for forming local/dev Django container
RUN mkdir -p /user_data/media/datasets /user_data/media/linking
RUN mkdir /tmp/django-email-dev
# Ownership change not a requirement for local/dev docker environments
RUN chmod -R 0777 /user_data

RUM mkdir /dist
COPY ../dist/*.whl  /dist/

# Install Celery Requirements
COPY ./link-server /worker
RUN pip install -r /worker/requirements.txt \
 && echo $LIB_VERSION

# Install Data Linking Package

#this one would not always try to see beyond what is previously cached
#RUN pip install --extra-index-url https://testpypi.python.org/pypi LigoLib

#this one would try to get the latest (does not always work consistently from all env)
#RUN pip3 install --no-cache-dir --upgrade --extra-index-url https://testpypi.python.org/pypi LigoLib
#RUN pip3 install --no-cache-dir --upgrade   --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple  LigoLib


#this one would try to get a specific version of LigoLib
#experimental

#RUN pip3 install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple LigoLib==${LIB_VERSION}

#Installed LigoLib from locally formed wheel distribution
#for could be combined with previous copy and run statements; however keeping it separate for ease of commenting out and uncommenting
#one of the installation choices of ligolib package or the other
#removing wheel file and ftemporary package folder after installation

RUN pip3 install /dist/*.whl \
    && rm -rf /dist/  

RUN echo 'django:x:999:999:django:/:/bin/sh' >> /etc/passwd

RUN chown 999:999 -R /worker
RUN chown 999:999 -R /user_data
RUN chown 999:999 -R /tmp

USER "999:999"
WORKDIR /worker

ENTRYPOINT ["celery", "-A", "tasks", "worker", "--loglevel=info"]

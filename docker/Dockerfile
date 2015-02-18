FROM centos:7
MAINTAINER Vincent Van der Kussen "vincent@vanderkussen.org"

RUN yum install -y python-setuptools httpd mod_wsgi
RUN easy_install pip
RUN mkdir -p /opt/jetfire/{client,app}
#RUN mkdir -p /var/www/html/jetfire/{client,app}

ADD requirements.txt /tmp/
#ADD app /opt/jetfire/app
ADD config.cfg /opt/jetfire/
#ADD config.cfg /var/www/html/jetfire/
ADD run.py /opt/jetfire/
#ADD run.py /var/www/html/jetfire/
#ADD jetfire.conf /etc/httpd/conf.d/
ADD jetfire.conf /opt/jetfire/
#ADD jetfire.wsgi /var/www/html/jetfire/
RUN pip install -r /tmp/requirements.txt

ENV DOCKERSRV mongo

EXPOSE 5000
CMD python /opt/jetfire/run.py

#EXPOSE 80

#ENTRYPOINT ["/usr/sbin/apachectl"]
#CMD ["-D", "FOREGROUND"]

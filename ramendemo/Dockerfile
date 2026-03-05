FROM registry.access.redhat.com/ubi8/python-38
#FROM docker.io/centos:centos7
ENV ENABLE_MICROPIPENV="1" \
    UPGRADE_PIP_TO_LATEST="1"
USER root

RUN yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm -y
RUN wget https://repo.mysql.com/mysql80-community-release-el8-1.noarch.rpm
RUN yum localinstall mysql80-community-release-el8-1.noarch.rpm -y
RUN yum install python3-mysqlclient mysql-connector-odbc gcc unixODBC-devel -y

RUN python -m pip install --upgrade pip
RUN pip3 install shortuuid mysqlclient mysql-connector mysql-connector-python pyodbc

#RUN yum install gcc unixODBC-devel python3-mysqlclient mysql-connector-odbc -y
#RUN python -m pip install --upgrade pip
#RUN pip3 install shortuuid mysqlclient mysql-connector mysql-connector-python pyodbc

WORKDIR /tmp
ADD *.py .

ENTRYPOINT [ "python3", "/tmp/runloop.py --size --server" ]

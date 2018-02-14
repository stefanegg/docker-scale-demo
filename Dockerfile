FROM alpine:latest

# install Python with web.py
RUN	apk update && \
	apk add python && \
	wget http://webpy.org/static/web.py-0.38.tar.gz && \
	tar xvzf web.py* && \
	cd web.py* && \
	/usr/bin/python setup.py install && \
	cd / && \
	rm -R web.py*

ADD webapp /webapp

EXPOSE 8080

VOLUME /host_hostname

ENV app_version=1.1

# Entry point
CMD ["/usr/bin/python", "/webapp/restserver.py"]

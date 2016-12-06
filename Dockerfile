FROM python:3.5

# Install uWSGI
RUN pip install uwsgi

RUN apt-get install -y nodejs npm
RUN npm -g install yuglify

# Standard set up Nginx
ENV NGINX_VERSION 1.9.11-1~jessie
ENV DJANGO_SETTINGS_MODULE yevent.settings
ENV PYTHONUNBUFFERED 1

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
	&& rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log
EXPOSE 8000
# Finished setting up Nginx

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# Copy the modified Nginx conf
COPY docker/config/nginx/* /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY docker/config/uwsgi.ini /etc/uwsgi/

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
# Custom Supervisord config
COPY docker/config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD . /app/
RUN rm -rf static_root
RUN python manage.py collectstatic --no-input --no-color
CMD ["/usr/bin/supervisord"]
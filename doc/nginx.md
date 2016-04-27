nginx
======

### Run In docker
--------------
```
docker run -tid --name nginx8089 -p 8089:80 -v /docker-config/nginx_ldap.conf:/etc/nginx/conf.d/default.conf -v /docker-config/index.html:/var/www/index.html cdkdc.domain.org:5000/nginx:latest
```

### nginx_ldap
--------------
```
FROM debian:8.4

MAINTAINER rainysia "rainysia#gmail.com"

# Define some variables.
ENV NGINX_VERSION release-1.10.0

# Install needed packages, compile and install.
# Remove unused packages and cleanup some directories.
RUN \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        ca-certificates \
        git \
        gcc \
        make \
        libpcre3-dev \
        zlib1g-dev \
        libldap2-dev \
        libssl-dev \
        wget && \
    mkdir /var/log/nginx && \
    mkdir /etc/nginx && \
    cd /tmp && \
    git clone https://github.com/kvspb/nginx-auth-ldap.git && \
    git clone https://github.com/nginx/nginx.git && \
    cd /tmp/nginx && \
    git checkout tags/${NGINX_VERSION} && \
    ./auto/configure \
        --add-module=/tmp/nginx-auth-ldap \
        --with-http_ssl_module \
        --with-http_gzip_static_module \
        --with-pcre \
        --with-debug \
        --conf-path=/etc/nginx/nginx.conf \ 
        --sbin-path=/usr/sbin/nginx \ 
        --pid-path=/var/log/nginx/nginx.pid \ 
        --error-log-path=/var/log/nginx/error.log \ 
        --http-log-path=/var/log/nginx/access.log && \ 
    make install && \
    apt-get purge -y \
        git \
        gcc \
        make \
        libpcre3-dev \
        zlib1g-dev \
        libldap2-dev \
        libssl-dev \
        wget && \
    apt-get autoremove -y && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/src/* && \
    rm -rf /tmp/* && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/man/* && \
    rm -rf /usr/share/locale/*

#
# link access and error logs to docker log collector.
#
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log


#
# Expose ports.
#
EXPOSE 80 443

#
# Start nginx.
#
CMD ["nginx", "-g", "daemon off;"]

```

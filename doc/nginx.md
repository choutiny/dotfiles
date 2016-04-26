nginx
======

### Run In docker
--------------
```
docker run -tid --name nginx8089 -p 8089:80 -v /docker-config/nginx_ldap.conf:/etc/nginx/conf.d/default.conf -v /docker-config/index.html:/var/www/index.html cdkdc.domain.org:5000/nginx:latest
```

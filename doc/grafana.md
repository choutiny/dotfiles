Grafana
=========
[Grafana official](http://grafana.org/)
[Grafana github](https://github.com/grafana/grafana)
[Grafana Docker](https://github.com/grafana/grafana-docker)

###Run
---------------
```
docker run -d --name=grafana -p 3000:3000 grafana/grafana
docker run -d  --restart=always -p 3000:3000 --name grafana 
docker run -d  --restart=always -p 3000:3000 --name grafana \
    -v /docker-config/grafana/grafana.ini:/etc/grafana/grafana.ini \
    -v /docker-config/grafana/ldap.toml:/etc/grafana/ldap.toml  cdkdc.synnex.org:5000/grafana
```
###Configuration
---------------
/etc/grafana/grafana.ini


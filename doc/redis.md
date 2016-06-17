redis
==========

### install
-----------
centos7
```
wget -r --no-parent -A 'epel-release-*.rpm' http://dl.fedoraproject.org/pub/epel/7/x86_64/e/
rpm -Uvh dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-*.rpm
yum install redis
systemctl start redis.service
systemctl status redis.service
```

### configure
-----------
/etc/redis.conf
/etc/redis-sentinel.conf
```
bind 0.0.0.0
```

### command
-----------
redis-cli -h 192.168.85.119 -p 6379

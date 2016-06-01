IPSEC for debian8 
===================
[strongswan-howto-create-your-own-vpn](https://www.zeitgeist.se/2013/11/22/strongswan-howto-create-your-own-vpn/)

### Install
----------
```
debian8
apt-get install strongswan libcharon-extra-plugins
or debian7
echo "deb http://ftp.debian.org/debian wheezy-backports main" \
    > /etc/apt/sources.list.d/wheezy-backports.list
apt-get update
apt-get -t wheezy-backports install strongswan libcharon-extra-plugins

ipsec version
```

### Configure
----------
```
cd /etc/ipsec.d
ipsec pki --gen --type rsa --size 4096 \
    --outform pem \
    > private/strongswanKey.pem
chmod 600 private/strongswanKey.pem
ipsec pki --self --ca --lifetime 3650 \
    --in private/strongswanKey.pem --type rsa \
    --dn "C=CH, O=strongSwan, CN=strongSwan Root CA" \
    --outform pem \
    > cacerts/strongswanCert.pem

ipsec pki --gen --type rsa --size 2048 \
    --outform pem \
    > private/vpnHostKey.pem
chmod 600 private/vpnHostKey.pem

Replace your vpn.domain for "vpn.zeitgeist.se"

ipsec pki --pub --in private/vpnHostKey.pem --type rsa | \
    ipsec pki --issue --lifetime 730 \
    --cacert cacerts/strongswanCert.pem \
    --cakey private/strongswanKey.pem \
    --dn "C=CH, O=strongSwan, CN=vpn.zeitgeist.se" \
    --san vpn.zeitgeist.se \
    --flag serverAuth --flag ikeIntermediate \
    --outform pem > certs/vpnHostCert.pem

Replace your username for "Alexander"
ipsec pki --gen --type rsa --size 2048 \
    --outform pem \
    > private/AlexanderKey.pem

chmod 600 private/AlexanderKey.pem

Replace your full domain for "zeitgeist.se"
ipsec pki --pub --in private/AlexanderKey.pem --type rsa | \
    ipsec pki --issue --lifetime 730 \
    --cacert cacerts/strongswanCert.pem \
    --cakey private/strongswanKey.pem \
    --dn "C=CH, O=strongSwan, CN=alexander@zeitgeist.se" \
    --san alexander@zeitgeist.se \
    --outform pem > certs/AlexanderCert.pem

openssl pkcs12 -export -inkey private/AlexanderKey.pem \
    -in certs/AlexanderCert.pem -name "Alexander's VPN Certificate" \
    -certfile cacerts/strongswanCert.pem \
    -caname "strongSwan Root CA" \
    -out Alexander.p12
will input a password, remember it
```

### /etc/ipsec.conf
----------
```
# ipsec.conf - strongSwan IPsec configuration file

config setup  
    # uniqueids=never
    charondebug="cfg 2, dmn 2, ike 2, net 2"

conn %default  
    keyexchange=ikev2
    ike=aes128-sha256-ecp256,aes256-sha384-ecp384,aes128-sha256-modp2048,aes128-sha1-modp2048,aes256-sha384-modp4096,aes256-sha256-modp4096,aes256-sha1-modp4096,aes128-sha256-modp1536,aes128-sha1-modp1536,aes256-sha384-modp2048,aes256-sha256-modp2048,aes256-sha1-modp2048,aes128-sha256-modp1024,aes128-sha1-modp1024,aes256-sha384-modp1536,aes256-sha256-modp1536,aes256-sha1-modp1536,aes256-sha384-modp1024,aes256-sha256-modp1024,aes256-sha1-modp1024!
    esp=aes128gcm16-ecp256,aes256gcm16-ecp384,aes128-sha256-ecp256,aes256-sha384-ecp384,aes128-sha256-modp2048,aes128-sha1-modp2048,aes256-sha384-modp4096,aes256-sha256-modp4096,aes256-sha1-modp4096,aes128-sha256-modp1536,aes128-sha1-modp1536,aes256-sha384-modp2048,aes256-sha256-modp2048,aes256-sha1-modp2048,aes128-sha256-modp1024,aes128-sha1-modp1024,aes256-sha384-modp1536,aes256-sha256-modp1536,aes256-sha1-modp1536,aes256-sha384-modp1024,aes256-sha256-modp1024,aes256-sha1-modp1024,aes128gcm16,aes256gcm16,aes128-sha256,aes128-sha1,aes256-sha384,aes256-sha256,aes256-sha1!
    dpdaction=clear
    dpddelay=300s
    rekey=no
    left=%any
    leftsubnet=0.0.0.0/0
    leftcert=vpnHostCert.pem
    right=%any
    rightdns=8.8.8.8,8.8.4.4
    rightsourceip=172.16.16.0/24

conn IPSec-IKEv2  
    keyexchange=ikev2
    auto=add

conn IPSec-IKEv2-EAP  
    also="IPSec-IKEv2"
    rightauth=eap-mschapv2
    rightsendcert=never
    eap_identity=%any

conn CiscoIPSec  
        keyexchange=ikev1
        leftsendcert=never
        #do not need server side cert
        leftauth=psk
        rightauth=psk
        #use PSK as client server auth type
        rightauth2=xauth
        #use xauth as user login auth type
        auto=add
```

### /etc/ipsec.secrets
----------
Replace your password for "yourpasswd1"
Replace your username for "user1"
```
: PSK "yourpasswd1"
: RSA vpnHostKey.pem
user1 : EAP "yourpasswd1"
user : XAUTH "yourpasswd1"
```
ipsec rereadsecrets

### iptables rules
----------
Replace your server IP for "xxx.xxx.xxx.xxx"
```
echo 1 > /proc/sys/net/ipv4/ip_forward
echo 0 > /proc/sys/net/ipv4/conf/all/accept_redirects
echo 0 > /proc/sys/net/ipv4/conf/all/send_redirects
iptables -t nat -A POSTROUTING -o eth0 ! -p esp \
    -j SNAT --to-source xxx.xxx.xxx.xxx

iptables -A INPUT -p udp --dport 500 --j ACCEPT
iptables -A INPUT -p udp --dport 4500 --j ACCEPT
iptables -A INPUT -p esp -j ACCEPT
```

### restart
----------
```
service ipsec restart
```

### Iphone
----------
```
Type=IPSec
Server=vpn.yourdomain.com
Account=user1
password...
```

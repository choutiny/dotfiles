php composer
============

### Install
------------
```
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer
```
or 
```
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('SHA384', 'composer-setup.php') === '070854512ef404f16bac87071a6db9fd9721da1684cd4589b1196c3faf71b9a2682e2311b36a5079825e155ac7ce150d') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
```

options
```
--install-dir 
    php composer-setup.php --install-dir=bin
--filename
    php composer-setup.php --filename=composer
--version
    php composer-setup.php --version=1.0.0-alpha8

download the stable version, preview will download pre-release version
    composer self-update
--preview
    composer self-update --preview
--snapshot
    composer self-update --snapshot
```

go to project folder and run the below command
```
php composer.phar install/update
composer install
```

### RD command 
------------


### composer.json
------------
```
{
    "require": {
        "xxx/xxx": "dev"
    },
    "autoload": {
        
    }

}
```

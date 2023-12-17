# Taro Telegram Bot

Taro Telegram Bot - Bot tells fortunes using tarot cards.

Development details: https://miro.com/app/board/uXjVNO9cbEw=/

## Tech

This is what the bot uses:

- [aiogram](https://github.com/aiogram/aiogram/tree/v2.22.2) - asynchronous library for writing telegram bots.
- [asyncpg](https://github.com/MagicStack/asyncpg/tree/v0.28.0) - asynchronous library for interacting with the database (PostgreSQL).
- [PostgreSQL](https://www.postgresql.org/about/news/postgresql-14-released-2318/) - open source object-relational database system for data storage.
- [NGINX](https://nginx.org/en/) - web server for web hooks.

## Installation

Requires [Python](https://www.python.org/downloads/release/python-3100/) v3.8+ to run.

Install the dependencies:

```sh
git clone git@github.com:GSemix/Cyber_Security_Telegram_Bot.git
cd Cyber_Security_Telegram_Bot
python3 -m venv venv
. venv/bin/active
pip3 install -r requirements.txt
touch .env
```

Next you need to set the configuration in .env(If you start on pooling, then in the first paragraph you only need a token):

```sh
TELEGRAM_token=63967534a296:AaKg8MtUxsdlvjsdlv6Y7V6U1HLy_UNeCo
TELEGRAM_webhook_host=https://ab123708.tw1.ru
TELEGRAM_webhook_path=/bot
TELEGRAM_webhook_url=https://ab123708.tw1.ru/bot
TELEGRAM_webapp_host=127.0.0.1
TELEGRAM_webapp_port=3001

TELEGRAM_LOGGING_level=INFO
TELEGRAM_LOGGING_fmt=%(asctime)s : %(levelname)s : %(pathname)s : %(funcName)s : %(message)s
TELEGRAM_LOGGING_datefmt=%Y-%m-%d %H:%M:%S
TELEGRAM_LOGGING_name=telegram_logger
TELEGRAM_LOGGING_path=app/logs/
TELEGRAM_LOGGING_max_bytes=10485760
TELEGRAM_LOGGING_backup_count=10

POSTGRESQL_host=127.0.0.1
POSTGRESQL_port=5432
POSTGRESQL_user=myuser
POSTGRESQL_password=mypass
POSTGRESQL_database=mybase
POSTGRESQL_min_size=3
POSTGRESQL_max_size=10
POSTGRESQL_max_queries=500

POSTGRESQL_LOGGING_level=INFO
POSTGRESQL_LOGGING_fmt=%(asctime)s : %(levelname)s : %(pathname)s : %(funcName)s : %(message)s
POSTGRESQL_LOGGING_datefmt=%Y-%m-%d %H:%M:%S
POSTGRESQL_LOGGING_name=postgresql_logger
POSTGRESQL_LOGGING_path=app/logs/
POSTGRESQL_LOGGING_max_bytes=10485760
POSTGRESQL_LOGGING_backup_count=10
```

After the correctly entered config, launch the bot:

```sh
python3 -m app
```

## PostgreSQL

Running by example Ubuntu Server 22.04 installation and setting PostgreSQL 14

### Installation

```sh
apt install postgresql-14 postgresql-contrib-14 -y
systemctl start postgresql.service
systemctl status postgresql.service
systemctl enable postgresql.service
```

### Example of creating a user and his db

```sh
su postgres
psql
CREATE DATABASE example_db;
CREATE USER example_name WITH ENCRYPTED PASSWORD 'example_pass';
GRANT ALL PRIVILEGES ON DATABASE example_db TO example_name;
\l
```

### An example of opening access to the entire database to everyone from outside with password

In /etc/postgresql/.../postgresql.conf:

```sh
listen_addresses = '*'
```

In /etc/postgresql/.../pg_hba.conf(append last line):

```sh
host all all 0.0.0.0/0 password
```

Let's open the port and restart PostgreSQL:

```sh
ufw allow 5432
ufw reload
systemctl restart postgresql.service
```

Check connections if present:

```sh
netstat -pant | grep postgres
ss -ltn
nmap -sS -O example_domen.ru
```

### Example of changing the 'postgres' user password

```sh
passwd postgres
su postgres
psql
ALTER USER postgres WITH PASSWORD 'example_pass';
```

### Initial configuration setup of PostgreSQL

The configuration file is located in /etc/postgresql/.../postgresql.conf. 
A [site](https://pgtune.leopard.in.ua) that can generate the initial configuration.

Restart the service:

```sh
systemctl restart postgresql.service
```

## NGINX

Running by example Ubuntu Server 22.04 installation and setting NGINX SSL for WebHooks

### Installation

Installing dependencies:

```sh
sudo snap install core; sudo snap refresh core
sudo apt install certbot
sudo apt install nginx
sudo apt install python3-certbot-nginx
```

Firewall setup:

```sh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'
sudo ufw reload
sudo ufw status
```

Obtaining a domain ssl certificate(which is tied to the ip of this server):

```sh
certbot --nginx -d example_domen.ru
```

### Configuring nginx for WebHook

Example /etc/nginx/sites-avaliable/example for webhook:

```sh
server {
    listen 80;
    server_name example_domen.ru;

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
        listen 443 ssl;
        server_name example_domen.ru;

        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_certificate /etc/letsencrypt/live/example_domen.ru/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example_domen.ru/privkey.pem;

        location /bot {
            proxy_pass         http://127.0.0.1:3001;
            proxy_redirect     off;
	    proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
        }
}
```

Let's check the configuration and restart the service:

```sh
ln -s /etc/nginx/sites-available/example /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

Add to certificate auto-renewal:

```sh
echo -e '0 0 * * * certbot renew --quiet' | sudo crontab -
```

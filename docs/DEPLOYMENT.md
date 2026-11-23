# PARTBASE Production Deployment Guide

This guide details running PARTBASE on Linux Ubuntu with Gunicorn, Nginx, and Systemd.

## 1. Prerequisites

- Python 3.12+
- Nginx
- Certbot (Let's Encrypt SSL)
- SQLite or PostgreSQL

## 2. Systemd Service Configuration

Create `/etc/systemd/system/partbase.service`:

```ini
[Unit]
Description=PARTBASE Flask Application Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/partbase
Environment="PATH=/var/www/partbase/venv/bin"
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=generate-secure-random-key"
ExecStart=/var/www/partbase/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 wsgi:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable partbase
sudo systemctl start partbase
```

## 3. Nginx Reverse Proxy Setup

Create `/etc/nginx/sites-available/partbase`:

```nginx
server {
    listen 80;
    server_name partbase.chennai.in www.partbase.chennai.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/partbase/app/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

Enable the site and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/partbase /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

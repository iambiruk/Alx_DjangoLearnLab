
DOMAIN="yourdomain.com"
EMAIL="admin@yourdomain.com"

sudo apt update
sudo apt install certbot python3-certbot-nginx

sudo systemctl stop nginx

sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m $EMAIL

sudo systemctl start nginx

echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo tee -a /etc/crontab

sudo chmod 755 /etc/letsencrypt/live/
sudo chmod 755 /etc/letsencrypt/archive/
sudo chmod 644 /etc/letsencrypt/live/$DOMAIN/fullchain.pem
sudo chmod 644 /etc/letsencrypt/live/$DOMAIN/privkey.pem

echo "SSL certificate setup completed for $DOMAIN"

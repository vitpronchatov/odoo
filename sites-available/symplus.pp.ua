server {
listen 80;
server_name symplus.pp.ua;
return 301 https://$host$request_uri;
}

server {
listen 443 ssl;
server_name symplus.pp.ua;
ssl_certificate /etc/nginx/ssl/certificate.crt;
ssl_certificate_key /etc/nginx/ssl/private.key;
access_log /var/log/nginx/symplus.pp.ua.access.log;
error_log /var/log/nginx/symplus.pp.ua.error.log;
location / {
	proxy_pass http://127.0.0.1:8069;
}
}

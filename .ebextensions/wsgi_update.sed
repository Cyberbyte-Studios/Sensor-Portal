/<Virtual/ a\
RewriteEngine On\
RewriteCond %{HTTP:Authorization} ^(.*)\
RewriteRule .* - [e=HTTP_AUTHORIZATION:%1]

/<\/Virtual/ a\
WSGIPassAuthorization On\
WSGIApplicationGroup %{GLOBAL}

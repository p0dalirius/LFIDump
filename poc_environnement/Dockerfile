FROM debian:buster

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -qq -y update; \
    apt-get -qq -y install software-properties-common curl apache2 php php-xml php-curl; \
    rm /var/www/html/index.*

RUN echo '<?php echo file_get_contents($_GET["page"]); ?>' > /var/www/html/lfi.php

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]
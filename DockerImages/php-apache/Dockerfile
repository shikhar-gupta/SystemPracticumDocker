FROM base-php-apache
RUN service ssh start
RUN service apache2 start || service apache2 restart
ADD supervisord.conf /etc/
CMD ["supervisord","-n"]

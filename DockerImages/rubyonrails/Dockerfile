FROM base-php-apache
RUN service ssh start
ADD supervisord.conf /etc/
CMD ["supervisord","-n"]

FROM base-mysql
RUN service ssh start
RUN service mysql start || service mysql restart
ADD supervisord.conf /etc/
CMD [ "supervisord", "-n"] 

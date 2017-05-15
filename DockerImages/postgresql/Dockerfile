FROM base-postgresql
RUN service ssh start
ADD supervisord.conf /etc/
CMD ["supervisord","-n"]

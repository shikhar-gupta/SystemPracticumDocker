FROM base-redis
RUN service ssh start
ADD supervisord.conf /etc/
CMD ["supervisord","-n"]

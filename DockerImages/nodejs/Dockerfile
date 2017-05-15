FROM base-nodejs
RUN service ssh start
ADD ./data/ /home/.
ADD supervisord.conf /etc/
CMD ["supervisord","-n"]

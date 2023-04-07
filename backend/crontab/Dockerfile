FROM ubuntu:latest
MAINTAINER baeldung.com

#Install Cron
RUN apt-get update
RUN apt-get -y install cron curl

# Add the cron job
RUN crontab -l | { cat; echo "* * * * * curl https://cooler.amos.wtf/api/maintenance --header \"Authorization: \$MEROSS_CREDENTIAL\" -X POST"; } | crontab -

RUN echo "printenv | grep -v \"no_proxy\" >> /etc/environment\ncron -f" > /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the command on container startup
CMD /entrypoint.sh

docker and docker compose were already installed before

Created a container with a flask app that runs on 8128 port locally 

The app has a text form to receive inputted message_id value

The received message id is sent via a get request to elasticsearch EKS cluster to receive the output of how the Rspamd spam filter module scanned the email message
The ouput has info about the spam score it received, what rspamd patterns were triggered and shows a detailed description per main of the rspamd patterns triggered that should be resovled for the email to pass the filtration.

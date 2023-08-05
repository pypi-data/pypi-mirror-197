import logging
import json
from base64 import b64encode

from airflow.providers.google.cloud.hooks.pubsub import PubSubHook
from awehflow.events.base import EventHandler


class PublishToGooglePubSubEventHandler(EventHandler):
    def __init__(self, project_id, topic, gcp_conn_id='google_cloud_default'):
        self.project_id = project_id
        self.topic = topic
        self.pubsub_hook = PubSubHook(gcp_conn_id=gcp_conn_id)
        credential_email = self.pubsub_hook._get_credentials_email()
        logging.info(f"Created PubSubHook with account: {credential_email}")

    def catch_all(self, event):
        self.__emit_message(event)

    def __emit_message(self, message={}):
        message = {
            'data': self.__encode_message(message)
        }
        self.__emit_batch([message])

    def __emit_batch(self, messages):
        self.pubsub_hook.publish(self.project_id, self.topic, messages)

    @staticmethod
    def __encode_message(message):
        return b64encode(json.dumps(message).encode()).decode()
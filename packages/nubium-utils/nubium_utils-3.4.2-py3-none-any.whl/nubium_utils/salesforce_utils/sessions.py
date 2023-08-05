import logging
from os import environ

import requests
from simple_salesforce import Salesforce

LOGGER = logging.getLogger(__name__)


def get_salesforce_session():
    if environ.get('SALESFORCE_USE_LIGHTNING', '').lower() == 'true':
        return get_salesforce_lightning_session()
    return get_salesforce_legacy_session()


def get_salesforce_legacy_session():
    domain = 'login'
    if environ.get('SALESFORCE_USE_SANDBOX', '').lower() == 'true':
        domain = 'test'
        LOGGER.info('Using the SANDBOX instance of Salesforce API')

    return Salesforce(
        username=environ['SALESFORCE_USERNAME'],
        password=environ['SALESFORCE_API_PASSWORD'],
        security_token=environ['SALESFORCE_API_SECURITY_TOKEN'],
        domain=domain,
        client_id=f'MODE-{environ["NU_APP_NAME"]}')


def get_salesforce_lightning_session():
    authorization_response = get_authorization()

    return Salesforce(
        instance_url=authorization_response.json()["instance_url"],
        session_id=authorization_response.json()["access_token"])


def get_authorization():
    url = 'https://salesforce.com/services/oauth2/token'
    if environ.get('SALESFORCE_USE_SANDBOX', '').lower() == 'true':
        url = 'https://test.salesforce.com/services/oauth2/token'
        LOGGER.info('Using the SANDBOX instance of Salesforce API')

    params = {
        'grant_type': "password",
        'client_id': environ['SALESFORCE_LIGHTNING_STREAMS_CLIENT_ID'],
        'client_secret': environ['SALESFORCE_LIGHTNING_STREAMS_CLIENT_SECRET'],
        'username': environ['SALESFORCE_LIGHTNING_USERNAME'],
        'password': environ['SALESFORCE_LIGHTNING_API_PASSWORD'] + environ['SALESFORCE_LIGHTNING_API_SECURITY_TOKEN']}

    return requests.post(url=url, data=params)

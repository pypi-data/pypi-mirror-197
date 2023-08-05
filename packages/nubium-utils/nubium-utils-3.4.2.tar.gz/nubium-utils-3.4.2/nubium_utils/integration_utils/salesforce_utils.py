import logging

import pytest

from nubium_utils.salesforce_utils.sessions import get_salesforce_session

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def salesforce_session():
    return get_salesforce_session()


@pytest.fixture()
def create_delete_leads(salesforce_session, format_external_create):
    """
    Since any given email address may have multiple leads, need a way to differentiate them. Made a special field
    that you can denote to designate which lead_id to use, and it'll store it as part of the key. Will work without it.
    """
    lead_ids = {}
    LOGGER.info("Creating leads...")
    for record in format_external_create:
        if '--NUBIUM_SF_LEAD_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_LEAD_IDX--")}'
        else:
            field_key = record["Email"]
        lead_ids[field_key] = salesforce_session.Lead.create(record)['id']
    yield lead_ids
    for lead_id in lead_ids.values():
        try:
            salesforce_session.Lead.delete(lead_id)
            LOGGER.info(f"Deleted lead id {lead_id}...")
        except Exception:
            LOGGER.info(f"{lead_id} appears to already be deleted.")


@pytest.fixture()
def update_leads(salesforce_session, create_delete_leads, format_external_update):
    for record in format_external_update:
        if '--NUBIUM_SF_LEAD_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_LEAD_IDX--")}'
        else:
            field_key = record["Email"]
        salesforce_session.Lead.update(create_delete_leads[field_key], record)


@pytest.fixture()
def delete_leads(salesforce_session, create_delete_leads, format_external_delete):
    for record in format_external_delete:
        if '--NUBIUM_SF_LEAD_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_LEAD_IDX--")}'
        else:
            field_key = record["Email"]
        salesforce_session.Lead.delete(create_delete_leads[field_key])

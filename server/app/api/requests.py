import os
from docusign_esign import ApiException
from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin

from app.api.utils import process_error, check_token
from app.document import DsDocument
from app.envelope import Envelope
from app.extensions import Extensions

from .session_data import SessionData
from app.ds_config import CONNECTED_FIELDS_BASE_HOST
import json


requests = Blueprint('requests', __name__)

@requests.route('/extensionApps', methods=['GET'])
@cross_origin()
def extension_apps():
    """Request for extension apps"""

    access_token = session.get('access_token')
    account_id = session.get('account_id')

    try:
        extensions = Extensions.getExtensions(account_id, access_token, CONNECTED_FIELDS_BASE_HOST)

        session['extensions'] = json.dumps(extensions)
        actual_app_ids = [item["appId"] for item in extensions]

        address_extension_id = Extensions.getAddressExtensionId()
        email_extension_ids = Extensions.getEmailExtensionIds()

        has_required_app = address_extension_id in actual_app_ids
        has_at_least_one_optional = any(app_id in actual_app_ids for app_id in email_extension_ids)

        has_all_app_ids = has_required_app and has_at_least_one_optional
    except ApiException as exc:
        return process_error(exc)
    return jsonify({'areExtensionsPresent': has_all_app_ids})


@requests.route('/requests/claim', methods=['POST'])
@cross_origin()
@check_token
def submit_claim():
    """Submit a claim"""
    try:
        req_json = request.get_json(force=True)
    except TypeError:
        return jsonify(message='Invalid JSON input'), 400

    claim = req_json['claim']
    useWithoutExtension = claim['useWithoutExtension']

    envelope_args = {
        'signer_client_id': 1000,
        'ds_return_url': req_json['callback-url'],
    }

    try:
        # Create envelope
        if useWithoutExtension == True:
            envelope = DsDocument.create_claim_without_extension('submit-claim.html', claim, envelope_args)
        else:
            extensions = json.loads(session.get('extensions'))
            envelope = DsDocument.create_claim('submit-claim.html', claim, envelope_args, extensions)
        # Submit envelope to the Docusign
        envelope_id = Envelope.send(envelope, session)
    except ApiException as exc:
        return process_error(exc)

    SessionData.set_ds_documents(envelope_id)

    try:
        # Get the recipient view
        result = Envelope.get_view(envelope_id, envelope_args, claim, session)
    except ApiException as exc:
        return process_error(exc)
    return jsonify({'envelope_id': envelope_id, 'redirect_url': result.url})


@requests.route('/requests/newinsurance', methods=['POST'])
@cross_origin()
@check_token
def buy_new_insurance():
    """Request for the purchase of a new insurance"""
    try:
        req_json = request.get_json(force=True)
    except TypeError:
        return jsonify(message='Invalid JSON input'), 400

    insurance_info = req_json['insurance']
    useWithoutExtension = req_json['useWithoutExtension']
    user = req_json['user']

    print("useWithoutExtension:", useWithoutExtension)

    envelope_args = {
        'signer_client_id': 1000,
        'ds_return_url': req_json['callback-url'],
        'gateway_account_id': os.environ.get('DS_PAYMENT_GATEWAY_ID'),
        'gateway_name': os.environ.get('DS_PAYMENT_GATEWAY_NAME'),
        'payment_display_name': os.environ.get('DS_PAYMENT_GATEWAY_DISPLAY_NAME'),

    }

    try:
        # Create envelope with payment
        if useWithoutExtension == True:
            envelope = DsDocument.create_with_payment_without_extension(
            'new-insurance.html', user, insurance_info, envelope_args
        )
        else:
            extensions = json.loads(session.get('extensions'))
            envelope = DsDocument.create_with_payment(
                'new-insurance.html', user, insurance_info, envelope_args, extensions
            )
        # Submit envelope to the Docusign
        envelope_id = Envelope.send(envelope, session)
    except ApiException as exc:
        return process_error(exc)

    SessionData.set_ds_documents(envelope_id)

    try:
        # Get the recipient view
        result = Envelope.get_view(envelope_id, envelope_args, user, session)
    except ApiException as exc:
        return process_error(exc)
    return jsonify({'envelope_id': envelope_id, 'redirect_url': result.url})


@requests.route('/requests', methods=['GET'])
@cross_origin()
def envelope_list():
    """Request for envelope list"""
    try:
        envelope_args = {
            'from_date': request.args.get('from-date')
        }
    except TypeError:
        return jsonify(message='Invalid JSON input'), 400

    user_documents = session.get('ds_documents', [])

    try:
        envelopes = Envelope.list(envelope_args, user_documents, session)
    except ApiException as exc:
        return process_error(exc)
    return jsonify({'envelopes': envelopes})


@requests.route('/requests/download', methods=['GET'])
@cross_origin()
@check_token
def envelope_download():
    """Request for document download from the envelope"""
    try:
        envelope_args = {
            'envelope_id': request.args['envelope-id'],
            "document_id": request.args['document-id'],
        }
    except TypeError:
        return jsonify(message="Invalid JSON input"), 400

    try:
        envelope_file = Envelope.download(envelope_args, session)
    except ApiException as exc:
        return process_error(exc)
    return envelope_file

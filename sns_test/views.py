import logging
import json
import re
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


@csrf_exempt
def receive_bloomberg_sns_message(request):
    print(f'request.header: \n {request.headers}')

    if request.method == 'POST':
        message_type = request.headers['X-Amz-Sns-Message-Type']
        response_json = json.loads(request.body)
        print(f'response_json: \n {response_json}')
        verify_sns(body_data=response_json)

        # Subscription confirmation
        if message_type == 'SubscriptionConfirmation':
            subscribe_url = response_json["SubscribeURL"]

            requests.get(subscribe_url)

            return HttpResponse(f"Subscription confirmed. Subscription confirmation request.body: \n{request.body}")

        # Notification messages
        elif message_type == "Notification":
            # Note: This second load is needed to parse the nested dict.
            #       First load parses the nested dict as a string (eg: '{}', instead of {''})
            response_json = json.loads(response_json['Message'])

            file_key = response_json['generated']['data']['key']
            file_key = format_file_key(file_key)

            print(f'\nfile_key: {file_key}')

            # TODO: call store_to_model here
            return HttpResponse(f"notification response_json: \n{response_json}")

    return HttpResponse("normal get request")


def verify_sns(body_data):
    """
    Documentation:
        Aws sns verification: https://docs.aws.amazon.com/sns/latest/dg/SendMessageToHttp.prepare.html
        Cryptography: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
    """

    import base64
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.exceptions import InvalidSignature

    from urllib.parse import urlparse

    # body_data['MessageId'] = '123'

    # Get the X509 certificate that Amazon SNS used to sign the message.
    sign_url = body_data['SigningCertURL']
    parsed_url = urlparse(sign_url)

    if parsed_url.scheme != 'https' or not parsed_url.hostname.endswith('.amazonaws.com'):
        logger.warning(
            f"Bloomberg sns: Invalid SigningCertUrl: {sign_url}. url should be from amazonaws.com and be in https")
        raise ValueError

    certificate = requests.get(sign_url).text.encode('utf-8')

    # Extract the public key from the certificate.
    public_key = x509.load_pem_x509_certificate(
        certificate, default_backend()).public_key()

    # Create the string to sign.
    if body_data['Type'] == 'Notification':
        fields = 'Message', 'MessageId', 'Timestamp', 'TopicArn', 'Type'
    else:
        fields = 'Message', 'MessageId', 'SubscribeURL', 'Timestamp', 'Token', 'TopicArn', 'Type'

    canonical_msg = ''.join(f'{f}\n{body_data[f]}\n' for f in fields).encode()

    # Decode the Signature value from Base64 format.
    decoded_signature = base64.b64decode(body_data['Signature'])

    # Verify the signature with the public key and the canonical message
    try:
        if body_data['SignatureVersion'] == '1':
            public_key.verify(
                decoded_signature,
                canonical_msg,
                padding.PKCS1v15(),
                hashes.SHA1()
            )

        elif body_data['SignatureVersion'] == '2':
            public_key.verify(
                decoded_signature,
                canonical_msg,
                padding.PKCS1v15(),
                hashes.SHA256()
            )

    except InvalidSignature:
        logger.warning(
            "Bloomberg sns: Invalid signature received. Need to check the validity of sender and message")
        raise ValueError

    return True


def format_file_key(file_name):
    # The response file_key we receive is "O2fUWpR2/catalogs/50544/content/responses/uc76v28sUnC7-20240613.json"
    # But we need to parse file_key to uc76v28sUnC7-20240613.json for our get_json_response()
    match = re.search(r'content\/responses\/(.+)$', file_name)
    return match.group(1)

import json
import re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from explorers.bloomberg.bdl.bdl_api_client import BDLClient


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def receive_bloomberg_sns_message(request):
    # Documentation: https://docs.aws.amazon.com/sns/latest/dg/SendMessageToHttp.prepare.html
    print(f"Request.header: \n{request.headers}\n")
    print(f"Request.body: \n{request.body}")
    
    if request.method == 'POST':
        message_type = request.headers['x-amz-sns-message-type']
        # Subscription confirmation
        if message_type == 'SubscriptionConfirmation':
           response_json = json.loads(request.body)
           subscribe_url = response_json["SubscribeURL"]

           if subscribe_url:
               request.get(subscribe_url)

           return HttpResponse(f"subscription confirmation request.body: {request.body}") 

        # Notification messages
        elif message_type == "Notification":
            response_json = json.loads(request.body)
            file_key = response_json['generated']['data']['key']
            file_key = format_file_key(file_key)

            # client = BDLClient()
            # datas = client.get_json_response(file_key)

            return HttpResponse(f"notification response_json: \n{response_json}")


    return HttpResponse("normal get request")


def format_file_key(file_name):
    # the response we receive is "O2fUWpR2/catalogs/50544/content/responses/uc76v28sUnC7-20240613.json"
    # need to parse file_key to uc76v28sUnC7-20240613.json to get_json_response

    match = re.search(r'content\/responses\/(.+)$', file_name)
    return match.group(1)


# {
#   "type": "ContentDeliveredActivity",
#   "endedAtTime": "2024-06-13T08:32:19.271585",
#   "generated": {
#     "event": "ContentDelivered",
#     "data": {
#       "key": "O2fUWpR2/catalogs/50544/content/responses/uc76v28sUnC7-20240613.json",
#       "S3AccessPointARN": null,
#       "S3MultiRegionAccessPointARN": "arn:aws:s3::695011528394:accesspoint/m6gae6b5ujtig.mrap"
#     },
#     "metadata": {
#       "DL_REQUEST_ID": "uc76v28sUnC7",
#       "DL_SNAPSHOT_TZ": "Asia/Tokyo",
#       "DL_SNAPSHOT_START_TIME": "2024-06-13T17:32:04",2
#       "DL_REQUEST_TYPE": "DataRequest"
#     }
#   }
# }

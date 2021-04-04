import urllib.request
import json
import os
import ssl


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def run_ANN():
    allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.

    data = {
        "data":
            [
                {
                    'Column3': "example_value",
                    'Column5': "0",
                    'Column6': "0",
                    'Column7': "0",
                    'Column8': "0",
                    'Column9': "0",
                    'Column10': "0",
                    'Column11': "0",
                    'Column12': "0",
                },
            ],
    }

    body = str.encode(json.dumps(data))

    url = 'http://2d752c31-8eb1-48fe-94eb-4f0e306f1c56.eastus.azurecontainer.io/score'
    api_key = 'WJp4MQLmjaDDXCG5uYLJm6tz1OdNn2E1'  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

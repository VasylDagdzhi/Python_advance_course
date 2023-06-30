import json, requests

def populateJson_for_message_id(m_id):
    return {"query": {"match_phrase": {"rspamd_meta.message_id": m_id}}}


def send_request(message_id):
    requestBody = populateJson_for_message_id(message_id)
    requestHeaders = {
        "user-agent": "my-python-app/0.0.1",
        "content-type": "application/json",
    }
    requestURL = "https://elastic.jellyfish.systems/_search?pretty"
    return requests.get(
        requestURL,
        json=requestBody,
        auth=("techops", "H16rMHKESfrAXqNtaSV0"),
        verify=False,
        headers=requestHeaders,
    ).json()


response = send_request("ww")

print(response)
import json
import requests
import urllib3
import shutil
import platform
import argparse

parser = argparse.ArgumentParser(description="Retrieve message from message_id")

parser.add_argument("message_id", type=str, help="ID of the message to be retrieved")

args = parser.parse_args()

message_id = args.message_id

terminal_size = shutil.get_terminal_size()  # os.get_terminal_size()
max_characters_length1 = 0  # int(terminal_size.columns / 1.38)
max_characters_length2 = 0  # int(terminal_size.columns / 1.29)

if platform.system() == "Darwin":
    # print("Running on Mac")
    max_characters_length1 = int(terminal_size.columns / 1.5)
    max_characters_length2 = int(terminal_size.columns / 1.5)
elif platform.system() == "Linux":
    # print("Running on Linux")
    max_characters_length1 = int(terminal_size.columns / 1.38)
    max_characters_length2 = int(terminal_size.columns / 1.29)
else:
    # print("Running on something else")
    max_characters_length1 = int(terminal_size.columns / 1.5)
    max_characters_length2 = int(terminal_size.columns / 1.5)


# RSPAMD dictionary where each key has a description
RSPAMD_INFO = {
    "SPOOF_REPLYTO": (
        "Rspamd's SPOOF_REPLYTO is a feature that checks whether an email's \"Reply-To\" header matches the sender's "
        'email address. The "Reply-To" header is an optional email header that specifies the email address that '
        "replies to the email should be sent to. In some cases, attackers may forge this header to make it appear as "
        "though the email is coming from a legitimate source, when in fact it is not."
    ),
    "R_BAD_CTE_7BIT": (
        "In Rspamd, R_BAD_CTE_7BIT is a rule that detects emails that use the 7-bit character encoding for their "
        "content, even though the content includes non-ASCII characters that cannot be represented in 7-bit encoding."
    ),
    "RSPAMD_URIBL": (
        "In Rspamd, RSPAMD_URIBL is a rule that checks whether the URLs included in an email are listed in one or more "
        "URI blacklists (URIBLs). A URI blacklist is a list of URLs or domains that have been identified as sources of"
        " spam, malware, or other types of malicious content. These blacklists are maintained by various organizations "
        "and are used by spam filters and other security systems to block access to known malicious websites."
    ),
    "R_SUSPICIOUS_URL": (
        "In Rspamd, R_SUSPICIOUS_URL is a rule that detects suspicious URLs in an email's content, including links that"
        " may be associated with phishing, malware, or other types of cyber attacks. The R_SUSPICIOUS_URL rule uses "
        "various techniques to identify URLs that may be suspicious or malicious, such as: Domain reputation: Rspamd "
        "checks the reputation of the domain associated with the URL to determine whether it has been associated with "
        "phishing, spam, or other malicious activity in the past. URL length: URLs that are abnormally long or complex"
        " may be a sign of obfuscation or an attempt to evade detection. URL structure: Rspamd analyzes the structure "
        "of the URL to identify patterns that are commonly used in phishing or malware attacks, such as URLs that "
        "include multiple subdomains or random characters. URL destination: Rspamd checks whether the destination of "
        "the URL matches the content of the email or appears to be unrelated or suspicious."
    ),
    "NCDM_SCORE_MODIFICATOR": (
        "In Rspamd, NCDM_SCORE_MODIFICATOR is a module that adjusts the score assigned to an email based on the "
        "similarity of its content to other emails that have been previously analyzed by Rspamd.The NCDM (Normalized "
        "Community Distance Metric) is a statistical algorithm used by Rspamd to calculate the similarity of two or "
        "more pieces of text. In terms of Namecheap, for our Private email pls check with L&A team if the client has "
        "any unresolved spam cases so that TO can remove the abuse flag from the client's PE domain. For shared "
        "hosting the cpanel user who sent the email is listed in spammers list in /etc/seusers file on the server. "
        "Pls check with L&A team if the client has any unresolved spam cases so that TO can remove him from that list."
    ),
    "SUBJECT_ENDS_SPACES": (
        "In Rspamd, SUBJECT_ENDS_SPACES is a rule that detects emails where the subject line ends with one or more "
        "whitespace characters, such as spaces or tabs. The subject line is an important part of an email message, as"
        " it often provides the recipient with a summary of the message's content and purpose. However, some spammers "
        "and malicious actors may attempt to manipulate the subject line to evade detection or trick the recipient into"
        " opening the email. One such technique is to add whitespace characters at the end of the subject line, which"
        " can cause the line to wrap incorrectly in some email clients or make it more difficult to search and analyze."
        " By detecting and flagging emails with subjects that end in spaces, Rspamd's SUBJECT_ENDS_SPACES rule helps to"
        " identify and block these types of emails and improve the accuracy of its spam detection."
    ),
    "FORGED_SENDER": (
        "In Rspamd, FORGED_SENDER is a rule that detects emails where the sender's address has been "
        'forged or falsified. The sender\'s address, also known as the "From" address, is an important part of an '
        "email message as it identifies the sender and allows the recipient to reply or contact them. However, spammers"
        " and malicious actors may attempt to forge the sender's address to evade detection, deceive the recipient, or "
        "impersonate a trusted sender. By detecting and flagging emails with forged sender addresses, Rspamd's "
        "FORGED_SENDER rule helps to identify and block these types of emails and improve the accuracy of its spam "
        "detection. The rule works by comparing the sender's address listed in the email's header to the domain name "
        "used in the email's envelope sender address (also known as the Return-Path address) and checking if they "
        "match."
    ),
    "LOCAL_FUZZY_DENIED": (
        "In Rspamd, LOCAL_FUZZY_DENIED is a rule that detects emails where the content has been identified as a known "
        "spam message using local fuzzy hashes. Fuzzy hashing is a technique used to identify similar or identical "
        "content by generating a unique hash value for each piece of data. In Rspamd, the local fuzzy hashes are "
        "generated by analyzing known spam messages and identifying common patterns or signatures. When an email "
        "message is received, Rspamd generates a fuzzy hash for the message content and compares it to the local "
        "database of known spam messages. If a match is found, the email is flagged as spam and the LOCAL_FUZZY_DENIED "
        "rule is triggered. In such cases the email contents must be analyzed to make sure it is legit before "
        "contacting TO to remove the bad hash indicated in the script output according to the procedure: "
        "https://collab.namecheap.net/display/DVLS/Search+and+Delete+fuzzy+hashes"
    ),
    "PHISHING": (
        "A domain substitution detected in the email body. Usually, this is used in phishing scams to trick people "
        "by making it look like they opening a URL leading to a trusted resource. Example: "
        "url: google.com leading in the html href code to: https://fake.google.com The client has the same thing "
        "in his mail and he needs to correct the link to be for the same domain it is leading at or remove it"
    ),
    "MIME_MA_MISSING_TEXT": (
        "In Rspamd, MIME_MA_MISSING_TEXT is a rule that detects emails with missing or empty text "
        "parts in their MIME (Multipurpose Internet Mail Extensions) structure. MIME is a standard used for formatting"
        " email messages that include multimedia content, such as images, videos, and attachments. MIME allows "
        "different types of content to be included in the same email message by dividing the content into separate "
        'parts or "body parts". The MIME_MA_MISSING_TEXT rule in Rspamd detects emails that have at least one MIME '
        'part that is marked as "text" but is missing its content or has an empty body. Such emails may be a sign of '
        "spam or other malicious activity, as they may attempt to evade detection by including empty text parts or "
        "other irregularities in their MIME structure."
    ),
    "URI_COUNT_ODD": (
        "In Rspamd, URI_COUNT_ODD is a rule that detects emails with an odd number of URIs in the body of the email. "
        'This test is applied specifically to "multipart/alternative" type emails (ie emails that contain both a '
        "plain text part and an html part). Since both the text part and the html part should have the same URIs in "
        "them, the total number of URIs in the message should be an even number. If there is an odd number or URIs in "
        "a multipart message, then the text part and HTML part don't match, which is somewhat suspicious."
    ),
    "HTTP_TO_HTTPS": (
        "Protocol mismatch in the contents of the email for the domain in href parameter of the url and its text part:"
        ' <a href="http://minnesota-ice.com" style="color:blue" target="_blank">https://minnesota-ice.com</a></span>'
        "</span><br></p>;"
    ),
    "NC_ML_SPAM_OUTGOING": (
        "Rspamd NC_ML_SPAM_OUTGOING is a spam detection engine used to identify and classify incoming emails as spam. "
        "It uses a combination of machine learning algorithms and other methods to detect spam. It is used in "
        "combination with other spam filtering solutions to provide a comprehensive spam protection system."
    ),
    "MIME_BASE64_TEXT_BOGUS": (
        "RSPAMD MIME_BASE64_TEXT_BOGUS is an RSPAMD rule that is triggered when a message contains text that has been "
        "encoded as base64, but does not appear to be valid. It is used to detect potential malicious content that has "
        "been encoded to hide its true nature."
    ),
    "FAKE_REPLY": (
        'Subject has the reply part: "Re:" while the email is sent wihtout previous correspondence and is not a reply.'
    ),
    "FROM_DN_EQ_ADDR": (
        "RSPAMD FROM_DN_EQ_ADDR is a rule for Rspamd, an open-source spam filtering system, that checks if the "
        'sender\'s domain name in an email is equal to the address provided in the "From" header. '
        "If the domains do not match, then the message is likely spam."
    ),
}

RSPAMD_ADVICE = {"RSPAMD_SYMBOL_NAME": "Advice to CS reps"}

urllib3.disable_warnings()

requestHeaders = {
    "user-agent": "my-python-app/0.0.1",
    "content-type": "application/json",
}
requestURL = "https://elastic.jellyfish.systems/_search?pretty"
# message_id = input("Enter message id to search for -->  ")


def populateJson_for_message_id(m_id):
    return {"query": {"match_phrase": {"rspamd_meta.message_id": m_id}}}


def split_string(string, length):
    # Initialize an empty list to store the substrings
    substrings = []

    # Loop over the string and slice it into substrings of length 'length'
    for i in range(0, len(string), length):
        substrings.append(string[i : i + length])

    return substrings


print(f"Search pattern: {message_id}")
requestBody = populateJson_for_message_id(message_id)
r = requests.get(
    requestURL,
    json=requestBody,
    auth=("techops", "VSI2b2RP4uoq5Oqvn6nz"),
    verify=False,
    headers=requestHeaders,
)
r = r.json()
# print(r)

if (
    json.loads(json.dumps(r, sort_keys=True, indent=2, ensure_ascii=False))["hits"][
        "total"
    ]["value"]
    == 0
):
    print(f"Unfortunately, nothing was found by the input search pattern.")
    exit(0)

output = ""
for item in json.loads(json.dumps(r, sort_keys=True, indent=2, ensure_ascii=False))[
    "hits"
]["hits"]:
    for data_item in item:
        output = item["_source"]

if output["rspamd_meta"]["score"] < 8:
    print(f"{'Total spam score:':36}\t {str(output['rspamd_meta']['score'])}")
else:
    print(f"{'Total spam score:':36}\t{str(output['rspamd_meta']['score'])}")
if output["rspamd_meta"]["action"] == "reject" or "milter-reject":
    print(
        f"{'Action taken by the rspamd filter:':36}\t{str(output['rspamd_meta']['action'])}"
    )
print(f"{'Sender:':36}\t{output['rspamd_meta']['header_from'][0]}")
recipients = output["rspamd_meta"]["header_to"][0].split(sep=",")
print(f"Recipients:")
for recipient in recipients:
    print(f"\t{recipient.lstrip()}")
print(f"Total recipients: {len(recipients)}")


print(f"{'Subject of the email:':36}\t\"{output['rspamd_meta']['header_subject'][0]}\"")
print(f"{'Date and time it was sent:':36}\t{output['rspamd_meta']['header_date'][0]}")


print("")
header = f"| {'Rspamd symbol name':40} | {'Score':8} | {'Options':{max_characters_length1}} |"
print("-" * len(header))
print(header)
print("-" * len(header))
for symbol in output["rspamd_meta"]["symbols"]:
    # print(f"{symbol}")
    if symbol["score"] > 0:
        if symbol["name"] == "PHISHING":
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| { str(symbol['options'][0].replace('->', ' -> ')):{max_characters_length1}} |"
            )
        elif symbol["name"] == "SPOOF_REPLYTO":
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(symbol['options'][0] + ' -> ' + symbol['options'][1]):{max_characters_length1}} |"
            )
        elif symbol["name"] == "R_BAD_CTE_7BIT":
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(symbol['options']):{max_characters_length1}} |"
            )
        elif symbol["name"] == "RSPAMD_URIBL":
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(symbol['options'][0]):{max_characters_length1}} |"
            )
        elif symbol["name"] == "R_SUSPICIOUS_URL":
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(symbol['options'][0]):{max_characters_length1}} |"
            )
        elif symbol["name"] == "NCDM_SCORE_MODIFICATOR":
            print(
                +f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(symbol['options'][0]):{max_characters_length1}} |"
            )
        elif symbol["name"] == "NC_ML_SPAM_OUTGOING":
            print(
                +f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(symbol['options'][0]):{max_characters_length1}} |"
            )
        elif symbol["name"] == "SUBJECT_ENDS_SPACES":
            subject = f"\"{str(output['rspamd_meta']['header_subject'][0])}\""
            print(
                +f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {subject:{max_characters_length1}} |"
            )
        elif symbol["name"] == "MIME_BASE64_TEXT_BOGUS":
            subject = f"\"{str(output['rspamd_meta']['header_subject'][0])}\""
            print(+f"| {str(symbol['name']):40} | {str(symbol['score']):8} ")
        elif symbol["name"] == "FAKE_REPLY":
            subject = f"\"{str(output['rspamd_meta']['header_subject'][0])}\""
            print(
                +f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {subject:{max_characters_length1}} |"
            )
        elif symbol["name"] == "FROM_DN_EQ_ADDR":
            subject = f"\"{str(output['rspamd_meta']['header_subject'][0])}\""
            print(f"| {str(symbol['name']):40} | {str(symbol['score']):8} ")
        elif symbol["name"] == "FORGED_SENDER":
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(symbol['options'][0] + ' -> ' + symbol['options'][1]):{max_characters_length1}} |"
            )
        elif symbol["name"] == "LOCAL_FUZZY_DENIED":
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} "
                f"| {str(output['rspamd_meta']['fuzzy_hashes']):{max_characters_length1}} |"
            )
        else:
            print(
                f"| {str(symbol['name']):40} | {str(symbol['score']):8} | {'':{max_characters_length1}} |"
            )
print("-" * len(header))
print(f"\nDetailed description of triggered RSPAMD symbols:")

header = f"| {'Rspamd symbol name':40} | {'Description':{max_characters_length2}} |"
print("-" * len(header))
print(header)
print("-" * len(header))
for symbol in output["rspamd_meta"]["symbols"]:
    if symbol["score"] > 0:
        if symbol["name"] in RSPAMD_INFO.keys():
            if len(RSPAMD_INFO[symbol["name"]]) > max_characters_length2:
                desc = split_string(RSPAMD_INFO[symbol["name"]], max_characters_length2)
                desc_pos = 0
                for line in desc:
                    if desc_pos == 0:
                        print(
                            f"| {str(symbol['name']):40} | {line:{max_characters_length2}} |"
                        )
                    else:
                        print(f"| {' ':40} | {line:{max_characters_length2}} |")
                    desc_pos += 1
            else:
                print(f"| {str(symbol['name']):40} | {RSPAMD_INFO[symbol['name']]} |")
            print("-" * len(header))

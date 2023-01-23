import os
import requests
import json

# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print("Current rules:", json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print("DELETE Rules:", json.dumps(response.json()))


def set_rules(rules):
    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(show_created_at: bool, show_author_info: bool):
    def gen_query(is_more, param) -> str:
        if not is_more:
            return f'?{param}'
        else:
            return f'&{param}'

    baseurl = "https://api.twitter.com/2/tweets/search/stream"
    is_condition = False
    if show_created_at:
        baseurl += gen_query(is_condition, "tweet.fields=created_at")
        is_condition = True
    if show_author_info:
        baseurl += gen_query(is_condition, "expansions=author_id")
        is_condition = True

    response = requests.get(baseurl, auth=bearer_oauth, stream=True)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
            print(f'https://twitter.com/{json_response["includes"]["users"][0]["username"]}/status/{json_response["data"]["id"]}')
            print("="*20)

# https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule#list
def subscribe_targets(lists: list[str], hashtags: list[str] = [], rule_name: str = "subscribe influencers") -> list[dict[str, str]]:
    targets = ""
    for handle in lists:
        targets += f"from:{handle} OR "
    for tag in hashtags:
        targets += f"#{tag} OR "
    final_rule = [
        {"value": f"({targets[:len(targets)-4]}) -is:retweet -is:reply -is:nullcast", "tag": rule_name},
    ]

    return final_rule

def initialize():
    rules = get_rules()
    delete_all_rules(rules)


if __name__ == "__main__":
    initialize()
    followers = subscribe_targets(["elonmusk"])
    set_rules(followers)
    get_stream(True, True)
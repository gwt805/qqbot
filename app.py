import json
import requests
import nacl.signing
import nacl.encoding
from loguru import logger
from flask import Flask, request,jsonify

app = Flask(__name__)

APP_ID = "" # your appID
BOT_SECRET = "" # your secret

@app.route('/qqbot', methods=['POST'])
def qqbot():
    data = request.get_json()
#     logger.info(data)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    if data.get("op") == 13:  # 回调地址验证事件
        validation_payload = data.get("d", {})
        plain_token = validation_payload.get("plain_token")
        event_ts = validation_payload.get("event_ts")

        if not plain_token or not event_ts:
            return jsonify({"error": "Missing required fields"}), 400

        signature = generate_ed25519_signature(plain_token, event_ts, BOT_SECRET) # 计算签名
        return jsonify({"plain_token": plain_token, "signature": signature})
    else:
        event_type = data.get("t")
        message = data.get("d", {})
        if event_type == "C2C_MESSAGE_CREATE":  # 单聊消息
            openid = message["author"]["id"]
            content = message["content"].strip()
            msg_id = message["id"]
#             logger.info(f"Received private message from {openid}: {content}")

            # 回复单聊消息
            reply_message = f"你好，{openid}！收到你的消息：{content}"
            if send_private_message(openid, reply_message, msg_id):
                return jsonify({"status": "Message sent successfully"})
            else:
                return jsonify({"error": "Failed to send message"}), 500

        elif event_type == "GROUP_AT_MESSAGE_CREATE":  # 群聊消息
            group_openid = message["group_openid"]
            content = message["content"].strip()
            msg_id = message["id"]
#             logger.info(f"Received group message from {group_openid}: {content}")

            # 回复群聊消息
            reply_message = f"你好，群聊中有人 @ 了我！收到的消息是：{content}"
            if send_group_message(group_openid, reply_message, msg_id):
                return jsonify({"status": "Message sent successfully"})
            else:
                return jsonify({"error": "Failed to send message"}), 500

    return jsonify({"error": "Unknown event"}), 400

def generate_ed25519_signature(plain_token, event_ts, secret):
    sign_str = f"{event_ts}{plain_token}".encode() # 拼接待签名的字符串
    signing_key = nacl.signing.SigningKey(secret.encode()) # 生成私钥
    signed_message = signing_key.sign(sign_str)
    signature = signed_message.signature.hex() # 生成签名
    return signature

def get_access_token():
    url = "https://qqbot-token.weilong.workers.dev/app/getAppAccessToken"
    headers = {"Content-Type": "application/json"}
    data = {"appId": APP_ID, "clientSecret": BOT_SECRET}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
#         logger.info(response.json().get("access_token"))
        return response.json().get("access_token")
    else:
#         logger.info(f"Failed to get access_token: {response.text}")
        return None

def send_private_message(openid, content, msg_id=None): # 单聊
    access_token = get_access_token()
    if not access_token: return False
    url = f"https://qqbot-msg.weilong.workers.dev/v2/users/{openid}/messages"
    headers = {"Authorization": f"QQBot {access_token}", "Content-Type": "application/json"}
    data = {
        "msg_type": 0,  # 文本消息
        "content": content
    }
    if msg_id:
        data["msg_id"] = msg_id

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
#         logger.info("Private message sent successfully")
        return True
    else:
#         logger.info(f"Failed to send private message: {response.text}")
        return False

def send_group_message(group_openid, content, msg_id=None): # 群聊
    access_token = get_access_token()
    if not access_token: return False
    url = f"https://qqbot-msg.weilong.workers.dev/v2/groups/{group_openid}/messages"
    headers = {"Authorization": f"QQBot {access_token}", "Content-Type": "application/json"}
    data = {
        "msg_type": 0,  # 文本消息
        "content": content
    }
    if msg_id:
        data["msg_id"] = msg_id

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
#         logger.info("Group message sent successfully")
        return True
    else:
#         logger.info(f"Failed to send group message: {response.text}")
        return False

# 仅在本地运行时打开，pythonanywhere 上不需要这两行
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)

'''消息类型
文本:0 | markdown:2 | ark:3 | embed:4 | media:7 富媒体
'''
import requests
import nacl.signing
import nacl.encoding
from flask import Flask, request,jsonify

app = Flask(__name__)

APP_ID = "" # your appID
BOT_SECRET = "" # your secret

@app.route('/qqbot', methods=['POST'])
def qqbot():
    data = request.get_json()

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
            return process_message('private', openid, content, msg_id)
        elif event_type == "GROUP_AT_MESSAGE_CREATE":  # 群聊消息
            group_openid = message["group_openid"]
            content = message["content"].strip()
            msg_id = message["id"]
            return process_message('group', group_openid, content, msg_id)
        else:
            return jsonify({"error": "Unknown event"})

def generate_ed25519_signature(plain_token, event_ts, secret):
    sign_str = f"{event_ts}{plain_token}".encode() # 拼接待签名的字符串
    signing_key = nacl.signing.SigningKey(secret.encode()) # 生成私钥
    signed_message = signing_key.sign(sign_str)
    signature = signed_message.signature.hex() # 生成签名
    return signature

def get_access_token():
    # url = "https://qqbot-token.weilong.workers.dev/app/getAppAccessToken" # pythonanywhere + cloudflare
    url = "https://bots.qq.com/app/getAppAccessToken"
    headers = {"Content-Type": "application/json"}
    data = {"appId": APP_ID, "clientSecret": BOT_SECRET}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200: return response.json().get("access_token")
    else: return None

def send_private_message(openid, msg_type, content_type, content, msg_id=None): # 单聊
    access_token = get_access_token()
    if not access_token: return False
    # url = f"https://qqbot-msg.weilong.workers.dev/v2/users/{openid}/messages" # pythonanywhere + cloudflare
    url = f"https://sandbox.api.sgroup.qq.com/v2/users/{openid}/messages" # 正式环境去掉 sandbox
    headers = {"Authorization": f"QQBot {access_token}", "Content-Type": "application/json"}
    data = {"msg_type": msg_type, f"{content}": content}
    if msg_id: data["msg_id"] = msg_id

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200: return jsonify({"status": "Message sent successfully"})
    else: return jsonify({"error": "Failed to send message"})

def send_group_message(group_openid, msg_type, content_type, content, msg_id=None): # 群聊
    access_token = get_access_token()
    if not access_token: return False
    # url = f"https://qqbot-msg.weilong.workers.dev/v2/groups/{group_openid}/messages" # pythonanywhere + cloudflare
    url = f"https://sandbox.api.sgroup.qq.com/v2/groups/{group_openid}/messages" # 正式环境去掉 sandbox
    headers = {"Authorization": f"QQBot {access_token}", "Content-Type": "application/json"}
    data = {"msg_type": msg_type, f"{content}": content}
    if msg_id: data["msg_id"] = msg_id

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200: return jsonify({"status": "Message sent successfully"})
    else: return jsonify({"error": "Failed to send message"})

def process_message(msg_type, openid, content, msg_id):
    if content == "" or content == '/help':
        mk = '''
            # 我是机器人 AIRbot

            ## 使用方法
            - /指令 + 空格 + 问题 ; > 例如：/天气 上海
            - /help 查看帮助,这里不需要加空格

            ## 指令列表
            1. /AI
            2. /天气
            3. /help
            4. 待续功能...

            ## 如需添加其他功能，请联系群主
        '''
        if msg_type == 'group': return send_group_message(openid, 2, 'markdown', {'content': mk}, msg_id)
        if msg_type == 'private': return send_private_message(openid, 2,'markdown', {'content': mk}, msg_id)

    if content.startswith("/天气"):
        if (content.split("/天气 ")) == 1:
            if msg_type == 'group': return send_group_message(openid, 0, 'content', '请输入城市名', msg_id)
            if msg_type == 'private': return send_private_message(openid, 0, 'content', '请输入城市名', msg_id)
        else:
            city = content.split("/天气 ")[1]
            if city == '':
                if msg_type == 'group': return send_group_message(openid, 0, 'content', '请输入城市名', msg_id)
                if msg_type == 'private': return send_private_message(openid, 0, 'content', '请输入城市名', msg_id)
            else:
                try:
                    res = requests.get(f"https://v.api.aa1.cn/api/api-weather/qq-weather.php?msg={city}").text
                    if msg_type == 'group': return send_group_message(openid, 0, 'content', res, msg_id)
                    if msg_type == 'private': return send_private_message(openid, 0, 'content', res, msg_id)
                except:
                    if msg_type == 'group': return send_group_message(openid, 0, 'content', "天气获取失败", msg_id)
                    if msg_type == 'private': return send_private_message(openid, 0, 'content', "天气获取失败", msg_id)

    if content.startswith("/AI"):
        if (content.split("/AI ")) == 1:
            if msg_type == 'group': return send_group_message(openid, 0, 'content', '请输入问题', msg_id)
            if msg_type == 'private': send_private_message(openid, 0, 'content', '请输入问题', msg_id)
        else:
            question = content.split("/AI ")[1]
            if question == '':
                if msg_type == 'group': return send_group_message(openid, 0, 'content', '请输入问题', msg_id)
                if msg_type == 'private': return send_private_message(openid, 0, 'content', '请输入问题', msg_id)
            else:
                try:
                    res = requests.post(f"https://tools.mgtv100.com/external/v1/pear/deepseek", {'content': question}).json()
                    if msg_type == 'group': return send_group_message(openid, 2, 'markdown', {'content': res['data']['message']}, msg_id)
                    if msg_type == 'private': return send_private_message(openid, 2, 'markdown', {'content': res['data']['message']}, msg_id)
                except:
                    if msg_type == 'group': return send_group_message(openid, 0, 'content', "结果获取失败", msg_id)
                    if msg_type == 'private': return send_private_message(openid, 0, 'content', "结果获取失败", msg_id)
                
# 仅在本地运行时打开，pythonanywhere 上不需要这两行
# if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080)
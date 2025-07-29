from flask import Flask, request, abort
import json
import hashlib
import hmac
import base64
from flask import Flask, request, abort
import json
import hashlib
import hmac
import base64

app = Flask(__name__)

CHANNEL_SECRET = 'fe34da3598d63042fba214cb261da1cb'

@app.route('/callback', methods=['POST'])
def callback():
    body = request.get_data()  # bytes
    signature = request.headers.get('X-Line-Signature', '')

    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'), body, hashlib.sha256).digest()
    computed_signature = base64.b64encode(hash).decode()

    if not hmac.compare_digest(signature, computed_signature):
        print('❌ 署名不一致')
        abort(400)

    try:
        print('✅ 署名OK & JSON表示')
        print(json.dumps(json.loads(body.decode('utf-8')), indent=2))
    except json.JSONDecodeError:
        print('⚠️ JSONデコード失敗：', body)

    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
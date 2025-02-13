from flask import Flask, request, jsonify

app = Flask(__name__)

import requests
import json


def deepseek_completions(input):
    url = "https://api.deepseek.com/chat/completions"

    payload = json.dumps({
        "messages": [
            {
                "content": "You are a helpful assistant",
                "role": "system"
            },
            {
                "content": input,
                "role": "user"
            }
        ],
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer <TOKEN>'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if 'input' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'input' parameter"
            }), 400
            
        user_input = data['input']
        result = deepseek_completions(user_input)

        response = {
            "status": "success",
            "message": "处理成功",
            "data": result
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

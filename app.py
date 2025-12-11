import re
import json
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
OLLAMA_MODEL = "llama3"   # 你的模型名稱


# -------------------------------------------------------
# 最安全 JSON Parser（最新版）
# -------------------------------------------------------
def safe_parse_json(raw: str):
    import json, re

    text = raw.strip()

    # 1. 嘗試解析（若模型剛好輸出完整 JSON）
    try:
        return json.loads(text)
    except:
        pass

    # 2. 移除 markdown 包裝
    text = re.sub(r"^```[a-zA-Z0-9]*\s*", "", text)
    text = re.sub(r"```$", "", text).strip()

    # 3. 取出 JSON 主體
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise json.JSONDecodeError("No JSON object found.", raw, 0)

    json_text = text[start:end + 1]

    # 4. 再試一次解析（也許剛好成功）
    try:
        return json.loads(json_text)
    except:
        pass

    # 5. 修復常見格式錯誤
    json_text = re.sub(r'"([^"]+)"\s+(kcal|g)', r'"\1 \2"', json_text)
    json_text = re.sub(r'(?<!")(\d+(\.\d+)?\s*-\s*\d+(\.\d+)?)\s*(kcal|g)', r'"\1 \5"', json_text)
    json_text = re.sub(r'(?<!")(\d+(\.\d+)?)\s*(kcal|g)', r'"\1 \3"', json_text)
    json_text = re.sub(r'"(\d+(\.\d+)?)(g|kcal)"', r'"\1 \3"', json_text)
    json_text = re.sub(r",\s*}", "}", json_text)

    return json.loads(json_text)


# -------------------------------------------------------
# LLM 查詢（最新版）
# -------------------------------------------------------
def query_llm(food, amount):
    prompt = f"""
You are a professional nutritionist.

User ate: {food}
Amount: {amount}

Return ONLY valid JSON with this structure:
{{
  "calories": "<range> kcal",
  "protein": "<range> g",
  "fat": "<range> g",
  "carbs": "<range> g",
  "suggestion": "<short suggestion>"
}}

Rules:
- No text before or after the JSON.
- Units must be inside the string.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=20
    )

    raw = response.json().get("response", "")
    return safe_parse_json(raw)


# -------------------------------------------------------
# Routes
# -------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    food = request.form.get("food")
    amount = request.form.get("amount")

    if not food or not amount:
        return jsonify({"error": "Missing input"}), 400

    ai_data = query_llm(food, amount)
    return jsonify(ai_data)


# -------------------------------------------------------
# 啟動伺服器
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)

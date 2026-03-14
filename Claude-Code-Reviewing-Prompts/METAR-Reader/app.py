"""
app.py — METAR Reader Flask Application
METAR 天气阅读器 Flask 应用

Fetches raw METAR data from aviationweather.gov and returns a
human-readable weather summary.
从 aviationweather.gov 获取原始 METAR 数据，并返回人类可读的天气摘要。
"""

import requests
from flask import Flask, jsonify, render_template, request

from metar_decoder import METARDecoder

app = Flask(__name__)

# Aviation Weather Center API endpoint / 航空气象中心 API 端点
AWC_BASE_URL = "https://aviationweather.gov/api/data/metar"


def fetch_metar(station_id: str) -> str | None:
    """
    Fetch the latest METAR string for a given station ID.
    获取指定机场的最新 METAR 字符串。

    Returns the raw METAR text, or None if the request fails.
    返回原始 METAR 文本，失败时返回 None。
    """
    params = {"ids": station_id.upper(), "format": "raw"}
    resp = requests.get(AWC_BASE_URL, params=params, timeout=10)
    resp.raise_for_status()
    text = resp.text.strip()
    return text if text else None


@app.route("/")
def index():
    """Serve the main page. / 提供主页。"""
    return render_template("index.html")


@app.route("/api/metar")
def get_metar():
    """
    GET /api/metar?station=KHIO
    Fetch and decode a METAR report for the requested station.
    获取并解码请求机场的 METAR 报告。
    """
    station = request.args.get("station", "").strip().upper()

    # Validate input / 验证输入
    if not station:
        return jsonify({"error": "Please provide a station ID (e.g. KHIO)."}), 400
    if len(station) < 3 or len(station) > 4 or not station.isalpha():
        return jsonify({"error": f"'{station}' is not a valid ICAO station code. Use 3–4 letters (e.g. KHIO, KSEA, EGLL)."}), 400

    # Fetch raw METAR / 获取原始 METAR
    try:
        raw = fetch_metar(station)
    except requests.exceptions.Timeout:
        return jsonify({"error": "The weather service timed out. Please try again."}), 504
    except requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Could not reach the weather service: {exc}"}), 502

    if not raw:
        return jsonify({"error": f"No METAR data found for station '{station}'. Check the airport code and try again."}), 404

    # Decode and return / 解码并返回
    decoder = METARDecoder(raw)
    return jsonify({"raw": raw, "decoded": decoder.result})


if __name__ == "__main__":
    # Debug mode enabled for development / 开发模式下启用调试
    app.run(debug=True, port=5000)

"""
test_routes.py — Flask route tests for app.py
app.py 的 Flask 路由测试

fetch_metar() is patched with unittest.mock so no real network calls are made.
使用 unittest.mock 替换 fetch_metar()，不会发出真实网络请求。
"""

import json
from unittest.mock import patch, MagicMock
import pytest
import requests


# ─────────────────────────────────────────────
# Index route / 主页路由
# ─────────────────────────────────────────────

class TestIndexRoute:
    def test_index_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_index_contains_html(self, client):
        resp = client.get("/")
        assert b"METAR" in resp.data


# ─────────────────────────────────────────────
# /api/metar — input validation / 输入校验
# ─────────────────────────────────────────────

class TestMetarApiValidation:
    def test_missing_station_returns_400(self, client):
        resp = client.get("/api/metar")
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert "error" in data

    def test_empty_station_returns_400(self, client):
        resp = client.get("/api/metar?station=")
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert "error" in data

    def test_numeric_station_returns_400(self, client):
        resp = client.get("/api/metar?station=1234")
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert "error" in data

    def test_too_short_station_returns_400(self, client):
        # 2-letter codes are invalid (minimum 3)
        resp = client.get("/api/metar?station=KS")
        assert resp.status_code == 400

    def test_too_long_station_returns_400(self, client):
        # 5-letter codes are invalid
        resp = client.get("/api/metar?station=KSEAX")
        assert resp.status_code == 400

    def test_station_with_digits_returns_400(self, client):
        resp = client.get("/api/metar?station=K1EA")
        assert resp.status_code == 400


# ─────────────────────────────────────────────
# /api/metar — successful responses / 成功响应
# ─────────────────────────────────────────────

MOCK_KSEA_RAW = "KSEA 141753Z 27012KT 10SM FEW035 12/04 A2992 RMK AO2"
MOCK_EGLL_RAW = "EGLL 141820Z VRB03KT 0800 FG OVC002 04/04 Q1008 NOSIG"
MOCK_ZBAA_RAW = "ZBAA 141830Z 36005KT 0800 +SN OVC005 M05/M10 Q1023"


class TestMetarApiSuccess:
    def test_success_returns_200(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        assert resp.status_code == 200

    def test_response_has_raw_field(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        data = json.loads(resp.data)
        assert "raw" in data
        assert data["raw"] == MOCK_KSEA_RAW

    def test_response_has_decoded_field(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        data = json.loads(resp.data)
        assert "decoded" in data

    def test_decoded_contains_station(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        decoded = json.loads(resp.data)["decoded"]
        assert decoded["station"]["raw"] == "KSEA"

    def test_decoded_contains_wind(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        decoded = json.loads(resp.data)["decoded"]
        assert "wind" in decoded
        assert decoded["wind"]["cardinal"] == "West"

    def test_decoded_contains_temperature(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        decoded = json.loads(resp.data)["decoded"]
        assert decoded["temp_dewpoint"]["temp_c"] == 12

    def test_decoded_contains_summary(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        decoded = json.loads(resp.data)["decoded"]
        assert "summary" in decoded
        assert len(decoded["summary"]) > 0

    def test_decoded_contains_emoji(self, client):
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=KSEA")
        decoded = json.loads(resp.data)["decoded"]
        assert "condition_emoji" in decoded

    def test_station_uppercased_automatically(self, client):
        # lowercase input should be uppercased before lookup
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW) as mock_fetch:
            client.get("/api/metar?station=ksea")
        mock_fetch.assert_called_once_with("KSEA")

    def test_fog_metar_egll(self, client):
        with patch("app.fetch_metar", return_value=MOCK_EGLL_RAW):
            resp = client.get("/api/metar?station=EGLL")
        decoded = json.loads(resp.data)["decoded"]
        assert decoded["condition_emoji"] == "🌫️"
        assert decoded["temp_dewpoint"]["humidity_pct"] == 100

    def test_snow_metar_zbaa(self, client):
        with patch("app.fetch_metar", return_value=MOCK_ZBAA_RAW):
            resp = client.get("/api/metar?station=ZBAA")
        decoded = json.loads(resp.data)["decoded"]
        assert decoded["condition_emoji"] == "❄️"
        assert decoded["temp_dewpoint"]["temp_c"] == -5


# ─────────────────────────────────────────────
# /api/metar — error handling / 错误处理
# ─────────────────────────────────────────────

class TestMetarApiErrors:
    def test_station_not_found_returns_404(self, client):
        # fetch_metar returns None → station has no data
        with patch("app.fetch_metar", return_value=None):
            resp = client.get("/api/metar?station=ZZZZ")
        assert resp.status_code == 404
        data = json.loads(resp.data)
        assert "error" in data

    def test_timeout_returns_504(self, client):
        with patch("app.fetch_metar", side_effect=requests.exceptions.Timeout):
            resp = client.get("/api/metar?station=KSEA")
        assert resp.status_code == 504
        data = json.loads(resp.data)
        assert "error" in data

    def test_request_exception_returns_502(self, client):
        with patch("app.fetch_metar", side_effect=requests.exceptions.ConnectionError("unreachable")):
            resp = client.get("/api/metar?station=KSEA")
        assert resp.status_code == 502
        data = json.loads(resp.data)
        assert "error" in data

    def test_error_response_has_no_raw_field(self, client):
        with patch("app.fetch_metar", return_value=None):
            resp = client.get("/api/metar?station=ZZZZ")
        data = json.loads(resp.data)
        assert "raw" not in data

    def test_three_letter_station_accepted(self, client):
        # 3-letter codes like "HIO" are valid
        with patch("app.fetch_metar", return_value=MOCK_KSEA_RAW):
            resp = client.get("/api/metar?station=HIO")
        assert resp.status_code == 200

# METAR Reader

A Flask web app that fetches live METAR weather reports from [Aviation Weather Center](https://aviationweather.gov) and decodes them into plain English.

基于 Flask 的网页应用，从[航空气象中心](https://aviationweather.gov)获取实时 METAR 天气报文并解码为人类可读的描述。

---

## What is METAR? / 什么是 METAR？

METAR (Meteorological Aerodrome Report) is the standard format used worldwide to report current airport weather conditions. A raw METAR looks like this:

METAR（气象机场报告）是全球通用的机场当前天气报告标准格式。原始 METAR 如下所示：

```
KSEA 141753Z 27012KT 10SM FEW035 12/04 A2992 RMK AO2
```

This app translates that into human-readable output: wind speed and direction, temperature, humidity, visibility, sky conditions, and altimeter setting.

本应用将其翻译为人类可读的输出：风速风向、温度、湿度、能见度、天空状况和气压设置。

---

## Features / 功能特性

- Live data from the FAA Aviation Weather Center API — no API key needed / 从美国联邦航空局航空气象中心 API 获取实时数据，无需 API 密钥
- Decodes wind, visibility, sky cover, temperature/dew point, humidity, and pressure / 解码风、能见度、天空状况、温度/露点、湿度和气压
- Weather condition emoji based on sky state / 根据天空状态显示天气 emoji
- Quick-pick buttons for common airports (KSEA, KLAX, KJFK, EGLL, ZBAA, etc.) / 常用机场快速选择按钮
- Collapsible raw METAR display / 可折叠的原始 METAR 显示

---

## Project Structure / 项目结构

```
METAR-Reader/
├── app.py              # Flask application + API route / Flask 应用 + API 路由
├── metar_decoder.py    # METAR string parser and decoder / METAR 字符串解析器
├── requirements.txt    # Python dependencies / Python 依赖
├── templates/
│   └── index.html      # Main page template / 主页模板
├── static/
│   ├── css/
│   │   └── style.css   # Styles / 样式表
│   └── js/
│       └── app.js      # Frontend fetch + render logic / 前端请求与渲染逻辑
└── tests/
    ├── conftest.py     # Shared pytest fixtures / 共享 pytest fixture
    ├── test_decoder.py # Unit tests for METARDecoder / 解码器单元测试
    └── test_routes.py  # Flask route tests / Flask 路由测试
```

---

## Getting Started / 快速开始

### Prerequisites / 前置要求

- Python 3.10+
- Internet access (fetches live data from aviationweather.gov) / 网络访问（从 aviationweather.gov 获取实时数据）

### Installation / 安装

```bash
# 1. Clone the repo / 克隆仓库
git clone <your-repo-url>
cd METAR-Reader

# 2. Create and activate a virtual environment / 创建并激活虚拟环境
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies / 安装依赖
pip install -r requirements.txt
```

### Running / 运行

```bash
python app.py
```

Then open your browser to `http://localhost:5000`.

然后在浏览器中打开 `http://localhost:5000`。

---

## Usage / 使用方法

1. Enter a 3–4 letter ICAO airport code (e.g. `KSEA`, `KLAX`, `EGLL`, `ZBAA`) / 输入 3–4 位 ICAO 机场代码
2. Click **Get Weather** or press Enter / 点击 **Get Weather** 或按回车键
3. View the decoded weather report / 查看解码后的天气报告

**ICAO code format / ICAO 代码格式：**
- US airports start with `K` — e.g. `KJFK`, `KLAX`, `KORD` / 美国机场以 `K` 开头
- European airports often start with `E` or `L` — e.g. `EGLL` (London Heathrow) / 欧洲机场通常以 `E` 或 `L` 开头
- Chinese airports start with `Z` — e.g. `ZBAA` (Beijing Capital) / 中国机场以 `Z` 开头

---

## API

The backend exposes one endpoint: / 后端提供一个接口：

```
GET /api/metar?station=KSEA
```

**Success response / 成功响应：**
```json
{
  "raw": "KSEA 141753Z 27012KT 10SM FEW035 12/04 A2992 RMK AO2",
  "decoded": {
    "station": { "raw": "KSEA" },
    "time": { "display": "Day 14 of the month, 17:53 UTC" },
    "wind": { "speed_mph": 13.8, "cardinal": "West", "calm": false },
    "visibility": { "display": "More than 10 miles visibility (excellent)" },
    "sky": [{ "display": "A few clouds at 3,500 ft" }],
    "temp_dewpoint": { "temp_f": 53.6, "temp_c": 12, "humidity_pct": 57 },
    "altimeter": { "display": "29.92 inHg (1013 hPa)" },
    "summary": "Mostly clear with a few clouds. 53.6°F (12°C). winds 13.8 mph from the West.",
    "condition_emoji": "🌤"
  }
}
```

**Error response / 错误响应：**
```json
{ "error": "No METAR data found for station 'XXXX'. Check the airport code and try again." }
```

| Status / 状态码 | Cause / 原因 |
|---|---|
| `400` | Missing or invalid station code / 缺少或无效的机场代码 |
| `404` | No data found for that station / 该机场无数据 |
| `502` | Cannot reach aviationweather.gov / 无法连接气象服务 |
| `504` | Request timed out / 请求超时 |

---

## Testing / 测试

Tests are written with **pytest** and use `unittest.mock` to patch the network layer — no real HTTP requests are made.

测试使用 **pytest** 编写，并通过 `unittest.mock` 替换网络层，不会发出真实的 HTTP 请求。

### Running the tests / 运行测试

```bash
# Run all tests / 运行所有测试
pytest tests/

# Verbose output / 详细输出
pytest tests/ -v

# Run only decoder tests / 仅运行解码器测试
pytest tests/test_decoder.py -v

# Run only route tests / 仅运行路由测试
pytest tests/test_routes.py -v
```

### Test structure / 测试结构

**`tests/test_decoder.py`** — Unit tests for `METARDecoder` and helper functions (65 tests)

直接向 `METARDecoder` 传入模拟 METAR 字符串，测试所有解析字段（65 个测试）

| Test class / 测试类 | What it covers / 覆盖内容 |
|---|---|
| `TestHelpers` | Unit conversions: ℃→℉, knots→mph, degrees→cardinal / 单位换算 |
| `TestStationAndTime` | ICAO code, timestamp, AUTO flag, METAR/SPECI prefix / 机场代码、时间、自动站标志 |
| `TestWind` | Direction, speed, gusts, calm, variable (VRB), MPS unit / 风向、风速、阵风、平静风、可变风 |
| `TestVisibility` | SM, ICAO meters, two-token fractions (e.g. `1 1/4SM`) / 英里制、米制、分数能见度 |
| `TestSkyConditions` | CLR/FEW/SCT/BKN/OVC, height in feet, CB/TCU cloud type / 天空状况、云高、云型 |
| `TestTemperature` | Positive/negative (M-prefix) temps, dew point, humidity / 正负气温、露点、湿度 |
| `TestAltimeter` | A-format (inHg), Q-format (hPa), cross-unit conversion / A/Q 格式气压及单位换算 |
| `TestWeatherPhenomena` | Light/heavy rain, snow, fog, thunderstorm / 小雨、大雨、雪、雾、雷暴 |
| `TestRemarks` | RMK extraction, no bleed into other fields / 备注提取 |
| `TestSummaryAndEmoji` | Plain-English summary, all 8 condition emojis / 摘要文字、8 种天气 emoji |
| `TestEdgeCases` | SPECI prefix, trailing `$`, RVR tokens, full realistic METARs / 边界情况 |

**`tests/test_routes.py`** — Flask route tests with mocked `fetch_metar` (26 tests)

使用 `unittest.mock.patch` 模拟 `fetch_metar`，零网络请求（26 个测试）

| Test class / 测试类 | What it covers / 覆盖内容 |
|---|---|
| `TestIndexRoute` | `GET /` returns 200 and HTML / 主页返回 200 和 HTML |
| `TestMetarApiValidation` | Missing, empty, numeric, too-short/long station codes / 输入校验 |
| `TestMetarApiSuccess` | Response structure, field values, automatic uppercasing / 成功响应结构与字段 |
| `TestMetarApiErrors` | 404 no data, 504 timeout, 502 connection error / 三种错误响应码 |

---

## Data Source / 数据来源

All weather data comes from the [FAA Aviation Weather Center](https://aviationweather.gov/api/data/metar). METAR reports are updated approximately every 30 minutes.

所有天气数据来自[美国联邦航空局航空气象中心](https://aviationweather.gov/api/data/metar)。METAR 报告约每 30 分钟更新一次。

---

## License / 许可证

MIT

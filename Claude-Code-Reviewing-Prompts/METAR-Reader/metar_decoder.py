"""
metar_decoder.py — METAR Weather Report Decoder
METAR 天气报文解码器

Parses raw METAR strings from aviationweather.gov and converts them
into human-readable plain English descriptions.
解析来自 aviationweather.gov 的原始 METAR 字符串，并将其转换为人类可读的普通英语描述。
"""

import re
from datetime import datetime, timezone


# ─────────────────────────────────────────────
# Helper conversion functions / 辅助换算函数
# ─────────────────────────────────────────────

def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit. / 摄氏转华氏。"""
    return round(c * 9 / 5 + 32, 1)


def knots_to_mph(knots: float) -> float:
    """Convert knots to miles per hour. / 节转英里每小时。"""
    return round(knots * 1.15078, 1)


def meters_to_feet(meters: float) -> int:
    """Convert meters to feet. / 米转英尺。"""
    return int(meters * 3.28084)


def degrees_to_cardinal(deg: int) -> str:
    """
    Convert wind direction in degrees to a cardinal/intercardinal label.
    将风向角度转换为罗经方位名称。
    """
    dirs = [
        "North", "North-Northeast", "Northeast", "East-Northeast",
        "East", "East-Southeast", "Southeast", "South-Southeast",
        "South", "South-Southwest", "Southwest", "West-Southwest",
        "West", "West-Northwest", "Northwest", "North-Northwest",
    ]
    idx = round(deg / 22.5) % 16
    return dirs[idx]


# ─────────────────────────────────────────────
# Sky condition / 天空状况映射
# ─────────────────────────────────────────────

SKY_COVERAGE = {
    "SKC": "clear skies",
    "CLR": "clear skies",
    "NSC": "no significant clouds",
    "NCD": "no clouds detected",
    "FEW": "a few clouds",       # 1–2 oktas
    "SCT": "scattered clouds",   # 3–4 oktas
    "BKN": "broken clouds",      # 5–7 oktas
    "OVC": "overcast",           # 8 oktas
    "VV":  "vertical visibility (sky obscured)",
}

# Cloud types / 云型
CLOUD_TYPE = {
    "CB":  " (cumulonimbus — thunderstorm cloud)",
    "TCU": " (towering cumulus — potential thunderstorm)",
}

# Weather phenomena / 天气现象
WEATHER_DESC = {
    # Intensity / 强度
    "-": "light",
    "+": "heavy",
    "VC": "in the vicinity",
    # Descriptor / 描述符
    "MI": "shallow",
    "PR": "partial",
    "BC": "patches of",
    "DR": "low drifting",
    "BL": "blowing",
    "SH": "shower",
    "TS": "thunderstorm",
    "FZ": "freezing",
    # Precipitation / 降水
    "RA": "rain",
    "DZ": "drizzle",
    "SN": "snow",
    "SG": "snow grains",
    "IC": "ice crystals",
    "PL": "ice pellets",
    "GR": "hail",
    "GS": "small hail",
    "UP": "unknown precipitation",
    # Obscuration / 能见度障碍
    "BR": "mist",
    "FG": "fog",
    "FU": "smoke",
    "VA": "volcanic ash",
    "DU": "dust",
    "SA": "sand",
    "HZ": "haze",
    "PY": "spray",
    # Other / 其他
    "PO": "dust/sand whirls",
    "SQ": "squalls",
    "FC": "funnel cloud / tornado",
    "SS": "sandstorm",
    "DS": "dust storm",
}


# ─────────────────────────────────────────────
# Main decoder class / 主解码器类
# ─────────────────────────────────────────────

class METARDecoder:
    """
    Decode a raw METAR string into structured data and a plain-English summary.
    将原始 METAR 字符串解码为结构化数据和普通英语摘要。
    """

    def __init__(self, raw: str):
        self.raw = raw.strip()
        self.tokens = self.raw.split()
        self.result: dict = {}
        self._decode()

    # ── Top-level decoder / 顶层解码器 ──────────

    def _decode(self):
        tokens = list(self.tokens)  # work on a copy / 使用副本操作

        # Strip optional report-type prefix (METAR / SPECI) and trailing $ / 跳过可选报文类型前缀及末尾 $
        if tokens and tokens[0] in ("METAR", "SPECI"):
            tokens.pop(0)
        if tokens and tokens[-1] == "$":
            tokens.pop()

        result = {
            "station":      self._parse_station(tokens),
            "time":         self._parse_time(tokens),
            "auto":         self._parse_auto(tokens),
            "wind":         self._parse_wind(tokens),
            "visibility":   self._parse_visibility(tokens),
            "runway_visual": self._parse_rvr(tokens),
            "weather":      self._parse_weather(tokens),
            "sky":          self._parse_sky(tokens),
            "temp_dewpoint":self._parse_temp(tokens),
            "altimeter":    self._parse_altimeter(tokens),
            "remarks":      self._parse_remarks(tokens),
        }

        result["summary"] = self._build_summary(result)
        result["condition_emoji"] = self._pick_emoji(result)
        self.result = result

    # ── Individual field parsers / 各字段解析器 ──

    def _parse_station(self, tokens: list) -> dict:
        """Station ICAO identifier. / 机场 ICAO 识别码。"""
        if tokens and re.match(r'^[A-Z]{4}$', tokens[0]):
            return {"raw": tokens.pop(0)}
        return {"raw": "UNKNOWN"}

    def _parse_time(self, tokens: list) -> dict:
        """
        Day/Time group: DDHHMMz  e.g. 131453Z
        日期时间组: 日时分Z
        """
        if tokens and re.match(r'^\d{6}Z$', tokens[0]):
            t = tokens.pop(0)
            day  = int(t[0:2])
            hour = int(t[2:4])
            minute = int(t[4:6])
            return {
                "raw": t,
                "day": day,
                "hour": hour,
                "minute": minute,
                "display": f"Day {day} of the month, {hour:02d}:{minute:02d} UTC",
            }
        return {"raw": "", "display": "Unknown time"}

    def _parse_auto(self, tokens: list) -> bool:
        """AUTO flag — station is fully automated. / 自动站标志。"""
        if tokens and tokens[0] == "AUTO":
            tokens.pop(0)
            return True
        return False

    def _parse_wind(self, tokens: list) -> dict:
        """
        Wind group: dddssKT or dddssGggKT or VRB05KT
        风组: 方向速度(阵风)单位
        """
        pattern = re.compile(
            r'^(VRB|\d{3})(\d{2,3})(G(\d{2,3}))?(KT|MPS|KMH)$'
        )
        if tokens and pattern.match(tokens[0]):
            m = pattern.match(tokens.pop(0))
            raw_dir, raw_spd, _, raw_gust, unit = m.groups()

            speed = int(raw_spd)
            gust  = int(raw_gust) if raw_gust else None

            # Convert to mph / 换算为英里每小时
            if unit == "KT":
                speed_mph = knots_to_mph(speed)
                gust_mph  = knots_to_mph(gust) if gust else None
            elif unit == "MPS":
                speed_mph = round(speed * 2.23694, 1)
                gust_mph  = round(gust * 2.23694, 1) if gust else None
            else:  # KMH
                speed_mph = round(speed * 0.621371, 1)
                gust_mph  = round(gust * 0.621371, 1) if gust else None

            calm = (speed == 0)
            variable_dir = (raw_dir == "VRB")
            direction_deg = None if variable_dir else int(raw_dir)
            cardinal = "variable direction" if variable_dir else degrees_to_cardinal(direction_deg)

            # Variable wind direction range e.g. 280V350 / 可变风向范围
            var_range = None
            if tokens and re.match(r'^\d{3}V\d{3}$', tokens[0]):
                var_range = tokens.pop(0)

            return {
                "raw": m.group(0),
                "calm": calm,
                "direction_deg": direction_deg,
                "cardinal": cardinal,
                "speed_mph": speed_mph,
                "gust_mph": gust_mph,
                "unit": unit,
                "variable_range": var_range,
            }
        return {"raw": "", "calm": True, "direction_deg": None, "cardinal": "unknown",
                "speed_mph": 0, "gust_mph": None, "unit": "KT"}

    def _parse_visibility(self, tokens: list) -> dict:
        """
        Prevailing visibility — handles SM (statute miles) and meters.
        能见度 — 处理英里制和米制。
        """
        # Fractional SM: e.g. 1/4SM or 1 1/4SM / 分数英里
        frac_pattern = re.compile(r'^(\d+)?(\d/\d)SM$')
        sm_pattern   = re.compile(r'^(\d+)SM$')
        m_pattern    = re.compile(r'^(\d{4})$')  # ICAO meters / ICAO 米制

        vis_miles = None

        if tokens:
            # Check for "whole + fraction" spread across two tokens / 整数+分数两个 token
            two = " ".join(tokens[:2]) if len(tokens) >= 2 else ""
            m2 = frac_pattern.match(two.replace(" ", ""))
            if m2:
                whole = int(m2.group(1)) if m2.group(1) else 0
                num, den = m2.group(2).split("/")
                vis_miles = whole + int(num) / int(den)
                # Remove consumed tokens / 移除已消耗的 token
                if " " in two and frac_pattern.match(tokens[0]):
                    tokens.pop(0)
                tokens.pop(0)
            elif sm_pattern.match(tokens[0]):
                vis_miles = float(sm_pattern.match(tokens[0]).group(1))
                tokens.pop(0)
            elif m_pattern.match(tokens[0]) and int(tokens[0]) <= 9999:
                vis_m = int(tokens[0])
                vis_miles = round(vis_m / 1609.34, 1)
                tokens.pop(0)

        if vis_miles is None:
            return {"raw": "", "display": "Visibility not reported"}

        if vis_miles >= 10:
            display = "More than 10 miles visibility (excellent)"
        elif vis_miles >= 5:
            display = f"{vis_miles} miles visibility (good)"
        elif vis_miles >= 1:
            display = f"{vis_miles} miles visibility (moderate)"
        else:
            display = f"{vis_miles} miles visibility (poor — low visibility conditions)"

        return {"raw": str(vis_miles), "miles": vis_miles, "display": display}

    def _parse_rvr(self, tokens: list) -> list:
        """
        Runway Visual Range: R28L/2400FT  — strip from token list.
        跑道视程 — 从 token 列表中移除。
        """
        rvr_list = []
        while tokens and tokens[0].startswith("R") and "/" in tokens[0]:
            rvr_list.append(tokens.pop(0))
        return rvr_list

    def _parse_weather(self, tokens: list) -> list:
        """
        Present weather phenomena, e.g. -RA, +TSRA, BR, FG, BLSN
        当前天气现象
        """
        wx_pattern = re.compile(
            r'^([-+]|VC)?(MI|PR|BC|DR|BL|SH|TS|FZ)?'
            r'(RA|DZ|SN|SG|IC|PL|GR|GS|UP|BR|FG|FU|VA|DU|SA|HZ|PY|PO|SQ|FC|SS|DS)(\w*)$'
        )
        results = []
        while tokens and wx_pattern.match(tokens[0]):
            raw = tokens.pop(0)
            m = wx_pattern.match(raw)
            intensity = WEATHER_DESC.get(m.group(1), "")
            descriptor = WEATHER_DESC.get(m.group(2), "")
            phenomenon = WEATHER_DESC.get(m.group(3), m.group(3))
            parts = [p for p in [intensity, descriptor, phenomenon] if p]
            results.append({"raw": raw, "display": " ".join(parts)})
        return results

    def _parse_sky(self, tokens: list) -> list:
        """
        Sky condition groups: FEW015, SCT040, BKN080CB, OVC010, CLR, SKC
        天空状况组
        """
        sky_pattern = re.compile(
            r'^(SKC|CLR|NSC|NCD|FEW|SCT|BKN|OVC|VV)(\d{3})?(CB|TCU)?$'
        )
        layers = []
        while tokens and sky_pattern.match(tokens[0]):
            raw = tokens.pop(0)
            m = sky_pattern.match(raw)
            coverage_code = m.group(1)
            height_code   = m.group(2)
            cloud_type    = m.group(3)

            coverage = SKY_COVERAGE.get(coverage_code, coverage_code)
            height_ft = int(height_code) * 100 if height_code else None
            suffix = CLOUD_TYPE.get(cloud_type, "") if cloud_type else ""

            if height_ft is not None:
                display = f"{coverage.capitalize()} at {height_ft:,} ft{suffix}"
            else:
                display = coverage.capitalize()

            layers.append({"raw": raw, "coverage": coverage_code,
                           "height_ft": height_ft, "display": display})
        return layers

    def _parse_temp(self, tokens: list) -> dict:
        """
        Temperature / dew point: TT/DD  e.g. 11/01, M05/M10
        气温/露点  (M prefix = negative / M 前缀表示负值)
        """
        pattern = re.compile(r'^(M?\d{2})/(M?\d{2})$')
        if tokens and pattern.match(tokens[0]):
            raw = tokens.pop(0)
            m = pattern.match(raw)

            def parse_val(s):
                return -int(s[1:]) if s.startswith("M") else int(s)

            temp_c = parse_val(m.group(1))
            dew_c  = parse_val(m.group(2))
            temp_f = celsius_to_fahrenheit(temp_c)
            dew_f  = celsius_to_fahrenheit(dew_c)

            # Relative humidity approximation / 相对湿度近似值
            rh = round(100 * (112 - 0.1 * temp_c + dew_c) / (112 + 0.9 * temp_c))
            rh = max(0, min(100, rh))

            return {
                "raw": raw,
                "temp_c": temp_c,
                "temp_f": temp_f,
                "dew_c": dew_c,
                "dew_f": dew_f,
                "humidity_pct": rh,
                "display": f"{temp_f}°F ({temp_c}°C), dew point {dew_f}°F ({dew_c}°C), humidity ~{rh}%",
            }
        return {"raw": "", "temp_c": None, "temp_f": None,
                "dew_c": None, "dew_f": None, "humidity_pct": None,
                "display": "Temperature not reported"}

    def _parse_altimeter(self, tokens: list) -> dict:
        """
        Altimeter: A2992 (inches Hg) or Q1013 (hPa)
        气压计: 英制或公制
        """
        a_pattern = re.compile(r'^A(\d{4})$')
        q_pattern = re.compile(r'^Q(\d{4})$')
        if tokens:
            if a_pattern.match(tokens[0]):
                raw = tokens.pop(0)
                inhg = int(a_pattern.match(raw).group(1)) / 100
                hpa  = round(inhg * 33.8639)
                return {"raw": raw, "inhg": inhg, "hpa": hpa,
                        "display": f"{inhg:.2f} inHg ({hpa} hPa)"}
            if q_pattern.match(tokens[0]):
                raw = tokens.pop(0)
                hpa  = int(q_pattern.match(raw).group(1))
                inhg = round(hpa / 33.8639, 2)
                return {"raw": raw, "inhg": inhg, "hpa": hpa,
                        "display": f"{hpa} hPa ({inhg:.2f} inHg)"}
        return {"raw": "", "inhg": None, "hpa": None, "display": "Pressure not reported"}

    def _parse_remarks(self, tokens: list) -> str:
        """Everything after RMK is remarks — return as-is. / RMK 之后的内容作为备注原样返回。"""
        if "RMK" in tokens:
            idx = tokens.index("RMK")
            remarks = " ".join(tokens[idx + 1:])
            del tokens[idx:]
            return remarks
        return ""

    # ── Plain-English summary builder / 普通英语摘要构建器 ──

    def _build_summary(self, r: dict) -> str:
        parts = []

        # Sky / 天空
        sky_layers = r.get("sky", [])
        if sky_layers:
            dominant = sky_layers[-1]  # highest/worst layer / 最高/最差层
            code = dominant["coverage"]
            if code in ("SKC", "CLR", "NSC", "NCD"):
                parts.append("Clear skies")
            elif code == "FEW":
                parts.append("Mostly clear with a few clouds")
            elif code == "SCT":
                parts.append("Partly cloudy")
            elif code == "BKN":
                parts.append("Mostly cloudy")
            elif code == "OVC":
                parts.append("Overcast (completely cloudy)")
            elif code == "VV":
                parts.append("Sky obscured")
        else:
            parts.append("Sky condition not reported")

        # Weather phenomena / 天气现象
        wx = r.get("weather", [])
        if wx:
            wx_str = ", ".join(w["display"] for w in wx)
            parts.append(f"with {wx_str}")

        # Temperature / 温度
        td = r.get("temp_dewpoint", {})
        if td.get("temp_f") is not None:
            parts.append(f"{td['temp_f']}°F ({td['temp_c']}°C)")
            parts.append(f"humidity around {td['humidity_pct']}%")

        # Wind / 风
        wind = r.get("wind", {})
        if wind.get("calm"):
            parts.append("calm winds")
        elif wind.get("speed_mph") is not None:
            spd = wind["speed_mph"]
            cardinal = wind["cardinal"]
            gust = wind.get("gust_mph")
            wind_str = f"winds {spd} mph from the {cardinal}"
            if gust:
                wind_str += f", gusting to {gust} mph"
            parts.append(wind_str)

        # Visibility / 能见度
        vis = r.get("visibility", {})
        if vis.get("miles") is not None:
            if vis["miles"] >= 10:
                parts.append("excellent visibility")
            else:
                parts.append(f"visibility {vis['miles']} miles")

        # Altimeter / 气压
        alt = r.get("altimeter", {})
        if alt.get("inhg"):
            parts.append(f"pressure {alt['inhg']:.2f} inHg")

        return ". ".join(parts) + "." if parts else "Unable to parse weather data."

    def _pick_emoji(self, r: dict) -> str:
        """Choose a weather emoji based on conditions. / 根据天气状况选择 emoji。"""
        wx_codes = [w["raw"] for w in r.get("weather", [])]
        sky_codes = [s["coverage"] for s in r.get("sky", [])]

        # Thunderstorm / 雷暴
        if any("TS" in w for w in wx_codes):
            return "⛈️"
        # Snow / 雪
        if any("SN" in w or "SG" in w or "PL" in w for w in wx_codes):
            return "❄️"
        # Rain / 雨
        if any("RA" in w or "DZ" in w for w in wx_codes):
            return "🌧️"
        # Fog / mist / 雾/薄雾
        if any(w in ("FG", "BR") for w in wx_codes):
            return "🌫️"
        # Overcast / broken / 阴/多云
        if "OVC" in sky_codes:
            return "☁️"
        if "BKN" in sky_codes:
            return "🌥️"
        if "SCT" in sky_codes:
            return "⛅"
        # Clear / 晴
        return "☀️"

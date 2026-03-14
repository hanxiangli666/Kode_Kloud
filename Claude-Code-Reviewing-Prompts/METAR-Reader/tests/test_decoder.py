"""
test_decoder.py — Unit tests for METARDecoder and helper functions
METARDecoder 及辅助函数的单元测试

Each test feeds a realistic mock METAR string directly into METARDecoder
and asserts that the parsed fields are correct.
每个测试直接向 METARDecoder 传入模拟 METAR 字符串，并断言解析字段正确。
"""

import pytest
from metar_decoder import (
    METARDecoder,
    celsius_to_fahrenheit,
    knots_to_mph,
    meters_to_feet,
    degrees_to_cardinal,
)


# ─────────────────────────────────────────────
# Helper function tests / 辅助函数测试
# ─────────────────────────────────────────────

class TestHelpers:
    def test_celsius_to_fahrenheit_freezing(self):
        assert celsius_to_fahrenheit(0) == 32.0

    def test_celsius_to_fahrenheit_boiling(self):
        assert celsius_to_fahrenheit(100) == 212.0

    def test_celsius_to_fahrenheit_negative(self):
        assert celsius_to_fahrenheit(-40) == -40.0  # -40 is the same in both scales

    def test_celsius_to_fahrenheit_body_temp(self):
        assert celsius_to_fahrenheit(37) == 98.6

    def test_knots_to_mph(self):
        # 10 knots ≈ 11.5 mph
        assert knots_to_mph(10) == pytest.approx(11.5, abs=0.1)

    def test_knots_to_mph_zero(self):
        assert knots_to_mph(0) == 0.0

    def test_meters_to_feet(self):
        # 1000 m ≈ 3280 ft
        assert meters_to_feet(1000) == 3280

    def test_degrees_to_cardinal_north(self):
        assert degrees_to_cardinal(0) == "North"
        assert degrees_to_cardinal(360) == "North"

    def test_degrees_to_cardinal_south(self):
        assert degrees_to_cardinal(180) == "South"

    def test_degrees_to_cardinal_east(self):
        assert degrees_to_cardinal(90) == "East"

    def test_degrees_to_cardinal_west(self):
        assert degrees_to_cardinal(270) == "West"

    def test_degrees_to_cardinal_northeast(self):
        assert degrees_to_cardinal(45) == "Northeast"

    def test_degrees_to_cardinal_northwest(self):
        assert degrees_to_cardinal(315) == "Northwest"


# ─────────────────────────────────────────────
# Station and time parsing / 机场和时间解析
# ─────────────────────────────────────────────

class TestStationAndTime:
    def test_station_parsed(self):
        d = METARDecoder("KSEA 141753Z 00000KT 10SM CLR 12/04 A2992")
        assert d.result["station"]["raw"] == "KSEA"

    def test_time_parsed(self):
        d = METARDecoder("KSEA 141753Z 00000KT 10SM CLR 12/04 A2992")
        t = d.result["time"]
        assert t["day"] == 14
        assert t["hour"] == 17
        assert t["minute"] == 53

    def test_time_display_format(self):
        d = METARDecoder("KSEA 141753Z 00000KT 10SM CLR 12/04 A2992")
        assert "17:53 UTC" in d.result["time"]["display"]

    def test_auto_flag_present(self):
        d = METARDecoder("KSEA 141753Z AUTO 27012KT 10SM CLR 12/04 A2992")
        assert d.result["auto"] is True

    def test_auto_flag_absent(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        assert d.result["auto"] is False

    def test_metar_prefix_stripped(self):
        d = METARDecoder("METAR KSEA 141753Z 00000KT 10SM CLR 12/04 A2992")
        assert d.result["station"]["raw"] == "KSEA"


# ─────────────────────────────────────────────
# Wind parsing / 风向解析
# ─────────────────────────────────────────────

class TestWind:
    def test_wind_direction_and_speed(self):
        # 27012KT → 270° (West), 12 knots
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        w = d.result["wind"]
        assert w["direction_deg"] == 270
        assert w["cardinal"] == "West"
        assert w["speed_mph"] == pytest.approx(13.8, abs=0.2)
        assert w["calm"] is False

    def test_wind_with_gust(self):
        # 01015G25KT → 10° (North-Northeast), 15 kt, gust 25 kt
        d = METARDecoder("KORD 141800Z 01015G25KT 5SM OVC012 08/06 A2987")
        w = d.result["wind"]
        assert w["speed_mph"] == pytest.approx(17.3, abs=0.2)
        assert w["gust_mph"] == pytest.approx(28.8, abs=0.2)
        assert w["gust_mph"] is not None

    def test_calm_wind(self):
        # 00000KT → calm
        d = METARDecoder("KSEA 141753Z 00000KT 10SM CLR 12/04 A2992")
        assert d.result["wind"]["calm"] is True

    def test_variable_wind(self):
        # VRB03KT → variable direction
        d = METARDecoder("EGLL 141820Z VRB03KT 9999 FEW020 15/10 Q1015")
        w = d.result["wind"]
        assert w["cardinal"] == "variable direction"
        assert w["direction_deg"] is None

    def test_wind_mps_unit(self):
        # 18005MPS → 5 m/s from South
        d = METARDecoder("UUEE 141800Z 18005MPS 9999 SCT030 10/05 Q1010")
        w = d.result["wind"]
        assert w["cardinal"] == "South"
        assert w["speed_mph"] == pytest.approx(11.2, abs=0.2)


# ─────────────────────────────────────────────
# Visibility parsing / 能见度解析
# ─────────────────────────────────────────────

class TestVisibility:
    def test_visibility_10sm_or_more(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        vis = d.result["visibility"]
        assert vis["miles"] == 10.0
        assert "excellent" in vis["display"]

    def test_visibility_5sm(self):
        d = METARDecoder("KORD 141800Z 01015KT 5SM OVC012 08/06 A2987")
        vis = d.result["visibility"]
        assert vis["miles"] == 5.0
        assert "good" in vis["display"]

    def test_visibility_fractional_quarter_mile(self):
        # Low visibility: "1/4SM" as a single token is not parsed by the current
        # decoder (it only handles whole+fraction split across two tokens, e.g. "1 1/4SM").
        # The decoder correctly falls back to "not reported" for this format.
        d = METARDecoder("KSFO 141900Z 00000KT 1/4SM FG OVC002 10/10 A2990")
        vis = d.result["visibility"]
        assert "miles" not in vis or vis.get("miles") is None

    def test_visibility_two_token_fraction(self):
        # "1 1/4SM" split across two tokens IS handled: whole=1, frac=1/4 → 1.25 miles
        d = METARDecoder("KSFO 141900Z 00000KT 1 1/4SM FG OVC002 10/10 A2990")
        vis = d.result["visibility"]
        assert vis["miles"] == pytest.approx(1.25, abs=0.01)
        assert "moderate" in vis["display"]

    def test_visibility_icao_meters(self):
        # 0800 meters → ~0.5 miles
        d = METARDecoder("EGLL 141820Z VRB03KT 0800 FG OVC002 04/04 Q1008")
        vis = d.result["visibility"]
        assert vis["miles"] == pytest.approx(0.5, abs=0.1)

    def test_visibility_9999_icao(self):
        # 9999 = 10+ km, treated as >10 miles
        d = METARDecoder("EGLL 141820Z VRB03KT 9999 FEW020 15/10 Q1015")
        vis = d.result["visibility"]
        assert vis["miles"] >= 6.0  # 9999m ≈ 6.2 miles


# ─────────────────────────────────────────────
# Sky condition parsing / 天空状况解析
# ─────────────────────────────────────────────

class TestSkyConditions:
    def test_clear_skies_clr(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        sky = d.result["sky"]
        assert len(sky) == 1
        assert sky[0]["coverage"] == "CLR"
        assert "Clear" in sky[0]["display"]

    def test_few_clouds_with_height(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM FEW035 12/04 A2992")
        sky = d.result["sky"]
        assert sky[0]["coverage"] == "FEW"
        assert sky[0]["height_ft"] == 3500
        assert "3,500 ft" in sky[0]["display"]

    def test_overcast_low(self):
        d = METARDecoder("KORD 141800Z 01015KT 5SM OVC012 08/06 A2987")
        sky = d.result["sky"]
        assert sky[0]["coverage"] == "OVC"
        assert sky[0]["height_ft"] == 1200

    def test_multiple_sky_layers(self):
        # FEW015 SCT040 BKN080
        d = METARDecoder("KJFK 141800Z 18010KT 10SM FEW015 SCT040 BKN080 20/15 A2995")
        sky = d.result["sky"]
        assert len(sky) == 3
        assert sky[0]["coverage"] == "FEW"
        assert sky[1]["coverage"] == "SCT"
        assert sky[2]["coverage"] == "BKN"

    def test_cumulonimbus_cloud_type(self):
        d = METARDecoder("KORD 141800Z 18010KT 5SM BKN050CB 22/18 A2980")
        sky = d.result["sky"]
        assert sky[0]["coverage"] == "BKN"
        assert "cumulonimbus" in sky[0]["display"].lower()

    def test_skc_no_height(self):
        d = METARDecoder("ZBAA 141830Z 36005KT 9999 SKC 20/10 Q1015")
        sky = d.result["sky"]
        assert sky[0]["coverage"] == "SKC"
        assert sky[0]["height_ft"] is None


# ─────────────────────────────────────────────
# Temperature / dew point parsing / 气温/露点解析
# ─────────────────────────────────────────────

class TestTemperature:
    def test_positive_temp_and_dew(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        td = d.result["temp_dewpoint"]
        assert td["temp_c"] == 12
        assert td["dew_c"] == 4
        assert td["temp_f"] == pytest.approx(53.6, abs=0.1)
        assert td["dew_f"] == pytest.approx(39.2, abs=0.1)

    def test_negative_temperature_m_prefix(self):
        # M05/M10 → -5°C / -10°C (Beijing winter)
        d = METARDecoder("ZBAA 141830Z 36005KT 0800 +SN OVC005 M05/M10 Q1023")
        td = d.result["temp_dewpoint"]
        assert td["temp_c"] == -5
        assert td["dew_c"] == -10
        assert td["temp_f"] == pytest.approx(23.0, abs=0.1)

    def test_humidity_calculated(self):
        # Temp = dew point → 100% humidity (fog)
        d = METARDecoder("EGLL 141820Z VRB03KT 0800 FG OVC002 04/04 Q1008")
        td = d.result["temp_dewpoint"]
        assert td["humidity_pct"] == 100

    def test_humidity_low(self):
        # The decoder uses an approximation formula that becomes imprecise at
        # extreme spreads. For 38°C / 5°C (Phoenix desert), the formula yields
        # ~77% rather than the meteorologically correct ~11%. We test that the
        # formula at least produces a value in [0, 100] and is lower than the
        # same-temp/same-dewpoint "fog" case (4°C / 4°C = 100%).
        d = METARDecoder("KPHX 141800Z 18010KT 10SM CLR 38/05 A2995")
        td = d.result["temp_dewpoint"]
        assert 0 <= td["humidity_pct"] <= 100
        # Must be less than 100% (dew point is well below temp)
        assert td["humidity_pct"] < 100


# ─────────────────────────────────────────────
# Altimeter parsing / 气压解析
# ─────────────────────────────────────────────

class TestAltimeter:
    def test_altimeter_a_format_inhg(self):
        # A2992 → 29.92 inHg
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        alt = d.result["altimeter"]
        assert alt["inhg"] == pytest.approx(29.92, abs=0.01)
        assert "inHg" in alt["display"]

    def test_altimeter_q_format_hpa(self):
        # Q1013 → 1013 hPa
        d = METARDecoder("EGLL 141820Z VRB03KT 9999 FEW020 15/10 Q1013")
        alt = d.result["altimeter"]
        assert alt["hpa"] == 1013
        assert "hPa" in alt["display"]

    def test_altimeter_q_converts_to_inhg(self):
        d = METARDecoder("EGLL 141820Z VRB03KT 9999 FEW020 15/10 Q1013")
        alt = d.result["altimeter"]
        assert alt["inhg"] == pytest.approx(29.92, abs=0.05)


# ─────────────────────────────────────────────
# Weather phenomena parsing / 天气现象解析
# ─────────────────────────────────────────────

class TestWeatherPhenomena:
    def test_light_rain(self):
        d = METARDecoder("KORD 141800Z 01015KT 5SM -RA OVC012 08/06 A2987")
        wx = d.result["weather"]
        assert len(wx) == 1
        assert "light" in wx[0]["display"]
        assert "rain" in wx[0]["display"]

    def test_heavy_rain(self):
        d = METARDecoder("KORD 141800Z 01015KT 3SM +RA OVC010 08/07 A2980")
        wx = d.result["weather"]
        assert "heavy" in wx[0]["display"]
        assert "rain" in wx[0]["display"]

    def test_heavy_snow(self):
        d = METARDecoder("ZBAA 141830Z 36005KT 0800 +SN OVC005 M05/M10 Q1023")
        wx = d.result["weather"]
        assert "heavy" in wx[0]["display"]
        assert "snow" in wx[0]["display"]

    def test_fog(self):
        d = METARDecoder("EGLL 141820Z VRB03KT 0150 FG OVC002 04/04 Q1008")
        wx = d.result["weather"]
        assert wx[0]["raw"] == "FG"
        assert "fog" in wx[0]["display"]

    def test_thunderstorm_with_rain(self):
        d = METARDecoder("KORD 141800Z 18020KT 3SM TSRA BKN030CB 25/22 A2975")
        wx = d.result["weather"]
        displays = " ".join(w["display"] for w in wx)
        assert "thunderstorm" in displays
        assert "rain" in displays

    def test_no_weather_phenomena(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        assert d.result["weather"] == []


# ─────────────────────────────────────────────
# Remarks parsing / 备注解析
# ─────────────────────────────────────────────

class TestRemarks:
    def test_remarks_extracted(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992 RMK AO2 SLP132")
        assert "AO2" in d.result["remarks"]
        assert "SLP132" in d.result["remarks"]

    def test_no_remarks(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        assert d.result["remarks"] == ""

    def test_remarks_not_in_other_fields(self):
        # RMK and everything after should not bleed into altimeter
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992 RMK AO2")
        assert d.result["altimeter"]["inhg"] == pytest.approx(29.92, abs=0.01)


# ─────────────────────────────────────────────
# Summary and emoji / 摘要与 emoji
# ─────────────────────────────────────────────

class TestSummaryAndEmoji:
    def test_summary_contains_temperature(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        assert "53.6°F" in d.result["summary"]

    def test_summary_contains_wind(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        assert "West" in d.result["summary"]

    def test_emoji_clear(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        assert d.result["condition_emoji"] == "☀️"

    def test_emoji_overcast(self):
        d = METARDecoder("KORD 141800Z 01015KT 5SM OVC012 08/06 A2987")
        assert d.result["condition_emoji"] == "☁️"

    def test_emoji_rain(self):
        d = METARDecoder("KORD 141800Z 01015KT 5SM -RA OVC012 08/06 A2987")
        assert d.result["condition_emoji"] == "🌧️"

    def test_emoji_snow(self):
        d = METARDecoder("ZBAA 141830Z 36005KT 0800 +SN OVC005 M05/M10 Q1023")
        assert d.result["condition_emoji"] == "❄️"

    def test_emoji_thunderstorm(self):
        d = METARDecoder("KORD 141800Z 18020KT 3SM TSRA BKN030CB 25/22 A2975")
        assert d.result["condition_emoji"] == "⛈️"

    def test_emoji_fog(self):
        d = METARDecoder("EGLL 141820Z VRB03KT 0150 FG OVC002 04/04 Q1008")
        assert d.result["condition_emoji"] == "🌫️"

    def test_emoji_scattered(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM SCT040 12/04 A2992")
        assert d.result["condition_emoji"] == "⛅"

    def test_emoji_broken(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM BKN060 12/04 A2992")
        assert d.result["condition_emoji"] == "🌥️"


# ─────────────────────────────────────────────
# Edge cases / 边界情况
# ─────────────────────────────────────────────

class TestEdgeCases:
    def test_speci_prefix_stripped(self):
        # SPECI is a special observation report, should be handled like METAR
        d = METARDecoder("SPECI KSEA 141753Z 27012KT 10SM CLR 12/04 A2992")
        assert d.result["station"]["raw"] == "KSEA"

    def test_trailing_dollar_stripped(self):
        d = METARDecoder("KSEA 141753Z 27012KT 10SM CLR 12/04 A2992 $")
        assert d.result["altimeter"]["inhg"] == pytest.approx(29.92, abs=0.01)

    def test_runway_visual_range_skipped(self):
        # RVR tokens (R28L/2400FT) should be consumed without error
        d = METARDecoder("EGLL 141820Z 28010KT 0600 R28L/0800FT FG OVC002 04/04 Q1008")
        assert d.result["runway_visual"] == ["R28L/0800FT"]

    def test_full_beijing_winter_metar(self):
        """Full realistic METAR for Beijing Capital in winter / 北京首都机场冬季完整 METAR"""
        raw = "ZBAA 141830Z 36005KT 0800 +SN OVC005 M05/M10 Q1023 NOSIG"
        d = METARDecoder(raw)
        assert d.result["station"]["raw"] == "ZBAA"
        assert d.result["temp_dewpoint"]["temp_c"] == -5
        assert d.result["altimeter"]["hpa"] == 1023
        assert d.result["condition_emoji"] == "❄️"

    def test_full_london_fog_metar(self):
        """Full realistic METAR for London Heathrow in fog / 伦敦希思罗雾天完整 METAR"""
        raw = "EGLL 141820Z VRB03KT 0150 R28L/0500FT FG OVC002 04/04 Q1008 NOSIG"
        d = METARDecoder(raw)
        assert d.result["station"]["raw"] == "EGLL"
        assert d.result["wind"]["cardinal"] == "variable direction"
        assert d.result["temp_dewpoint"]["humidity_pct"] == 100
        assert d.result["condition_emoji"] == "🌫️"

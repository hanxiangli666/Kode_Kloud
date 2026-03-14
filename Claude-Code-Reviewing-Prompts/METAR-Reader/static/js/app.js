/**
 * app.js — METAR Reader frontend logic
 * METAR 阅读器前端逻辑
 *
 * Handles user input, calls the Flask API, and renders the decoded
 * weather data onto the page.
 * 处理用户输入，调用 Flask API，并将解码的天气数据渲染到页面上。
 */

// ── DOM references / DOM 引用 ──────────────────
const input       = document.getElementById("station-input");
const searchBtn   = document.getElementById("search-btn");
const loading     = document.getElementById("loading");
const errorBox    = document.getElementById("error-box");
const resultCard  = document.getElementById("result-card");

// Result fields / 结果字段
const resultEmoji   = document.getElementById("result-emoji");
const resultStation = document.getElementById("result-station");
const resultTime    = document.getElementById("result-time");
const resultSummary = document.getElementById("result-summary");
const valSky        = document.getElementById("val-sky");
const valTemp       = document.getElementById("val-temp");
const valHumidity   = document.getElementById("val-humidity");
const valWind       = document.getElementById("val-wind");
const valVis        = document.getElementById("val-vis");
const valAlt        = document.getElementById("val-alt");
const rawMetar      = document.getElementById("raw-metar");

// ── State helpers / 状态辅助函数 ──────────────

function showLoading() {
  hide(errorBox);
  hide(resultCard);
  show(loading);
}

function showError(msg) {
  hide(loading);
  hide(resultCard);
  errorBox.textContent = "⚠️  " + msg;
  show(errorBox);
}

function show(el)  { el.classList.remove("hidden"); }
function hide(el)  { el.classList.add("hidden"); }

// ── Main fetch / 主请求函数 ───────────────────

async function fetchWeather(station) {
  if (!station) { showError("Please enter an airport code."); return; }

  showLoading();

  try {
    const res  = await fetch(`/api/metar?station=${encodeURIComponent(station)}`);
    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "An unexpected error occurred.");
      return;
    }

    renderResult(data);
  } catch (err) {
    showError("Network error — could not reach the server. Is Flask running?");
    console.error(err);
  }
}

// ── Render decoded data / 渲染解码数据 ──────────

function renderResult(data) {
  hide(loading);
  const d = data.decoded;

  // ── Emoji + station + time / emoji + 机场 + 时间
  resultEmoji.textContent   = d.condition_emoji || "🌡️";
  resultStation.textContent = d.station?.raw || "Unknown";
  resultTime.textContent    = d.time?.display || "";

  // ── Plain-English summary / 普通英语摘要
  resultSummary.textContent = d.summary || "No summary available.";

  // ── Sky / 天空
  if (d.sky && d.sky.length > 0) {
    valSky.innerHTML = d.sky.map(s => s.display).join("<br/>");
  } else {
    valSky.textContent = "Not reported";
  }

  // ── Temperature / 温度
  const td = d.temp_dewpoint;
  if (td?.temp_f !== null && td?.temp_f !== undefined) {
    valTemp.innerHTML = `${td.temp_f}°F / ${td.temp_c}°C<br/>
                         <small style="font-weight:400;color:#6b7f9e">
                           Dew point: ${td.dew_f}°F / ${td.dew_c}°C
                         </small>`;
  } else {
    valTemp.textContent = "Not reported";
  }

  // ── Humidity / 湿度
  valHumidity.textContent = (td?.humidity_pct != null)
    ? `${td.humidity_pct}%`
    : "Not reported";

  // ── Wind / 风
  const w = d.wind;
  if (w?.calm) {
    valWind.textContent = "Calm";
  } else if (w?.speed_mph != null) {
    let windStr = `${w.speed_mph} mph from the ${w.cardinal}`;
    if (w.gust_mph) windStr += ` (gusts ${w.gust_mph} mph)`;
    valWind.textContent = windStr;
  } else {
    valWind.textContent = "Not reported";
  }

  // ── Visibility / 能见度
  valVis.textContent = d.visibility?.display || "Not reported";

  // ── Altimeter / 气压
  valAlt.textContent = d.altimeter?.display || "Not reported";

  // ── Raw METAR / 原始 METAR
  rawMetar.textContent = data.raw || "";

  show(resultCard);
}

// ── Event listeners / 事件监听器 ─────────────

searchBtn.addEventListener("click", () => {
  fetchWeather(input.value.trim().toUpperCase());
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    fetchWeather(input.value.trim().toUpperCase());
  }
});

// ── Quick-pick buttons / 快速选择按钮 ─────────
document.querySelectorAll(".quick-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const code = btn.dataset.code;
    input.value = code;
    fetchWeather(code);
  });
});

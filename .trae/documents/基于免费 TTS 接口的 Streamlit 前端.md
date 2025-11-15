## 项目目标
- 封装 `https://dds.dui.ai/runtime/v1/synthesize` 免费 TTS 接口，提供中文界面输入文本、选择发音人、语速、音量与音频格式，生成并播放/下载音频。
- 纯前端体验由 Streamlit 驱动，服务端调用接口避免浏览器 CORS 与跨域问题。

## 关键功能
- 文本输入与长度校验（≤200字，来源：一个免费的TTS接口 | 虫子樱桃 [1]）。
- 发音人选择（默认 `ppangf_csn`，支持自定义与若干预置）。
- 参数控制：`speed`、`volume`、`audioType`。
- 生成音频后页面播放与下载。
- 请求结果缓存，减少重复调用。

## 技术方案
- 框架：`streamlit` 用于快速搭建交互式页面。
- 网络：`requests` 使用 `GET` 方式携带 `params` 访问 TTS 接口并接收二进制音频。
- 缓存：`st.cache_data` 以文本与参数为键进行缓存。
- 结构：单文件 `app.py`，后续可拆分为模块。

## 交互与校验
- 文本框与实时统计；按钮触发合成；异常弹窗反馈。
- 语速范围 `0.5–2.0`（步进 `0.1`），音量 `0–100`（步进 `1`）。
- 音频格式首选 `wav`，可提供 `mp3` 选项；若远端不支持，则提示错误。

## 错误处理
- HTTP 错误码统一提示；超时与网络异常区分展示。
- 文本为空或超长即时拦截，避免无效请求。

## 代码骨架
```python
import streamlit as st
import requests

st.set_page_config(page_title="免费 TTS 接口封装", page_icon="🔊", layout="centered")

st.title("免费 TTS 接口封装")
text = st.text_area("输入文本（≤200字）", "您好世界")
voice = st.selectbox("发音人", ["ppangf_csn", "qiumum_0gushi", "kaolam_diantai", "juan1f"], index=0)
speed = st.slider("语速", 0.5, 2.0, 1.0, 0.1)
volume = st.slider("音量", 0, 100, 50, 1)
audio_type = st.selectbox("音频格式", ["wav", "mp3"], index=0)

@st.cache_data(show_spinner=False)
def synthesize(text, voice, speed, volume, audio_type):
    base = "https://dds.dui.ai/runtime/v1/synthesize"
    params = {"voiceId": voice, "text": text, "speed": speed, "volume": volume, "audioType": audio_type}
    r = requests.get(base, params=params, timeout=20)
    r.raise_for_status()
    return r.content

if st.button("生成语音"):
    if len(text) == 0 or len(text) > 200:
        st.error("文本不能为空且不超过200字")
    else:
        try:
            audio_bytes = synthesize(text, voice, speed, volume, audio_type)
            st.audio(audio_bytes, format=f"audio/{audio_type}")
            st.download_button("下载音频", audio_bytes, file_name=f"tts.{audio_type}", mime=f"audio/{audio_type}")
        except requests.HTTPError as e:
            st.error(f"请求失败：{e.response.status_code}")
        except Exception as e:
            st.error(f"发生错误：{e}")
```

## 部署与运行
- 依赖：`streamlit`, `requests`。
- 本地运行：`streamlit run app.py`。
- 可选：将接口基础 URL 等外置到配置或 Secrets。

## 后续扩展
- 发音人列表动态来源与搜索。
- 批量文本合成与队列。
- 结果持久化与历史记录。

[1] https://www.czyt.eu.org/post/a-free-tts-api/
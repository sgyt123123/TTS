import streamlit as st
import requests
import time
from urllib.parse import urlencode

st.set_page_config(page_title="TTS语音合成", page_icon="🎵", layout="wide")

BASE_URL = "https://dds.dui.ai/runtime/v1/synthesize"

VOICES = [
    {"id": "qiumum_0gushi", "name": "精品秋木", "label": "秋木・精品", "desc": "活泼开朗适合有声读物等场景"},
    {"id": "kaolam_diantai", "name": "精品考拉", "label": "考拉・电台男声", "desc": "电台男声温柔的电台男声"},
    {"id": "juan1f", "name": "小美", "label": "小美・客服", "desc": "客服女声声音甜美热情，客服、营销场景均适用"},
    {"id": "xmguof", "name": "婷", "label": "婷・营销", "desc": "营销女声音色亲切大方，适用于电话销售、调研回访等场景"},
    {"id": "xmamif", "name": "小咪", "label": "小咪・营销", "desc": "营销女声活力甜美，适用于电话营销、邀约等场景"},
    {"id": "lunaif_ctn", "name": "晓健", "label": "晓健・粤语标准", "desc": "标准粤语女声偏正式的标准粤语，适用于新闻播报等场景"},
    {"id": "hchunf_ctn", "name": "何春", "label": "何春・粤语自然", "desc": "自然粤语女声音色偏甜美自然，适用于家居播报等场景"},
    {"id": "dayaof_csd", "name": "大瑶", "label": "大瑶・山东话", "desc": "山东话女声音色偏甜美自然，适用于家居播报等场景"},
    {"id": "wqingf_csn", "name": "文卿", "label": "文卿・四川话", "desc": "四川话女声音色偏甜美自然，适用于车载导航等场景"},
    {"id": "ppangf_csn", "name": "胖胖", "label": "胖胖・四川话", "desc": "四川话女声音色偏甜美自然，适用于家居播报等场景"},
    {"id": "yezi1f_csh", "name": "叶子", "label": "叶子・上海话", "desc": "上海话女声音色偏甜美自然，适用于家居播报等场景"},
    {"id": "madoufp_yubo", "name": "麻豆", "label": "麻豆・娱播", "desc": "娱播女声甜美欢快的女声，适合做娱乐新闻的播报"},
    {"id": "madoufp_wenrou", "name": "麻豆", "label": "麻豆・温柔", "desc": "甜美温柔客服、营销、阅读听书的场景均可使用"},
    {"id": "xjingfp", "name": "小静", "label": "小静・甜美", "desc": "甜美女声音色甜美知性，可用于娱乐新闻等播报"},
    {"id": "xjingf_gushi", "name": "小静", "label": "小静・自然", "desc": "自然音色甜美知性，可用于娱乐新闻等播报"},
    {"id": "xjingf", "name": "小静", "label": "小静・商务", "desc": "商务知性音色甜美知性，可用于娱乐新闻等播报"},
    {"id": "zhilingfp", "name": "小玲", "label": "小玲・甜美女神", "desc": "甜美女神音色亲切、欢快、自然，适合用于各种场景"},
    {"id": "zhilingfp_huankuai", "name": "小玲", "label": "小玲・欢快自然", "desc": "欢快自然音色亲切、欢快、自然，适合用于各种场景"},
    {"id": "zhilingfa", "name": "小玲", "label": "小玲・标准", "desc": "标准小玲的音色亲切，甜美，自然，适合用于各种场景"},
    {"id": "zhilingf", "name": "传统小玲", "label": "传统小玲", "desc": "甜美性感音色甜美、自然、性感，适合用于各种场景"},
    {"id": "anonyf", "name": "小佚", "label": "小佚・平和沉稳", "desc": "音色沉稳严肃，适合用于新闻播报等"},
    {"id": "xbekef", "name": "贝壳", "label": "贝壳・可爱女童", "desc": "童真可爱，适合讲幼儿故事"},
    {"id": "xijunma", "name": "精品小军", "label": "小军・精品", "desc": "适合新闻播报等场景"},
    {"id": "xijunm", "name": "传统小军", "label": "小军・传统", "desc": "标准正式标准发音，适合新闻播报等场景"},
    {"id": "geyou", "name": "葛爷", "label": "葛爷・模仿", "desc": "淡定风趣模仿葛优音色"},
    {"id": "gdgm", "name": "纲叔", "label": "纲叔・模仿", "desc": "沉稳幽默模仿郭德纲音色"},
    {"id": "zxcm", "name": "星哥", "label": "星哥・模仿", "desc": "风趣幽默模仿周星驰音色"},
    {"id": "qianranf", "name": "传统然然", "label": "然然・传统", "desc": "天真俏皮成人女声模仿女童音色"},
    {"id": "hyanif", "name": "小妮", "label": "小妮・温柔亲切", "desc": "适合情感电台播报等场景"},
    {"id": "gqlanf", "name": "标准小兰", "label": "小兰・标准", "desc": "温柔的邻家女声，适合做客服音色"},
    {"id": "gqlanfp", "name": "精品小兰", "label": "小兰・精品", "desc": "温柔甜美，适合做客服音色"},
    {"id": "qianranfa", "name": "标准然然", "label": "然然・标准", "desc": "天真俏皮，语速1.2–1.4更佳"},
    {"id": "kaolaf", "name": "考拉", "label": "考拉・端庄优雅", "desc": "适合做新闻资讯等场景"},
    {"id": "smjief", "name": "小洁", "label": "小洁・亲切缓和", "desc": "推荐百科等有声读物的播报"},
    {"id": "wjianm_xsheng", "name": "小江", "label": "小江・亲切友善", "desc": "推荐电话客服场景，推荐语速1.3"},
    {"id": "feyinf", "name": "风吟", "label": "风吟・女老师", "desc": "威严正式的女老师"},
    {"id": "jlshim", "name": "季老师", "label": "季老师・成熟稳重", "desc": "适用于新闻播报的场景"},
    {"id": "lili1f_shangwu", "name": "璃璃", "label": "璃璃・商务大气", "desc": "适用于新闻、政务内容播报"},
    {"id": "lili1f_yubo", "name": "璃璃", "label": "璃璃・活力娱播", "desc": "适合娱乐新闻的播报"},
    {"id": "xizhef", "name": "行者", "label": "行者・端庄正式", "desc": "端庄严肃女声，适合社会新闻播报"},
    {"id": "cyangfp", "name": "精品初阳", "label": "初阳・精品", "desc": "乖巧可爱的女学生音色，可用于导航"},
    {"id": "cyangf", "name": "标准初阳", "label": "初阳・标准", "desc": "乖巧可爱的女学生音色，可用于导航"},
    {"id": "lzliafp", "name": "精品连连", "label": "连连・精品", "desc": "活泼可爱，推荐童话故事等有声读物"},
    {"id": "lzliafa", "name": "标准连连", "label": "连连・标准", "desc": "活泼可爱，推荐童话故事等有声读物"},
    {"id": "lzliaf", "name": "传统连连", "label": "连连・传统", "desc": "活泼可爱，推荐有声读物场景"},
    {"id": "gdfanf_natong", "name": "方方", "label": "方方・元气男孩", "desc": "推荐有声读物的场景"},
    {"id": "hyanifa", "name": "标准小妮", "label": "小妮・标准", "desc": "温柔亲切，适合情感电台播报"},
    {"id": "lucyfa", "name": "小浩", "label": "小浩・英文", "desc": "干练，适合英文场景"},
    {"id": "gdfanfp", "name": "芳芳", "label": "芳芳・甜美客服", "desc": "推荐客服场景使用"},
    {"id": "aningfp", "name": "精品安宁", "label": "安宁・精品", "desc": "温婉可人，适合哲理故事"},
    {"id": "aningf", "name": "标准安宁", "label": "安宁・标准", "desc": "温婉可人，适合哲理故事"},
    {"id": "boy", "name": "堂堂", "label": "堂堂・少先队", "desc": "推荐电话手表等智能设备场景"},
    {"id": "jjingf", "name": "标准晶晶", "label": "晶晶・标准", "desc": "知性大方，适合多种文本与场景"},
    {"id": "jjingfp", "name": "精品晶晶", "label": "晶晶・精品", "desc": "知性大方，适合多种文本与场景"},
    {"id": "kaolam", "name": "考拉", "label": "考拉・标准男声", "desc": "发音标准正式，适合新闻资讯场景"},
    {"id": "lanyuf", "name": "蓝雨", "label": "蓝雨・温柔甜美", "desc": "擅长讲童话故事"},
    {"id": "lili1f_diantai", "name": "璃璃", "label": "璃璃・电台安静", "desc": "适用情感电台场景"},
    {"id": "qiumum", "name": "秋木", "label": "秋木・活泼开朗", "desc": "推荐讲寓言故事"},
    {"id": "tzruim", "name": "小睿", "label": "小睿・活力朝气", "desc": "适合读课文"},
    {"id": "xiyaof", "name": "小妖", "label": "小妖・慵懒烟嗓", "desc": "特殊慵懒嗓音，适合悬疑小说"},
    {"id": "xiyaof_qingxin", "name": "小妖", "label": "小妖・清新甜美", "desc": "适合言情小说"},
    {"id": "yaayif", "name": "杨阿姨", "label": "杨阿姨・和蔼可亲", "desc": "适合讲百科知识等场景"},
    {"id": "zzherf", "name": "朱株儿", "label": "朱株儿・温柔舒适", "desc": "推荐讲童话故事等有声读物"},
    {"id": "juyinf_guigushi", "name": "绝音", "label": "绝音・鬼故事", "desc": "推荐讲鬼故事等恐怖场景"},
    {"id": "zzhuaf", "name": "砖砖", "label": "砖砖・自然", "desc": "推荐讲寓言故事等有声读物"},
    {"id": "yukaim_all", "name": "俞老师", "label": "俞老师・磁性", "desc": "发音自然有磁性，适用哲理故事"},
    {"id": "linbaf_gaoleng", "name": "零八", "label": "零八・高冷", "desc": "推荐有声读物场景"},
    {"id": "linbaf_qingxin", "name": "零八", "label": "零八・清新", "desc": "推荐有声读物场景"},
    {"id": "xiyaof_laoshi", "name": "小妖", "label": "小妖・女老师", "desc": "推荐武侠小说等场景"},
    {"id": "anonyg", "name": "佚佚", "label": "佚佚・成人女声", "desc": "模仿女童音色"},
    {"id": "luyaof", "name": "瑶瑶", "label": "瑶瑶・自然亲切", "desc": "可用于情感电台等场景"},
]

def get_params(text: str, voice_id: str, speed: float, volume: int, audio_type: str):
    # 将用户选择的倍速转换为API参数（倒数关系）
    # 用户选择2.0倍速 -> API需要0.5
    # 用户选择1.0倍速 -> API需要1.0
    # 用户选择0.5倍速 -> API需要2.0
    api_speed = 1.0 / speed if speed != 0 else 1.0
    return {
        "voiceId": voice_id,
        "text": text,
        "speed": api_speed,
        "volume": volume,
        "audioType": audio_type,
    }

def synthesize_once(text: str, voice_id: str, speed: float, volume: int, audio_type: str, max_retries: int = 3, retry_delay: float = 0.5):
    params = get_params(text, voice_id, speed, volume, audio_type)

    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                # 显示重试进度
                st.toast(f"第 {attempt} 次重试中...", icon="🔄")
            r = requests.get(BASE_URL, params=params, timeout=20)
            r.raise_for_status()
            return r.content
        except (requests.HTTPError, requests.Timeout, requests.ConnectionError) as e:
            if attempt == max_retries:
                raise e
            if attempt < max_retries:
                # 显示即将重试信息（等差数列：0.5秒、0.5秒、0.5秒...）
                wait_time = retry_delay
                st.toast(f"请求失败，{wait_time}秒后进行第 {attempt + 1} 次重试...", icon="⏳")
                time.sleep(wait_time)
                continue
        except Exception as e:
            # 对于其他类型的错误，不进行重试
            raise e

def build_url(text: str, voice_id: str, speed: float, volume: int, audio_type: str) -> str:
    qs = urlencode(get_params(text, voice_id, speed, volume, audio_type), safe="")
    return f"{BASE_URL}?{qs}"

def init_state():
    if "history" not in st.session_state:
        st.session_state["history"] = []

def add_history(item):
    st.session_state["history"].insert(0, item)

init_state()

st.title("🎵 TTS语音合成")
st.markdown("**智能语音合成工具** | 支持多种发音人 & 参数自定义")

# 添加一个分割线
st.markdown("---")

with st.sidebar:
    # 顶部标题区域
    st.markdown("### 🎙️ 合成参数")
    st.markdown("---")

    # 发音人选择
    st.markdown("🎭 **发音人选择**")
    labels = [v["label"] for v in VOICES]
    default_index = next((i for i, v in enumerate(VOICES) if v["id"] == "ppangf_csn"), 0)
    selected_label = st.selectbox("选择发音人", labels, index=default_index, label_visibility="collapsed")
    selected_voice = next(v for v in VOICES if v["label"] == selected_label)

    # 显示当前发音人信息
    with st.container():
        st.success(f"**{selected_voice['name']}**\n{selected_voice['desc']}")

    st.markdown("---")

    # 音频参数设置
    st.markdown("⚙️ **音频参数**")
    speed = st.slider("语速倍数", 0.5, 2.0, 1.0, 0.1, help="0.5 = 0.5倍速（更慢），1.0 = 正常语速，2.0 = 2倍速（更快）")
    volume = st.slider("音量", 0, 100, 50, 1)
    audio_type = st.radio("音频格式", ["wav", "mp3"], index=0, horizontal=True)

    st.markdown("---")

    # 重试设置
    st.markdown("🔄 **网络设置**")
    max_retries = st.slider("最大重试次数", 0, 5, 3, 1)
    retry_delay = st.slider("重试延迟(秒)", 0.5, 5.0, 0.5, 0.5)

    st.markdown("---")

    # 文本限制提示
    st.info("📝 **文本限制**: 不超过 200 字")

# 主要操作区域
col_input, col_info = st.columns([3, 1])

with col_input:
    text = st.text_area("📝 输入要合成的文本", "您好世界", height=120, label_visibility="collapsed")

with col_info:
    st.markdown("#### 📊 文本信息")
    st.markdown(f"**字数统计:** `{len(text)}/200`")

    # 紧凑的使用提示
    st.caption("💡 单条直接输入，批量每行一条")

# 操作按钮区域
st.markdown("---")
col_single, col_batch = st.columns([1, 1])

with col_single:
    do_single = st.button("🎵 生成语音", type="primary", use_container_width=True)

with col_batch:
    do_batch = st.button("📦 批量合成", use_container_width=True)

def handle_one(input_text: str):
    if len(input_text) == 0:
        st.error("文本不能为空")
        return
    if len(input_text) > 200:
        st.error("文本不超过 200 字")
        return
    try:
        # 创建进度占位符
        progress_placeholder = st.empty()

        with progress_placeholder.container():
            if max_retries > 0:
                st.info(f"合成中...（最多重试 {max_retries} 次）")
            else:
                st.info("合成中...")

        audio_bytes = synthesize_once(input_text, selected_voice["id"], speed, volume, audio_type, max_retries, retry_delay)

        # 清除进度显示
        progress_placeholder.empty()

        url = build_url(input_text, selected_voice["id"], speed, volume, audio_type)

        # 成功提示
        st.success("🎉 语音合成成功！")

        # 结果展示区域
        st.markdown("---")
        col_audio, col_params, col_download = st.columns([2, 2, 1])

        with col_audio:
            st.markdown("### 🎵 音频播放")
            st.audio(audio_bytes, format=f"audio/{audio_type}")

        with col_params:
            st.markdown("### ⚙️ 合成参数")
            speed_desc = f"{speed:.1f}倍速"
            api_speed = 1.0 / speed if speed != 0 else 1.0
            st.markdown(f"""
            **发音人**: {selected_voice['name']} ({selected_voice['label']})
            **语速**: {speed_desc} (API: {api_speed})
            **音量**: {volume}%
            **格式**: {audio_type.upper()}
            **文本**: {input_text[:30]}{'...' if len(input_text) > 30 else ''}
            """)

        with col_download:
            st.markdown("### 💾 下载")
            st.download_button(
                "📥 下载音频",
                audio_bytes,
                file_name=f"tts_{int(time.time())}.{audio_type}",
                mime=f"audio/{audio_type}",
                use_container_width=True
            )
        add_history({
            "text": input_text,
            "voiceId": selected_voice["id"],
            "name": selected_voice["name"],
            "label": selected_voice["label"],
            "desc": selected_voice["desc"],
            "speed": speed,
            "volume": volume,
            "audioType": audio_type,
            "url": url,
            "bytes": audio_bytes,
            "ts": int(time.time()),
        })
    except requests.HTTPError as e:
        progress_placeholder.empty()
        code = e.response.status_code if e.response is not None else "HTTPError"
        st.error(f"请求失败：{code}（已重试{max_retries}次）")
    except requests.Timeout:
        progress_placeholder.empty()
        st.error(f"请求超时（已重试{max_retries}次），请检查网络连接")
    except requests.ConnectionError:
        progress_placeholder.empty()
        st.error(f"网络连接失败（已重试{max_retries}次），请检查网络设置")
    except Exception as e:
        progress_placeholder.empty()
        st.error(f"发生错误：{e}")

if do_single:
    handle_one(text)

if do_batch:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        st.error("批量模式：请输入多行文本，每行一条")
    else:
        for idx, ln in enumerate(lines, start=1):
            st.write(f"第 {idx} 条：{ln}")
            handle_one(ln)

# 历史记录区域
st.markdown("---")
st.markdown("## 📚 历史记录")

if st.session_state["history"]:
    for i, item in enumerate(st.session_state["history"], start=1):
        speed_desc = f"{item['speed']:.1f}倍速"
        with st.expander(f"🎵 #{i} {item['label']} | {item['audioType'].upper()} | 语速{speed_desc} | {item['text'][:20]}..."):
            col_play, col_download = st.columns([2, 1])

            with col_play:
                st.audio(item["bytes"], format=f"audio/{item['audioType']}")

            with col_download:
                st.markdown("**操作**")
                st.download_button(
                    "📥 下载",
                    item["bytes"],
                    file_name=f"tts_{item['ts']}.{item['audioType']}",
                    mime=f"audio/{item['audioType']}",
                    use_container_width=True
                )

                # 显示详细信息
                st.markdown("**详细信息**")
                st.markdown(f"""
                **文本**: {item['text']}
                **音量**: {item['volume']}%
                **时间**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['ts']))}
                """)
else:
    st.info("📝 暂无历史记录，开始合成您的第一条语音吧！")

# 发音人列表区域
st.markdown("---")
st.markdown("## 🎭 发音人完整列表")

# 使用三列卡片式布局展示发音人
for i in range(0, len(VOICES), 3):
    col1, col2, col3 = st.columns(3)

    # 第一列卡片
    with col1:
        if i < len(VOICES):
            voice = VOICES[i]
            st.info(f"""
**🎙️ {voice['name']}**
`{voice['id']}`

{voice['desc']}

💡 **推荐场景**: {voice['label']}
""")

    # 第二列卡片
    with col2:
        if i + 1 < len(VOICES):
            voice = VOICES[i + 1]
            st.info(f"""
**🎙️ {voice['name']}**
`{voice['id']}`

{voice['desc']}

💡 **推荐场景**: {voice['label']}
""")

    # 第三列卡片
    with col3:
        if i + 2 < len(VOICES):
            voice = VOICES[i + 2]
            st.info(f"""
**🎙️ {voice['name']}**
`{voice['id']}`

{voice['desc']}

💡 **推荐场景**: {voice['label']}
""")

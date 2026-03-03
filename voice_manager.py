# voice_manager.py
# 声音复刻（上传音频）和声音设计（文字描述）两种方式创建音色
# 以及查询、删除音色

import os
import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService

import config

# 设置 API Key 和 WebSocket URL
dashscope.api_key = config.DASHSCOPE_API_KEY
dashscope.base_websocket_api_url = config.DASHSCOPE_WEBSOCKET_URL


def create_voice_from_audio(audio_url: str, prefix: str = config.VOICE_PREFIX,
                             language: str = "zh") -> str:
    """
    方式一：声音复刻 —— 上传一段参考音频，复刻出一个新音色。

    Args:
        audio_url: 参考音频的公网可访问 URL（WAV/MP3/M4A，10~20秒，≤10MB，采样率≥16kHz）
        prefix:    音色名称前缀（字母数字下划线，≤10字符）
        language:  参考音频的语言提示，zh / en / ja / ko / fr / de / ru 等

    Returns:
        voice_id: 生成的音色 ID，直接用于 TTS 的 voice 参数
    """
    service = VoiceEnrollmentService()
    voice_id = service.create_voice(
        target_model=config.TARGET_MODEL,
        prefix=prefix,
        url=audio_url,
        language_hints=[language],
    )
    print(f"[声音复刻] Request ID: {service.get_last_request_id()}")
    print(f"[声音复刻] Voice ID: {voice_id}")
    return voice_id


def create_voice_from_text(voice_prompt: str, prefix: str = config.VOICE_PREFIX,
                            preview_text: str = "你好，很高兴认识你。") -> str:
    """
    方式二：声音设计 —— 用文字描述生成一个全新音色（无需参考音频）。
    注意：声音设计只支持 Python SDK 通过 RESTful API 调用，不支持老版 DashScope SDK。
    本函数使用 VoiceEnrollmentService，SDK >= 1.23.4 支持。

    Args:
        voice_prompt: 声音描述文本（≤500字符，中文或英文）
                      示例："沉稳的中年男性，语速缓慢，音色低沉有磁性，适合朗读新闻"
        prefix:       音色名称前缀
        preview_text: 试听文本（可选）

    Returns:
        voice_id: 生成的音色 ID
    """
    service = VoiceEnrollmentService()
    # 声音设计通过 create_voice 的 voice_prompt 参数触发
    # url 传空字符串（声音设计不需要参考音频）
    voice_id = service.create_voice(
        target_model=config.TARGET_MODEL,
        prefix=prefix,
        url="",                    # 声音设计不需要音频 URL
        voice_prompt=voice_prompt,
        preview_text=preview_text,
    )
    print(f"[声音设计] Request ID: {service.get_last_request_id()}")
    print(f"[声音设计] Voice ID: {voice_id}")
    return voice_id


def list_all_voices(prefix: str = None, page_size: int = 20) -> list:
    """
    查询账号下已有的所有音色列表。

    Args:
        prefix:    按前缀筛选（传 None 查全部）
        page_size: 每页数量

    Returns:
        list of dict，每条包含 voice_id / status / gmt_create / gmt_modified
    """
    service = VoiceEnrollmentService()
    voices = service.list_voices(prefix=prefix, page_index=0, page_size=page_size)
    print(f"[查询音色] 共找到 {len(voices)} 个音色")
    for v in voices:
        print(f"  - {v.get('voice_id')}  状态: {v.get('status')}  创建: {v.get('gmt_create')}")
    return voices


def query_voice(voice_id: str) -> dict:
    """查询单个音色详细信息"""
    service = VoiceEnrollmentService()
    detail = service.query_voice(voice_id=voice_id)
    print(f"[查询音色] {voice_id}: {detail}")
    return detail


def wait_voice_ready(voice_id: str, max_wait_sec: int = 60, interval_sec: int = 5) -> bool:
    """
    等待音色审核通过（状态变为 OK）。
    声音复刻/设计创建后需要审核，通常几秒到几十秒。

    Returns:
        True: 审核通过，False: 超时或审核不通过
    """
    import time
    print(f"[等待音色] 等待 {voice_id} 审核通过...")
    for _ in range(max_wait_sec // interval_sec):
        detail = query_voice(voice_id)
        status = detail.get("status", "")
        if status == "OK":
            print(f"[等待音色] 审核通过！")
            return True
        elif status == "UNDEPLOYED":
            print(f"[等待音色] 审核不通过，请检查音频质量或描述文本。")
            return False
        print(f"[等待音色] 当前状态: {status}，继续等待...")
        time.sleep(interval_sec)
    print(f"[等待音色] 超时，最后状态未变为 OK。")
    return False


def delete_voice(voice_id: str):
    """删除一个音色（不可逆，释放配额）"""
    service = VoiceEnrollmentService()
    service.delete_voice(voice_id=voice_id)
    print(f"[删除音色] {voice_id} 已提交删除。Request ID: {service.get_last_request_id()}")


if __name__ == "__main__":
    # 快速测试：查询当前所有音色
    list_all_voices()

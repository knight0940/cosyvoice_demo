# tts.py
# 使用 CosyVoice Python SDK 进行语音合成（非流式，适合批量生成 demo）

import os
from pathlib import Path

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat

import config

dashscope.api_key = config.DASHSCOPE_API_KEY
dashscope.base_websocket_api_url = config.DASHSCOPE_WEBSOCKET_URL


def synthesize(
    text: str,
    voice_id: str,
    output_path: str,
    model: str = config.TARGET_MODEL,
    audio_format: AudioFormat = AudioFormat.WAV_24000HZ_MONO_16BIT,
    speech_rate: float = 1.0,
    volume: int = 50,
    instruction: str = None,
) -> str:
    """
    语音合成（非流式调用），将文本合成为音频文件并保存。

    Args:
        text:         待合成文本（≤20000字符）
        voice_id:     音色 ID（系统音色名 或 声音复刻/设计的 voice_id）
        output_path:  输出音频文件路径，e.g. "outputs/demo1.wav"
        model:        语音合成模型，必须与创建音色时的 target_model 一致
        audio_format: 音频格式，默认 WAV 24kHz
        speech_rate:  语速，0.5~2.0，默认 1.0
        volume:       音量，0~100，默认 50
        instruction:  情绪/风格指令（自然语言），如"用非常激昂的语气说话"
                      仅 cosyvoice-v3.5-plus/flash 和 cosyvoice-v3-flash 复刻音色支持

    Returns:
        output_path（保存路径）
    """
    # 每次调用前需重新初始化（文档要求）
    kwargs = dict(
        model=model,
        voice=voice_id,
        format=audio_format,
        speech_rate=speech_rate,
        volume=volume,
    )
    if instruction:
        kwargs["instruction"] = instruction

    synthesizer = SpeechSynthesizer(**kwargs)
    audio_bytes = synthesizer.call(text)

    request_id = synthesizer.get_last_request_id()
    first_delay = synthesizer.get_first_package_delay()
    print(f"[TTS] Request ID: {request_id}  首包延迟: {first_delay}ms")

    if audio_bytes is None:
        resp = synthesizer.get_response()
        raise RuntimeError(f"合成失败，服务端返回: {resp}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    print(f"[TTS] 已保存: {output_path}  ({len(audio_bytes)} bytes)")
    return output_path


if __name__ == "__main__":
    # 快速测试：用 cosyvoice-v3-flash 系统音色跑一条
    # 如果你还没有复刻音色，先用系统音色验证链路是否跑通
    test_model = "cosyvoice-v3-flash"
    test_voice = "longanyang"   # cosyvoice-v3-flash 系统音色

    import dashscope as ds
    ds.api_key = config.DASHSCOPE_API_KEY
    ds.base_websocket_api_url = config.DASHSCOPE_WEBSOCKET_URL

    synthesize(
        text="这是一次语音合成测试，链路跑通了！",
        voice_id=test_voice,
        output_path="outputs/test_system_voice.wav",
        model=test_model,
    )
    print("测试完成，请播放 outputs/test_system_voice.wav 确认效果。")

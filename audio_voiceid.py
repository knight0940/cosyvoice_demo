from voice_manager import create_voice_from_audio, wait_voice_ready

voice_id = create_voice_from_audio(
    audio_url="https://你的音频公网链接.wav",  # 10~20秒，清晰无噪音
    prefix="mydemo"
)
wait_voice_ready(voice_id)
print("可以用的 voice_id:", voice_id)

from voice_manager import create_voice_from_audio, wait_voice_ready

voice_id = create_voice_from_audio(
    audio_url="https://drive.google.com/uc?export=download&id=1dKc7olhlZew250UriplhHBsC1eGAm2X6",  # 10~20秒，清晰无噪音
    prefix="mydemo"
)
wait_voice_ready(voice_id)
print("可以用的 voice_id:", voice_id)

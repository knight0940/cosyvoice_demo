from tts import synthesize

voice_id = "cosyvoice-v3.5-plus-mydemo-9effc6039d7046eda418b47ce8899b43"

# 几条不同风格的台词，展示情绪控制能力
lines = [
    ("cool",     "ライブのことは任せといて。別に大したことじゃないし。",       "用慵懒随性、略带自信的语气说话"),
    ("greeting", "おはよう！今日もよろしくね。",                             None),
    ("thanks",   "ありがとう、助かったよ。本当に。",                         "语气温柔真诚，带着一点不好意思的感谢"),
    ("serious",  "音楽のことは、本気だから。",                              "语气沉静而坚定，透出一种不容置疑的认真感"),
]


for tag, text, instruction in lines:
    synthesize(
        text=text,
        voice_id=voice_id,
        output_path=f"outputs/ryou_{tag}.wav",
        instruction=instruction,
    )

print("全部生成完毕，请播放 outputs/ 目录下的文件。")

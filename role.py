from tts import synthesize

voice_id = "cosyvoice-v3.5-plus-vd-mydemo-2cf5d9f233bc49a196a3d410d03168a3"

# 几条不同风格的台词，展示情绪控制能力
lines = [
    ("casual",   "今天练习顺利吗？我感觉状态还不错呢。",          None),
    ("excited",  "哇，真的吗！那个新歌我也很喜欢！",              "用非常兴奋开心的语气说话，带着藏不住的笑意"),
    ("cool",     "演出的事交给我就行了，没什么大不了的。",         "用慵懒随性、略带自信的语气说话"),
    ("serious",  "音乐这件事，我是认真的。",                      "语气沉静而坚定，透出一种不容置疑的认真感"),
]

for tag, text, instruction in lines:
    synthesize(
        text=text,
        voice_id=voice_id,
        output_path=f"outputs/ryou_{tag}.wav",
        instruction=instruction,
    )

print("全部生成完毕，请播放 outputs/ 目录下的文件。")

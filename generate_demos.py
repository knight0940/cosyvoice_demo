# generate_demos.py
# 一键批量生成所有 demo 音频。
#
# 使用方式：
#   Step 1: 在 ROLES 里定义你的角色（voice_id 从 voice_manager.py 创建后填入）
#   Step 2: 在 SCRIPTS 里定义台词（可以按角色分，也可以公用）
#   Step 3: 运行：python generate_demos.py
#   Step 4: 查看 outputs/ 目录下的音频文件

from pathlib import Path
from tts import synthesize
from dashscope.audio.tts_v2 import AudioFormat
import config

# ============================================================
# 角色定义
# voice_id：运行 voice_manager.py 创建音色后填入实际 ID
#           格式类似：cosyvoice-v3.5-plus-mydemo-xxxxxxxx
#
# instruction：用自然语言控制情绪/风格（≤100字符）
#              cosyvoice-v3.5-plus/flash 支持任意指令
#
# 如果你还没有复刻音色，可以先用 cosyvoice-v3-flash 的系统音色测试整条链路：
#   model="cosyvoice-v3-flash", voice_id="longanyang" (男)
#   model="cosyvoice-v3-flash", voice_id="longxiaochun" (女)
# 

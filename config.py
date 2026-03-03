# config.py
import os

# ============================================================
# 从百炼控制台获取 API Key：
# https://bailian.console.aliyun.com/?tab=model#/api-key
# 强烈建议用环境变量，不要硬编码。
# 在终端执行：export DASHSCOPE_API_KEY="sk-xxx"
# ============================================================
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "YOUR_API_KEY_HERE")

# ============================================================
# 地域说明（重要！）
# - cosyvoice-v3.5-plus / v3.5-flash：只能用北京地域
#   WebSocket URL：wss://dashscope.aliyuncs.com/api-ws/v1/inference
# - 其他 cosyvoice-v3-plus/flash/v2/v1：北京和新加坡都可以
#   新加坡 URL：wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference
# ============================================================
DASHSCOPE_WEBSOCKET_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"

# ============================================================
# 使用哪个模型做声音复刻/设计，以及后续 TTS。
# 必须保持一致！复刻用哪个模型，合成也必须用同一个。
#
# 推荐选择：
#   cosyvoice-v3.5-plus  → 支持声音复刻+声音设计，效果最好，仅北京地域
#   cosyvoice-v3-flash   → 支持声音复刻+声音设计，价格低，速度快
# ============================================================
TARGET_MODEL = "cosyvoice-v3.5-plus"

# 音色 prefix（只允许字母数字下划线，不超过10字符）
VOICE_PREFIX = "mydemo"

# 输出音频目录
OUTPUT_DIR = "outputs"

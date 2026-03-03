# CosyVoice Demo

基于阿里云 CosyVoice 的语音合成（TTS）示例项目，支持声音复刻、声音设计和高质量语音合成。

## 功能特性

- **声音复刻**：上传参考音频，复刻目标音色
- **声音设计**：通过文字描述生成全新音色
- **语音合成**：支持情绪/风格指令的自然语音生成
- **批量生成**：支持多角色、多台词的批量音频生成

## 项目结构

```
cosyvoice_demo/
├── config.py              # 配置文件（API Key、模型选择等）
├── tts.py                 # 语音合成核心功能
├── voice_manager.py       # 声音复刻/设计、查询、删除管理
├── role.py               # 单角色多台词生成示例
├── text_voiceid.py       # 声音设计创建音色示例
├── generate_demos.py     # 批量音频生成工具
├── outputs/              # 生成音频的输出目录
└── README.md
```

## 快速开始

### 1. 安装依赖

使用 [uv](https://github.com/astral-sh/uv) 安装依赖：

```bash
uv sync
```

### 2. 配置 API Key

从[阿里云百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 API Key，然后设置环境变量：

```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

### 3. 运行测试

```bash
# 测试系统音色（无需复刻）
python tts.py

# 查询已有音色
python voice_manager.py
```

## 使用指南

### 创建自定义音色

#### 方式一：声音复刻（需参考音频）

```python
from voice_manager import create_voice_from_audio, wait_voice_ready

voice_id = create_voice_from_audio(
    audio_url="https://your-domain.com/reference.wav",
    prefix="mydemo",
    language="zh"
)
wait_voice_ready(voice_id)
```

#### 方式二：声音设计（文字描述）

```python
from voice_manager import create_voice_from_text, wait_voice_ready

voice_id = create_voice_from_text(
    voice_prompt="沉稳的中年男性，语速缓慢，音色低沉有磁性，适合朗读新闻",
    prefix="mydemo"
)
wait_voice_ready(voice_id)
```

### 语音合成

```python
from tts import synthesize

synthesize(
    text="你好，这是一段测试文本。",
    voice_id="cosyvoice-v3.5-plus-mydemo-xxxxxxxx",
    output_path="outputs/demo.wav",
    instruction="用非常激昂的语气说话"  # 可选：情绪指令
)
```

### 批量生成

参见 [role.py](role.py) 和 [generate_demos.py](generate_demos.py) 的示例代码。

## 配置说明

编辑 [config.py](config.py) 自定义以下配置：

| 配置项 | 说明 | 推荐值 |
|--------|------|--------|
| `TARGET_MODEL` | TTS 模型 | `cosyvoice-v3.5-plus`（最佳效果）或 `cosyvoice-v3-flash`（经济实惠） |
| `VOICE_PREFIX` | 音色名称前缀 | 字母数字下划线，≤10字符 |
| `DASHSCOPE_WEBSOCKET_URL` | 服务端点 | 北京地域或新加坡地域 |

## 支持的模型

| 模型 | 特性 | 地域 |
|------|------|------|
| cosyvoice-v3.5-plus | 声音复刻+设计，最佳效果 | 北京 |
| cosyvoice-v3.5-flash | 声音复刻+设计，快速经济 | 北京 |
| cosyvoice-v3-flash | 声音复刻+设计 | 北京/新加坡 |

## 注意事项

1. **模型一致性**：声音复刻/设计使用的模型必须与 TTS 合成时使用的模型一致
2. **音频要求**：参考音频需 10~20 秒，≤10MB，采样率≥16kHz，WAV/MP3/M4A 格式
3. **情绪指令**：仅 cosyvoice-v3.5-plus/flash 复刻音色支持 `instruction` 参数
4. **审核时间**：声音复刻/设计创建后需等待审核通过（通常几秒到几十秒）

## API 参考文档

- [CosyVoice 官方文档](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-voice-cloning-basic)
- [DashScope Python SDK](https://github.com/aliyun/dashscope)

## 许可证

MIT License

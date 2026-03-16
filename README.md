# 模型格式转换工具 (safetensors ↔ Diffusers)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个基于 Gradio 的图形界面工具，用于在 **safetensors 单文件**与 **Diffusers 文件夹**之间转换完整模型和 LoRA 权重。支持 SD1.x/2.x 和 SDXL 架构，操作简单，无需编写代码。
此项目完全又ai创作，可能会出现意想不到的问题


## ✨ 功能特性

- ✅ **大模型转换**：支持 safetensors ↔ Diffusers 双向转换。
- ✅ **LoRA 转换**：支持 LoRA 权重双向转换。
- ✅ **多种架构**：兼容 SD1.x、SD2.x 和 SDXL。
- ✅ **半精度支持**：可选择保存为 float16 节省空间。
- ✅ **友好界面**：基于 Gradio 的 Web UI，自动打开浏览器。
- ✅ **离线模式**：除首次获取配置外，转换过程完全离线（可配置代理）。
- ✅ **一键启动**：附赠批处理脚本，双击即可运行。

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/模型转换工具.git
cd 模型转换工具
```

### 2. 创建虚拟环境（推荐）
```bash
# 使用 venv
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 启动工具
- **Windows**：双击 `启动工具.bat`。
- **其他系统**：在终端中运行：
  ```bash
  python main.py
  ```

程序会自动打开浏览器，访问 `http://127.0.0.1:9524` 即可使用。

## 📖 使用指南

### 大模型转换
| 方向 | 操作 |
|------|------|
| safetensors → Diffusers | 选择转换类型为“大模型”，方向为“safetensors → Diffusers”，填写输入文件路径（`.safetensors`）和输出文件夹路径。首次运行需要联网下载模型配置，请确保代理已开启（见常见问题）。 |
| Diffusers → safetensors | 选择方向为“Diffusers → safetensors”，输入 Diffusers 文件夹路径，输出文件路径（`.safetensors`）。完全离线。 |

### LoRA 转换
| 方向 | 操作 |
|------|------|
| safetensors LoRA → Diffusers | 选择“LoRA”，方向为“safetensors → Diffusers”，填写基础模型路径（本地 Diffusers 格式文件夹）、输入 LoRA 文件路径（`.safetensors`）和输出文件夹。 |
| Diffusers LoRA → safetensors | 选择“LoRA”，方向为“Diffusers → safetensors”，输入 Diffusers 文件夹路径（其中包含 `pytorch_lora_weights.safetensors`），输出文件路径。 |

### 参数说明
- **模型架构**：仅大模型需要选择，根据你的模型选择 sd1/sd2/sdxl。
- **半精度**：勾选后保存为 float16，文件体积减半。
- **输入/输出路径**：使用绝对路径或相对路径均可。

## ❓ 常见问题

### Q1: 为什么转换大模型 safetensors → Diffusers 时报网络错误？
首次转换时需要从 Hugging Face 下载模型配置文件。请确保：
- 网络通畅（可以访问 huggingface.co）。
- 如果使用代理，请在 `main.py` 开头取消注释并设置正确的代理地址（例如 `os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'`）。
- 或者先手动下载缓存配置（如运行 `from diffusers import StableDiffusionXLPipeline; StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")`）。

### Q2: 端口 9524 被占用了怎么办？
- 修改 `main.py` 最后一行 `server_port` 为其他端口（如 9525）。
- 同时可以修改 `启动工具.bat` 中的提示文字（非必需）。

### Q3: 如何获取基础模型路径（用于 LoRA 转换）？
你需要一个完整的 Diffusers 格式的模型文件夹（例如从官方下载的 `stable-diffusion-xl-base-1.0`）。如果只有 safetensors 文件，可以先使用本工具的“大模型转换”将其转为 Diffusers 格式。

### Q4: 为什么我的 LoRA 转换后文件变大了？
LoRA 转换保存的是完整 pipeline（包含基础模型 + LoRA），所以文件夹较大。如果你只需要 LoRA 权重，可以在 Diffusers 文件夹中找到 `pytorch_lora_weights.safetensors` 文件，它就是 LoRA 权重。

## 🤝 贡献指南
欢迎贡献代码或提出建议！请遵循以下步骤：
1. Fork 本仓库。
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 打开一个 Pull Request。

## 📄 许可证
本项目采用 MIT 许可证。详情请参见 [LICENSE](LICENSE) 文件。

---

**如果你觉得这个工具有用，请给一个 ⭐️ 支持！**
```

如果仍有部分缺失，请告诉我具体是哪一段没有显示完整，我可以单独提供该部分。

import gradio as gr
import os
import shutil
import json
from diffusers import StableDiffusionXLPipeline, StableDiffusionPipeline
import torch

# 如需代理请取消下面两行的注释并修改地址
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def convert_full_model(input_path, output_path, model_type, direction, half):
    log = []
    try:
        if direction == "s2d":
            log.append(f"加载 safetensors 模型: {input_path}")
            if not input_path.endswith('.safetensors'):
                return "错误：输入文件必须是 .safetensors 格式", log

            pipeline_class = StableDiffusionXLPipeline if model_type == 'sdxl' else StableDiffusionPipeline
            dtype = torch.float16 if half else torch.float32
            pipe = pipeline_class.from_single_file(input_path, torch_dtype=dtype, use_safetensors=True)
            log.append("模型加载成功，正在保存为 Diffusers 格式...")
            pipe.save_pretrained(output_path, safe_serialization=True)
            log.append(f"转换完成！Diffusers 文件夹已保存至: {output_path}")

        else:
            log.append(f"加载 Diffusers 模型: {input_path}")
            pipeline_class = StableDiffusionXLPipeline if model_type == 'sdxl' else StableDiffusionPipeline
            dtype = torch.float16 if half else torch.float32
            pipe = pipeline_class.from_pretrained(input_path, torch_dtype=dtype, use_safetensors=True, local_files_only=True)
            log.append("模型加载成功，正在保存为 safetensors 单文件...")
            pipe.to_single_file(output_path, save_config=True, safe_serialization=True)
            log.append(f"转换完成！safetensors 文件已保存至: {output_path}")

        return "转换成功", log
    except Exception as e:
        return f"转换失败：{str(e)}", log

def convert_lora(input_path, output_path, base_model_path, direction, half):
    log = []
    try:
        if direction == "s2d":
            log.append("LoRA 转换：safetensors → Diffusers")
            if not input_path.endswith('.safetensors'):
                return "错误：LoRA 文件必须是 .safetensors 格式", log
            if not base_model_path:
                return "错误：转换 LoRA 到 Diffusers 需要提供基础模型路径", log

            index_path = os.path.join(base_model_path, "model_index.json")
            if not os.path.exists(index_path):
                return f"错误：基础模型路径 '{base_model_path}' 不是有效的 Diffusers 格式", log

            with open(index_path, 'r', encoding='utf-8') as f:
                model_index = json.load(f)
            pipeline_class = StableDiffusionXLPipeline if "StableDiffusionXLPipeline" in model_index.get("_class_name", "") else StableDiffusionPipeline

            dtype = torch.float16 if half else torch.float32
            log.append(f"加载基础模型: {base_model_path}")
            pipe = pipeline_class.from_pretrained(base_model_path, torch_dtype=dtype, use_safetensors=True, local_files_only=True)

            log.append(f"加载 LoRA 权重: {input_path}")
            pipe.load_lora_weights(input_path)

            os.makedirs(output_path, exist_ok=True)
            pipe.save_pretrained(output_path, safe_serialization=True)
            log.append(f"转换完成！Diffusers LoRA 已保存至: {output_path}")

        else:
            log.append("LoRA 转换：Diffusers → safetensors")
            lora_file = os.path.join(input_path, "pytorch_lora_weights.safetensors")
            if not os.path.exists(lora_file):
                files = [f for f in os.listdir(input_path) if f.endswith('.safetensors')]
                if not files:
                    return "错误：未在 Diffusers 文件夹中找到 LoRA 权重文件", log
                lora_file = os.path.join(input_path, files[0])
                log.append(f"找到权重文件: {files[0]}")
            shutil.copy2(lora_file, output_path)
            log.append(f"已复制 LoRA 权重至: {output_path}")

        return "转换成功", log
    except Exception as e:
        return f"转换失败：{str(e)}", log

def create_ui():
    with gr.Blocks(title="模型格式转换工具") as demo:
        gr.Markdown("# 🧠 模型格式转换工具（safetensors ↔ Diffusers）")

        with gr.Row():
            with gr.Column(scale=1):
                convert_type = gr.Radio(
                    choices=["大模型 (Full Model)", "LoRA"],
                    label="转换类型",
                    value="大模型 (Full Model)"
                )
                direction = gr.Radio(
                    choices=[
                        ("safetensors → Diffusers", "s2d"),
                        ("Diffusers → safetensors", "d2s")
                    ],
                    label="转换方向",
                    value="s2d"
                )
                model_type = gr.Dropdown(
                    choices=["sd1", "sd2", "sdxl"],
                    label="模型架构 (仅大模型)",
                    value="sdxl"
                )
                base_model_path = gr.Textbox(
                    label="基础模型路径 (仅 LoRA s2d 时需要)",
                    placeholder="例如: E:/models/sdxl_base (Diffusers 格式文件夹)"
                )
                input_path = gr.Textbox(
                    label="输入路径",
                    placeholder="safetensors 文件路径 或 Diffusers 文件夹路径"
                )
                output_path = gr.Textbox(
                    label="输出路径",
                    placeholder="转换后保存的路径（文件或文件夹）"
                )
                half = gr.Checkbox(label="保存为 float16 精度", value=True)
                convert_btn = gr.Button("开始转换", variant="primary")

            with gr.Column(scale=1):
                status = gr.Textbox(label="状态", interactive=False)
                log_output = gr.Textbox(label="日志", lines=20, max_lines=30, interactive=False)

        def run_conversion(convert_type, direction, model_type, base_model_path, input_path, output_path, half):
            if not input_path or not output_path:
                return "错误：输入和输出路径不能为空", ""

            if convert_type == "大模型 (Full Model)":
                status, logs = convert_full_model(input_path, output_path, model_type, direction, half)
            else:
                status, logs = convert_lora(input_path, output_path, base_model_path, direction, half)

            log_str = "\n".join(logs) if isinstance(logs, list) else str(logs)
            return status, log_str

        convert_btn.click(
            fn=run_conversion,
            inputs=[convert_type, direction, model_type, base_model_path, input_path, output_path, half],
            outputs=[status, log_output]
        )

    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=9524,
        share=False,
        theme=gr.themes.Soft(),
        inbrowser=True
    )
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from config.config import MODEL_PATH, USE_GPU
from utils.logger import logger

class ModelLoader:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() and USE_GPU else "cpu"
        logger.info(f"使用设备: {self.device}")

    def load_model(self):
        """加载预训练模型和分词器"""
        try:
            logger.info(f"开始加载模型: {MODEL_PATH}")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_PATH,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            logger.info("模型加载成功")
            return True
        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            return False

    def generate_text(self, prompt, max_length=512, temperature=0.7):
        """使用模型生成文本"""
        if not self.model or not self.tokenizer:
            logger.error("模型未加载")
            return None

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True
            )
            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return text
        except Exception as e:
            logger.error(f"文本生成失败: {str(e)}")
            return None

# 单例模式
model_loader = ModelLoader()
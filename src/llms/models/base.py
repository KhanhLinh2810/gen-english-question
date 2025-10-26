import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class Model:
    """Generalized text generation model (compatible with Gemma / GPT-style models)."""

    def __init__(self, model_name: str = "google/gemma-2b-it", device: str = None):
        """
        Load model and tokenizer into memory.

        Args:
            model_name (str): Name or path of the Hugging Face model.
            device (str): 'cpu' or 'cuda'. Defaults to GPU if available.
        """
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        print(f"🔹 Loading model: {model_name} on [{self.device.upper()}] ...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
        ).to(self.device)
        print("✅ Model and tokenizer loaded successfully.\n")

    def tokenize_corpus(self, text: str, max_length: int = 256):
        """Tokenize input text and return tensors."""
        encode = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=max_length,
            truncation=True,
            padding=False,
        )
        return encode["input_ids"].to(self.device), encode["attention_mask"].to(self.device)

    def inference(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_beams: int = 1,
        max_new_tokens: int = 128,
        token_max_length: int = 256,
    ):
        """
        Generate text from a given prompt.

        Args:
            prompt (str): Input text for the model.
            temperature (float): Sampling temperature (higher = more creative).
            top_p (float): Nucleus sampling parameter.
            num_beams (int): Number of beams (set 1 for sampling).
            max_new_tokens (int): Maximum number of tokens to generate.
            token_max_length (int): Max length for tokenization.
        """
        input_ids, attention_mask = self.tokenize_corpus(prompt, token_max_length)

        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                do_sample=True if num_beams == 1 else False,
                temperature=temperature,
                top_p=top_p,
                num_beams=num_beams,
                max_new_tokens=max_new_tokens,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded.strip()

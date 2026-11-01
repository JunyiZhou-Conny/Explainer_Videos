# B5 and C8: Qwen3-0.6B's shapes (nb cell 42's config) built on PyTorch's "meta" device (shapes only, no weights,
# no download, no GPU), then the notebook's LoraConfig (nb cell 67) applied by PEFT 0.20.0.
import torch, warnings
from transformers import Qwen3Config, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
from peft.utils.constants import TRANSFORMERS_MODELS_TO_LORA_TARGET_MODULES_MAPPING as DEFAULTS

cfg = Qwen3Config(vocab_size=151936, hidden_size=1024, intermediate_size=3072, num_hidden_layers=28,
                  num_attention_heads=16, num_key_value_heads=8, head_dim=128, tie_word_embeddings=True)

def fresh():
    with torch.device("meta"):
        return AutoModelForCausalLM.from_config(cfg)

def count(model):
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    return trainable, total

base = fresh()
print("PEFT default target modules for qwen3:", DEFAULTS["qwen3"])
print("parameters as downloaded:", f"{count(base)[1]:,}")
by_kind = {"Linear": 0, "Embedding": 0, "Qwen3RMSNorm": 0}
for m in base.modules():
    if type(m).__name__ in by_kind:
        by_kind[type(m).__name__] += sum(p.numel() for p in m.parameters(recurse=False))
print("by kind (lm_head shares the embedding):", {k: f"{v:,}" for k, v in by_kind.items()})

for label, kw in [("nb cell 67 (r=8, no target_modules)", {}),
                  ("r=16", {"r": 16}),
                  ("target_modules='all-linear'", {"target_modules": "all-linear"})]:
    args = dict(lora_alpha=16, lora_dropout=0.1, r=8, bias="none", task_type="CAUSAL_LM")
    args.update(kw)
    model = get_peft_model(fresh(), LoraConfig(**args))
    t, a = count(model)
    names = sorted({n.split(".")[-1] for n, m in model.named_modules() if hasattr(m, "lora_A")})
    print(f"{label}: trainable {t:,} of {a:,}; adapted: {names}")

# C8: inject a second time into the same model, as re-running the trainer cell after editing 4.1 does.
m = fresh()
get_peft_model(m, LoraConfig(lora_alpha=16, lora_dropout=0.1, r=8, bias="none", task_type="CAUSAL_LM"))
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    get_peft_model(m, LoraConfig(lora_alpha=16, lora_dropout=0.1, r=16, bias="none", task_type="CAUSAL_LM"))
for x in w:
    print("warning:", str(x.message).splitlines()[0][:160])

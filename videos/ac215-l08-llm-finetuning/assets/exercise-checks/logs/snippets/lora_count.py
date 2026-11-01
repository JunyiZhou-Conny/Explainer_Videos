# Q5 / B5: count LoRA parameters by hand from Qwen3-0.6B's shapes (nb cell 42's config).
hidden, heads, kv_heads, head_dim, inter, layers, vocab = 1024, 16, 8, 128, 3072, 28, 151936
shapes = {  # (in, out) of each linear layer in one block
    "q_proj": (hidden, heads * head_dim), "k_proj": (hidden, kv_heads * head_dim),
    "v_proj": (hidden, kv_heads * head_dim), "o_proj": (heads * head_dim, hidden),
    "gate_proj": (hidden, inter), "up_proj": (hidden, inter), "down_proj": (inter, hidden),
}
def lora(r, names):  # A is r x in, B is out x r
    return layers * sum(r * (shapes[n][0] + shapes[n][1]) for n in names)
print("r=8, q+v:      ", f"{lora(8, ['q_proj', 'v_proj']):,}")
print("r=16, q+v:     ", f"{lora(16, ['q_proj', 'v_proj']):,}")
print("r=8, all seven:", f"{lora(8, list(shapes)):,}")
print("r=8, q,k,v,o:  ", f"{lora(8, ['q_proj', 'k_proj', 'v_proj', 'o_proj']):,}")
linear = layers * sum(i * o for i, o in shapes.values())
embed = vocab * hidden                      # tied with lm_head: counted once
norms = layers * (2 * hidden + 2 * head_dim) + hidden   # two RMSNorms per block, q_norm and k_norm, the final norm
print("full model:    ", f"{linear + embed + norms:,}")
print("4-bit count:   ", f"{linear // 2 + embed + norms:,}", "(linear weights packed two per byte)")
print("+ LoRA r=8:    ", f"{linear // 2 + embed + norms + lora(8, ['q_proj', 'v_proj']):,}")

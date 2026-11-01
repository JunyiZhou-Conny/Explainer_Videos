hidden, heads, kv_heads, head_dim, inter, layers = 1024, 16, 8, 128, 3072, 28
shapes = {"q_proj": (hidden, heads * head_dim), "k_proj": (hidden, kv_heads * head_dim),
          "v_proj": (hidden, kv_heads * head_dim), "o_proj": (heads * head_dim, hidden),
          "gate_proj": (hidden, inter), "up_proj": (hidden, inter), "down_proj": (inter, hidden)}
def lora(r, names):  # A is r x in, B is out x r
    return layers * sum(r * (shapes[n][0] + shapes[n][1]) for n in names)
print(f"{lora(16, ['q_proj', 'v_proj']):,}", f"{lora(8, list(shapes)):,}", f"{lora(8, ['q_proj', 'k_proj', 'v_proj', 'o_proj']):,}")

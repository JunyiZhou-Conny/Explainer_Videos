# B6: perplexity from loss, and the step count of the training run.
import math
print("exp(2.6498) =", round(math.exp(2.6498), 2), "  exp(1.3872) =", round(math.exp(1.3872), 2))
print("steps, batch 4:", math.ceil(900 / 4) * 2, "  batch 8:", math.ceil(900 / 8) * 2)
print("adapter file, float32:", round(1146880 * 4 / 1e6, 2), "MB")

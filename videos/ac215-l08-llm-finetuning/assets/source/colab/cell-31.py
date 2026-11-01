# @title
# Check GPU compatibility with bfloat16
major, _ = torch.cuda.get_device_capability()
if major >= 8:
    print("Your GPU supports bfloat16. This notebook still trains in float16, so the same settings also work on T4 GPUs.")
else:
    print("Your GPU does not support bfloat16. This notebook trains in float16, which works on this GPU.")
## <font color ='#16AD04'>**Step 1: Load the Quantized Model** </font>

### <font color ='#0376B9'>**1.1 Check GPU Compatibility** </font>

Some GPUs have hardware accelerated bfloat16 computation. Modern GPUs (NVIDIA Ampere series and newer, compute capability ≥ 8.0) have specialized hardware to accelerate calculations using bfloat16. Let's check if our GPU supports this:


Note: For this tutorial we will be using float16 because some GPUs, like the T4, do not have accelerated support for bfloat16, ensuring broader compatibility for all users.
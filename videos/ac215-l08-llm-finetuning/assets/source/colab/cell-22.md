Now, let's test how this works.

1. For any given `text`, and a device (`cuda:0`),
2. We tokenize the text, returning it as a PyTorch tensor (`pt`)
3. Send it to the GPU using the `.to(device)` method.
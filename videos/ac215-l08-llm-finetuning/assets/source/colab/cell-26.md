
#### <font color ='#16AD04'>**2. Testing the model (Generating Text)** </font>


Now for the moment of truth. We've loaded a model with heavily compressed 4-bit weights. Can it still generate coherent text?

Let's perform a simple inference test. We'll pass our tokenized input to the `model.generate()` method and see what comes out. We use the `max_new_tokens` argument to control the length of the response, ensuring it doesn't run on forever.
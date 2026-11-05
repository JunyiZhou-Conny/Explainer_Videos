# recorded: the output the tutorial documents for `python cli.py --predict` against a live SageMaker endpoint.
# Source: dlops-io/model-deployment-aws README.md lines 137-147 @ 077f4db (verbatim, without the code fence). Not captured here: no AWS account.
# Note: 3 numbers per prediction and index 0 = gouda (an older 3-class model); today's release model has 4 outputs and cli.py:42 maps 0 = parmigiano (laptop/43, 47).
$ python cli.py --predict
Predict using endpoint
image_files: ['data/brie-1.jpg', 'data/brie-2.jpg', 'data/gouda-1.jpg', 'data/gouda-2.jpeg', 'data/gruyere-1.jpg']
Image: data/brie-2.jpg
Result: {'predictions': [[0.0887121782, 0.0439011417, 0.867386699]]}
[0.0887121782, 0.0439011417, 0.867386699] 2
Label:    brie 

Image: data/gouda-1.jpg
Result: {'predictions': [[0.986440122, 0.00689249625, 0.0066674049]]}
[0.986440122, 0.00689249625, 0.0066674049] 0
Label:    gouda 

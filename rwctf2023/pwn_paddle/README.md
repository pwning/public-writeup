# Paddle&emsp;<sub><sup>Clone-and-Pwn, 338 points</sup></sub>

_Writeup by [@bluepichu](https://github.com/bluepichu)_

> Flexible to serve ML models, and more.

The problem is simply [one of the example setups for Paddle Serving](https://github.com/PaddlePaddle/Serving/blob/v0.9.0/examples/Pipeline/simple_web_service/web_service.py).  The goal is to read `/flag` off the server.

Pretty early on, I realized that any exploit would almost certainly have to occur before `preprocess` is called, because after that point all of our data is loaded into a numpy array of fixed datatype and size.  Therefore, I worked on tracing back the input to `preprocess` by raising exceptions in the code until I figured out which parts touched our original user input.  Eventually I ended up at [`Operator.unpack_request_package`](https://github.com/PaddlePaddle/Serving/blob/e5d6f23c206c2cba3dae998a517c2cfb8c89e06c/python/pipeline/operator.py#L1763), which is in charge of the initial unpacking of the request that we send the server.  I noticed that, in addition to the `key` and `value` fields that we were already aware of, the request could also contain a `tensors` field, which would be unpacked _even if the target function didn't expect any tensors as input_.  The method in charge of this is [`Operator.proto_tensor_2_numpy`](https://github.com/PaddlePaddle/Serving/blob/e5d6f23c206c2cba3dae998a517c2cfb8c89e06c/python/pipeline/operator.py#L1672), which conveniently allows the user input to specify the element type of the tensor, _and_ [has a case for loading arbitrary bytes as pickles](https://github.com/PaddlePaddle/Serving/blob/e5d6f23c206c2cba3dae998a517c2cfb8c89e06c/python/pipeline/operator.py#L1753)!

After generating a pickle with [Pickora](https://github.com/splitline/Pickora) that simply sends `/flag` to an external address, we put together a [simple request script](./solve.py) to send the pickle to the server, and got the flag.

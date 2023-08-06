import json
from pathlib import Path
from fairscale.nn.model_parallel.initialize import initialize_model_parallel
from llama import ModelArgs, Transformer, Tokenizer, LLaMA
import time
import torch
import logging


logger = logging.getLogger(__name__)


class LLAMAModelAgent():
    def __init__(self, args, max_seq_len=1024, max_batch_size=2):
        ## Setting up DDP
        self.local_rank = int(os.environ.get("LOCAL_RANK", -1))
        self.world_size = int(os.environ.get("WORLD_SIZE", -1))
        
        torch.distributed.init_process_group("nccl")
        initialize_model_parallel(self.world_size)
        torch.cuda.set_device(self.local_rank)

        # seed must be the same in all processes
        torch.manual_seed(1)

        ## Getting model name
        if args.cache_dir:
            ckpt_dir = args.cache_dir +'/'+ args.model
            tokenizer_path=args.cache_dir+'/tokenizer.model'
        else:
            raise Exception('--cache_dir should be the path of downloaded llama models')

        checkpoints = sorted(Path(ckpt_dir).glob("*.pth"))
        assert (
            self.world_size == len(checkpoints)
        ), f"Loading a checkpoint for MP={len(checkpoints)} but world size is {self.world_size}"
        ckpt_path = checkpoints[self.local_rank]

        checkpoint = torch.load(ckpt_path, map_location="cpu")
        with open(Path(ckpt_dir) / "params.json", "r") as f:
            params = json.loads(f.read())

        self.model_args: ModelArgs = ModelArgs(max_seq_len=max_seq_len, max_batch_size=max_batch_size, **params)
        
        tokenizer = Tokenizer(model_path=tokenizer_path)
        self.model_args.vocab_size = tokenizer.n_words

        logger.info(f'Loading model: LLAMA_{args.model}')
        torch.set_default_tensor_type(torch.cuda.HalfTensor)
        self.model = Transformer(self.model_args)
        torch.set_default_tensor_type(torch.FloatTensor)
        self.model.load_state_dict(checkpoint, strict=False)
        logger.info(f'Model Loaded: LLAMA_{args.model}')

        self.generator = LLaMA(self.model, tokenizer)

        self.model_memory_usage()
        self.bechmark()


    def model_memory_usage(self):
        mem_params = sum([param.nelement()*param.element_size() for param in self.model.parameters()])
        mem_bufs = sum([buf.nelement()*buf.element_size() for buf in self.model.buffers()])
        mem = mem_params + mem_bufs\
        
        cache = 2 * 2 * self.model_args.n_layers * self.model_args.max_batch_size * self.model_args.max_seq_len * self.model_args.n_heads * 128

        for i in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if mem < 1024.0:
                break
            mem /= 1024.0

        for i_c in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if cache < 1024.0:
                break
            cache /= 1024.0

        logger.info(f'Memory Used by model: {mem:.{3}f} {i}')
        logger.info(f'Cache Used by model: {cache:.{3}f} {i_c}')

    def bechmark(self, max_length=100, num_iter=30, batch_size=16):
        text = "Explain how babies are born? How to calm them down and why do they cry so much?"
        generate_kwargs={"max_length": max_length}

        logger.info(f'Starting Benchmark')
        start = time.time()
        for _ in range(num_iter):
            responce = self.infer(batch=text, generate_kwargs=generate_kwargs, tokenizer_kwargs={})
        length = len(responce['decoded_text'][0].split(' '))

        end = time.time()
        logger.info(f'Benchmark results: Using single prompt, the model achieves generation speed of {num_iter/(end-start):.{3}f} it/s with generation length of {length}')
        


    def infer(self, batch, generate_kwargs={}, tokenizer_kwargs={}):
        if type(batch) == str:
            batch = [batch]

        predictions = self.generator.generate(batch, **generate_kwargs)

        logger.debug(f"Predicting on {batch}")
        logger.debug(f"Predicted {predictions}")

        return {
            "input_text": batch,
            "decoded_text": predictions
        }

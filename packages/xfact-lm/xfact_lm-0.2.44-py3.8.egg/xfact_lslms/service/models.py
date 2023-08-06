import logging
import os
import time
import torch
from threading import Thread
# Huggingface Imports
from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoModelForMaskedLM
import math
from accelerate import init_empty_weights, infer_auto_device_map

logger = logging.getLogger(__name__)

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def get_device_map(model_name, dtype, mem_gpu0=10):
    # Making a empty shell for Model
    with init_empty_weights():
        config = AutoConfig.from_pretrained(model_name)
        try:
            model = AutoModelForSeq2SeqLM.from_config(config).to(dtype)
        except:
            try:
                model = AutoModelForCausalLM.from_config(config).to(dtype)
            except:
                model = AutoModelForMaskedLM.from_config(config).to(dtype)
    # Getting Configration of Model and System
    num_device = torch.cuda.device_count()
    mem_params = sum([param.nelement()*param.element_size() for param in model.parameters()])

    mem = mem_params
    for i in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if mem < 1024.0:
                break
            mem /= 1024.0
    logger.info(f'Memory Used by model: {mem:.{3}f} {i}')

    if num_device <= 1 or mem_params < 5*1024*1024*1024:
        return 'auto'

    # Genetrating Custom Device Map
    mem_gpuN = math.ceil((mem_params/(1024*1024*1024) - mem_gpu0) / (num_device-1))+1
    mem_map=[str(mem_gpu0)+'GiB', str(mem_gpuN)+'GiB']

    d = {0: mem_map[0]}
    for i in range(1, num_device):
        d[i] = mem_map[1]
    logger.info(f'Memory Map for the model: {d}')

    device_map = infer_auto_device_map(
        model, max_memory=d, dtype=dtype, no_split_module_classes=["BloomBlock", "OPTDecoderLayer", "LLaMADecoderLayer", "T5LayerFF"]
    )
    logger.info(f'Device Map for the model: \n{device_map}')
    # Checking Device Map validity
    for i in d:
        if torch.cuda.get_device_properties(i).total_memory <= d[i]:
            raise Exception('Model cannot fit in given GPU Configuration; CUDA: Out of Memory')
    del model
    return device_map

class LanguageModelAgent():
    def __init__(self, args):
        self.past_key_values = None
        if args.bf16:
            self.dtype = torch.bfloat16
        elif args.fp16:
            self.dtype = torch.float16
        else:
            self.dtype = torch.float32
        if args.multi_gpu:
            device_map = get_device_map(args.model, self.dtype)
        else:
            device_map = None

        model_args = {
            'pretrained_model_name_or_path': args.model,
            'cache_dir': args.cache_dir if args.cache_dir and os.path.exists(args.cache_dir) else None,
            'torch_dtype': self.dtype,
            'device_map': device_map,
        }

        tokenizer_args = {
            'pretrained_model_name_or_path': args.model,
            'cache_dir': args.cache_dir if args.cache_dir and os.path.exists(args.cache_dir) else None,
        }

        logger.info(f'Loading model: {args.model}')
        self.tokenizer = AutoTokenizer.from_pretrained(**tokenizer_args, use_fast="/opt" not in args.model)

        try:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(**model_args)
        except:
            try:
                self.model = AutoModelForCausalLM.from_pretrained(**model_args)
            except:
                self.model = AutoModelForMaskedLM.from_pretrained(**model_args)

        logger.info(f'Model Loaded: {args.model}')
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if not args.multi_gpu:
            self.model.to(self.device)

        self.model.eval()
        self.bechmark()

    ## Need some optimization
    def multi_threading(self, batch, tokenizer_kwargs={}, generate_kwargs={}, num_threads=2):
        outs = {"input_text": [], "decoded_text": []}
        threads = []
        if len(batch) / num_threads < 2:
            raise Exception('Send an appropriate number for Batch and num_threads')
        
        n = math.ceil(len(batch) / num_threads)

        for i in range(0, len(batch), n):
            t = ThreadWithReturnValue(target=self.infer, args=(batch[i: i+n], tokenizer_kwargs, generate_kwargs))
            # add the thread to the list
            threads.append(t)
            # start the thread
            t.start()

        for t in threads:
            outs['input_text'].extend(t.join()['input_text'])
            outs['decoded_text'].extend(t.join()['decoded_text'])

        return outs

    def bechmark(self, max_length=100, num_iter=10, batch_size=16):
        text = "Explain how babies are born? How to calm them down and why do they cry so much?"
        generate_kwargs={"max_length": max_length}

        logger.info(f'Starting Benchmark')
        start = time.time()
        for _ in range(num_iter):
            responce = self.infer(batch=text, generate_kwargs=generate_kwargs, tokenizer_kwargs={})
        length = len(responce['decoded_text'][0].split(' '))
        end = time.time()
        logger.info(f'Benchmark results: Using single prompt, the model achieves generation speed of {num_iter/(end-start):.{3}f} it/s with generation length of {length}')
        
        text = ["Explain how babies are born? How to calm them down and why do they cry so much?"]*batch_size
        start = time.time()
        for _ in range(num_iter):
            responce = self.infer(batch=text, generate_kwargs=generate_kwargs, tokenizer_kwargs={})
        length = len(responce['decoded_text'][0].split(' '))
        end = time.time()
        logger.info(f'Benchmark reults: Using batch size of {batch_size}, the model achieves generation speed of {num_iter/(end-start):.{3}f} it/s with generation length of {length}')

    @torch.inference_mode()
    def infer(self, batch, tokenizer_kwargs, generate_kwargs):
        input_ids = self.tokenizer(batch, return_tensors="pt", **tokenizer_kwargs).to(self.device)
        outs = self.model.generate(**input_ids, **generate_kwargs).cpu()
        predictions = self.tokenizer.batch_decode(outs, skip_special_tokens=True)

        logger.debug(f"Predicting on {batch}")
        logger.debug(f"Predicted {predictions}")

        return {
            "input_text": batch,
            "decoded_text": predictions
        }
    
    @torch.inference_mode()
    def forward(self, inputs):
        
        for key in inputs:
            inputs[key] = torch.tensor(inputs[key], dtype=torch.int, device=self.device)

        outs = self.model(**inputs, past_key_values=self.past_key_values)

        logger.debug(f"Input {inputs}")
        logger.debug(f"Output {outs}")

        responce = {}
        for key in outs:
            if key != 'past_key_values':
                responce[key] = outs[key].tolist()
            else:
                self.past_key_values = outs[key]
            
        return responce
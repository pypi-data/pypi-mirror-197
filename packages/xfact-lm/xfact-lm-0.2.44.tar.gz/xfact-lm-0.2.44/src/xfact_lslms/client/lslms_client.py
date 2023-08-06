import datetime
import os
import uuid
from collections import defaultdict
from itertools import islice
from typing import Iterable, List, Iterator

import pika
import json

from pika import PlainCredentials
from tqdm import tqdm


def lazy_groups_of(iterable: Iterable[str], group_size: int) -> Iterator[List[str]]:
    """
    Takes an iterable and batches the individual instances into lists of the
    specified size. The last list may be smaller if there are instances left over.
    """
    iterator = iter(iterable)
    while True:
        s = list(islice(iterator, group_size))
        if len(s) > 0:
            yield s
        else:
            break
class LSMSClient(object):

    def __init__(self, username=None, password=None, model_name='flan-t5-xxl'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('scheduler.xfact.net',
                                                                       5672,
                                                                       "lm",
                                                                       credentials=PlainCredentials(username=username or os.getenv("AMQ_USERNAME", ""),
                                                                                                    password=password or os.getenv("AMQ_PASSWORD","")),
                                                                       heartbeat=20000))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

        self.queue = model_name

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n, tokenizer_kwargs=None, generate_kwargs=None, timeout=50):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                expiration=str(timeout)+'000',
            ),
            body=json.dumps({
                "batch": n,
                "tokenizer_kwargs": tokenizer_kwargs or {},
                "generate_kwargs": generate_kwargs or {}
            }).encode())

        self.connection.process_data_events(time_limit=timeout)

        if self.response:
            resp =  json.loads(self.response.decode('utf-8'))
            if 'error' in resp:
                print(resp['stack_trace'])
            else:
                return resp
        else:
            print('Error: Make sure the model is running (http://status.xfact.net/models). If the model is running, adjust the timeout or reduce the max_length parameter')
            return None
        
    def generate(self, n, tokenizer_kwargs=None, generate_kwargs=None, timeout=50):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = json.dumps({'func': 'generate', 
                              'body' : {
                                    "batch": n,
                                    "tokenizer_kwargs": tokenizer_kwargs or {},
                                    "generate_kwargs": generate_kwargs or {}
                                    }
        }).encode()

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                expiration=str(timeout)+'000',
            ),
            body=message)

        self.connection.process_data_events(time_limit=timeout)

        if self.response:
            resp =  json.loads(self.response.decode('utf-8'))
            if 'error' in resp:
                print(resp['stack_trace'])
            else:
                return resp
        else:
            print('Error: Make sure the model is running (http://status.xfact.net/models). If the model is running, adjust the timeout or reduce the max_length parameter')
            return None
        
    def forward(self, inputs, timeout=50):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = {'func': 'forward', 'body' : {
            "inputs": inputs
        }}

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                expiration=str(timeout)+'000',
            ),
            body=json.dumps(message).encode())

        self.connection.process_data_events(time_limit=timeout)

        if self.response:
            resp =  json.loads(self.response.decode('utf-8'))
            if 'error' in resp:
                print(resp['stack_trace'])
            else:
                return resp
        else:
            print('Error: Make sure the model is running (http://status.xfact.net/models). If the model is running, adjust the timeout or reduce the max_length parameter')
            return None

    def batch_call(self, all_items, batch_size=8, **kwargs):

        for batch in tqdm(lazy_groups_of(all_items, batch_size), desc="Inference", total=len(all_items)//batch_size):
            results = defaultdict(list)
            result = self.call(batch, **kwargs)

            if result and 'error' not in result:
                for k, v in result.items():
                    results[k].extend(v)
            else:
                raise Exception(f"bad result {result}")

            yield from results



if __name__ == "__main__":
    client = LSMSClient('','', model_name='')

    while tqdm(True):
        print(client.call("Tell me about X", generate_kwargs={"max_new_tokens":10,
                                                                     "do_sample": False,
                                                                     "num_return_sequences":1}))


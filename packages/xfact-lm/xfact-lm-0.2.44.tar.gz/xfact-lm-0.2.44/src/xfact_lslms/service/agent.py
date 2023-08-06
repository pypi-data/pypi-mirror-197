import logging
import argparse

from xfact_lslms.log_helper import setup_logging
from xfact_lslms.service.amq_communications import CommunicationLayer
from models import LanguageModelAgent

logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='t5-base', help='Model name')
    parser.add_argument('--cache_dir', default=None)
    parser.add_argument('--fp16', action='store_true')
    parser.add_argument('--bf16', action='store_true')
    parser.add_argument('--multi_gpu', action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    setup_logging()
    args = get_args()

    if 'llama' in args.model:
        logger.warning('Make sure to install https://github.com/zphang/transformers.git@llama_push version for transformer')

    lm = LanguageModelAgent(args)
    model_queue = args.model.split('/')[-1].lower()

    generate = lambda message: lm.infer(**message)
    forward = lambda message: lm.forward(**message)

    comms = CommunicationLayer(model_queue, generate, forward)
    comms.listen()

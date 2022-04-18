import custom
from custom import criterion
from custom.layers import *
from custom.config import config
from model import MusicTransformer
from data import Data
import utils
from processor import decode_midi, encode_midi

import datetime
import argparse
import sys

from tensorboardX import SummaryWriter

config.load("model", ["configs/"+(sys.argv[2] if len(sys.argv)>2 else "generate_noref")+".yml"], initialize=True)

# check cuda
if torch.cuda.is_available():
    config.device = torch.device('cuda')
else:
    config.device = torch.device('cpu')


current_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
gen_log_dir = 'logs/mt_decoder/generate_'+current_time+'/generate'
#gen_summary_writer = SummaryWriter(gen_log_dir)

mt = MusicTransformer(
    embedding_dim=config.embedding_dim,
    vocab_size=config.vocab_size,
    num_layer=config.num_layers,
    max_seq=config.max_seq,
    dropout=0,
    debug=False)
mt.load_state_dict(torch.load('model/'+(sys.argv[1] if len(sys.argv)>1 else "final")+'.pth'))
mt.test()

print(config.condition_file)
if config.condition_file is not None:
    inputs = np.array([encode_midi(config.condition_file)[:500]])
else:
    inputs = np.array([[24, 28, 31]])
inputs = torch.from_numpy(inputs)
result = mt(inputs, config.length)

for i in result:
    print(i)

decode_midi(result, file_path=config.save_path)

#gen_summary_writer.close()

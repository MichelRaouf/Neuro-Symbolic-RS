import argparse
import numpy as np
from time import time
from data_loader import load_data
from train import train

np.random.seed(555)

parser = argparse.ArgumentParser()

parser.add_argument('--aggregator', type=str, default='sum', help='Which aggregator to use')
parser.add_argument('--n_epochs', type=int, default=10, help='The number of epochs')
parser.add_argument('--neighbor_sample_size', type=int, default=4, help='The number of neighbors to be sampled "K"') #load data
parser.add_argument('--dim', type=int, default=32, help='Dimension of user and entity embeddings "d"')
parser.add_argument('--n_iter', type=int, default=2, help='Number of iterations when computing entity representation "H"')
parser.add_argument('--batch_size', type=int, default=65536, help='Batch size')
parser.add_argument('--l2_weight', type=float, default=1e-7, help='Weight of L2 regularization')
parser.add_argument('--lr', type=float, default=2e-2, help='Learning rate')
parser.add_argument('--ratio', type=int, default=1, help='Size of training dataset') #load_data

show_loss = False
show_time = False
show_topk = False

t = time()

args = parser.parse_args()
data = load_data(args) #args used in data loading are ratio and neighbor_sample_size
train(args, data, show_loss, show_topk)

if show_time:
    print('Time used: %d s' % (time() - t))
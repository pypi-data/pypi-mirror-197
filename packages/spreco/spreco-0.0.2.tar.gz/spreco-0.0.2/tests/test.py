from spreco.dataflow.base import RNGDataFlow
from spreco.dataflow.common import BatchData
from spreco.dataflow.parallel_map import MultiThreadMapData
from spreco.common import utils

import numpy as np

class cfl_pipe(RNGDataFlow):

    def __init__(self, files, shuffle):
        self._size   = len(files)
        self.files   = files
        self.shuffle = shuffle
    
    def __len__(self):
        return len(self.files)
    
    def __iter__(self):
        idxs = np.arange(self._size)
        if self.shuffle:
            self.rng.shuffle(idxs)
        
        for idx in idxs:
            fname = self.files[idx]
            yield fname

train_files = utils.read_filelist('test.txt')
dp = cfl_pipe(train_files, True)
def map_f(x):
    return x[:-4]
dp = MultiThreadMapData(dp, 10, map_f,  buffer_size=300, strict=True)
dp = BatchData(dp, 4, use_list=True)

dp.reset_state()
for f in dp:
    print(f)
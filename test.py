import time
from tqdm import tqdm

pbar = tqdm(total=100)

for i in range(100):
    # do some work here
    pbar.update(1)
    time.sleep(1)
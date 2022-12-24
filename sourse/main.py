from datetime import datetime
import time
from farnback import farn
from simpleflow import sf
from sparsetodense import std
from dualtvl1 import dtvl1
from pca import pca
from deep import df #banned
from denseRLOF import drlof
from VR import get_frames
from LK import LK


if __name__ == '__main__':
    start_time = datetime.now()
    for i in range(1):
        drlof()
    print((datetime.now() - start_time))


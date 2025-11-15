from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
import numpy as np
import time
import yaml
import math

class Threshold:
    def __init__(self) -> None:
        self.inlet = None
        self.flex_mean = 0
        self.relax_mean = 0
        self.temp_threshold = 0

    def get_signal(self):
        streams = resolve_stream('type', 'EMG')
        for stream in streams:
            if stream.name() == "EMG band":
                self.inlet = StreamInlet(stream, max_buflen = 1)
                print('received stream')
                break
    
    def recieve_data(self):
        sample, timestamp = self.inlet.pull_sample(timeout=0.0)
        return sample, timestamp



if __name__ == "__main__":
    threshold = Threshold()
    threshold.get_signal()
    
    while True:
        sample, timestamp = threshold.recieve_data()
        if sample:
            print("Sample:", sample)
        time.sleep(0.01)

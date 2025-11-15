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
            if stream.name() == "EMG Band":
                self.inlet = StreamInlet(stream, max_buflen = 1)
                print('received stream')
                break
    


    def calibrate(self):
        counter = 0
        print("Calibrating starting...")
        time.sleep(2)
        print("Completely relax in 3 seconds...")
        time.sleep(1)
        print("Completely relax in 2 seconds...")
        time.sleep(1)
        print("Completely relax in 1 second...")
        time.sleep(1)
        print("Completely relax now!")
        relax_data = np.array([])
        while(counter < 1000): # main loop to stream data from board
            sample, timestamp = self.inlet.pull_sample()
            print(counter, sample[0]**2)
            relax_data = np.append(relax_data,sample[0]**2)
            counter += 1
        
        mean_relax_data = np.mean(relax_data)
        print(mean_relax_data)
        
        print("STOP!!!!!!!")
        print("Clench in 3 seconds...")
        time.sleep(1)
        print("Clench in 2 seconds...")
        time.sleep(1)
        print("Clench in 1 second...")
        time.sleep(1)
        print("Clench now!")
        flex_data = np.array([])
        while(counter < 2000): # main loop to stream data from board
            sample, timestamp = self.inlet.pull_sample()
            print(counter, sample[0]**2)
            flex_data = np.append(flex_data,sample[0]**2)
            counter += 1
            
        mean_flex_data = np.mean(flex_data)
        print(mean_flex_data)
        counter = 0

        print("STOP!!!!!!!")
        
        #update relax and flex means and calculate temp_threshold
        self.relax_mean = mean_relax_data
        self.flex_mean = mean_flex_data
        self.temp_threshold = (math.sqrt(self.relax_mean) + 0.05 * (math.sqrt(self.flex_mean) - math.sqrt(self.relax_mean)))**2
        print(f'relax mean: {self.relax_mean}')
        print(f'flex mean: {self.flex_mean}')
        print(f'threshold: {self.temp_threshold}')
        #save data to config.yml file
        yaml_values = {
            'relax_mean': float(self.relax_mean), 
            'flex_mean': float(self.flex_mean), 
            'temp_threshold': float(self.temp_threshold)}
        with open('config.yml', 'w') as file:
            yaml.dump(yaml_values, file)



    def listen(self):
        sample, timestamp = self.inlet.pull_sample()

        #repull a sample in case there is none in the inlet
        while sample == None:
            sample, timestamp = self.inlet.pull_sample()

        control = ""
                #check for flex
        if sample[0]**2 > self.temp_threshold:
            #print("right", sample[0]**2, self.temp_threshold)
            control = "left"
                
                #else its relax
        else:
            #print("left", sample[0]**2, self.temp_threshold)
            control = "right"
        return control




if __name__ == "__main__":
    threshold = Threshold()
    threshold.get_signal()
    threshold.calibrate()
    threshold.listen()

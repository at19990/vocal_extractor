# Vocal Extractor    
## About    

This program extracts a vocal part from a vocal mixed and a karaoke sound source.  The uses of this tool are making a remix material, generate learning data for DNN and so on.    

## How to use    

It can process only WAVE files (sampling bit rate:16bit, sampling frequency: 44.1kHz).  
```
>> python vocal_extract.py {mixed_path} {karaoke_path} {output_file_name(.wav)} {volume_threshold (recommended 0.01~0.1)}
```  
As shown above, you need to input in command.  

## Method      

By inverting a phase of a karaoke source and synthesize with a mixed audio source, This script only eliminates instrumental part.  
The heads of each audio source are determined automatically through detecting the part which exceeds the user-input-threshold.    

## Hints      

In the specific types of an audio source such as listed below,  Sometimes you could fail to extraction.
-  The song which not contained prelude part
-  A vocal mixed source's mixing or volume is significantly different from karaoke source.
-  The head of the vocal source is different from the karaoke source for more than 10 seconds.     

## Requirements    

About libraries, please refer to __requirements.txt__

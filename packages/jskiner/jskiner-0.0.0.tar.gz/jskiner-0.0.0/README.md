# JSkiner 

The is a python **Js**on **Sch**ema **In**ference **E**ngine with **R**ust's core. 

# Installation 

```bash
pip install jsiner
```

# Usage

## Checking the Json Schema of a Large .jsonl file

```bash
jshow \
    --jsonl <path_to_jsonl> 
    --verbose <0/1> 
    --out <output_file_path>
    --nworkers <number_of_cpu_core>
```

## Infering the Schema in Python

```python
from jshow import InferenceEngine
cpu_cnt = 16
engine = InferenceEngine(cpu_cnt)
json_string_list = ["1", "1.2", "null", "{\"a\": 1}"]
schema_str = engine.run(json_string_list)
print(schema_str)
```
>> 'Union({Atomic(Float()), Atomic(Int()), Atomic(Non()), Record({"a": Atomic(Int())})})'



# TODO:
- [X] move json schema inference rust code here
- [X] add cmd.py tools for parsing .jsonl file to jshow
- [ ] build the cicd pipeline using .workflow

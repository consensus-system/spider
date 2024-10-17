import evaluate
from modelscope import GenerationConfig

module = evaluate.load("yuyijiong/quad_match_score")
predictions=["food | good | food#taste | pos"]
references=["food | good | food#taste | pos & service | bad | service#general | neg"]
result=module.compute(predictions=predictions, references=references)
print(result)

# import torch
# from transformers import T5Tokenizer, AutoModelForSeq2SeqLM
# tokenizer = T5Tokenizer.from_pretrained("yuyijiong/T5-large-sentiment-analysis-Chinese-MultiTask")
# model = AutoModelForSeq2SeqLM.from_pretrained("yuyijiong/T5-large-sentiment-analysis-Chinese-MultiTask", device_map="auto")
# generation_config=GenerationConfig.from_pretrained("yuyijiong/T5-large-sentiment-analysis-Chinese-MultiTask")
# text = '情感四元组(对象 | 观点 | 方面 | 极性)抽取任务(观点可以较长): [个头大、口感不错,就是个别坏了的或者有烂掉口子刻意用泥土封着,这样做不好。]'
# input_ids = tokenizer(text,return_tensors="pt", padding=True)['input_ids'].cuda(0)
# with torch.no_grad():
#   output = model.generate(input_ids=input_ids,generation_config=generation_config)
# output_str = tokenizer.batch_decode(output, skip_special_tokens=True)
# print(output_str)
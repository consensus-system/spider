from transformers import BertTokenizer, BertForSequenceClassification
from datasets import load_dataset

# 加载预训练的BERT模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese', num_labels=2)

# 加载数据集
dataset = load_dataset('chnsenticorp')

# 数据预处理
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True)

encoded_dataset = dataset.map(tokenize_function, batched=True)

# 训练模型（示例代码，实际训练需要更多步骤）
model.train(encoded_dataset)
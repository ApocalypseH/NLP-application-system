from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
import torch
import numpy as np
import pickle as pkl
from importlib import import_module

bp = Blueprint('paragraph', __name__, url_prefix='/paragraph')
dataset = 'Net/MicroBlog'
# 搜狗新闻:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random
embedding = 'embedding_blog.npz'
x = import_module('Net.models.TextCNN')
config = x.Config(dataset, embedding)
model = x.Model(config).to(config.device)

def pre_process(config, raw_content):
    UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号
    tokenizer = lambda x: [y for y in x]  # char-level
    # tokenizer = lambda x: x.split(' ')  # 以空格隔开，word-level
    vocab = pkl.load(open(config.vocab_path, 'rb'))
    pad_size = config.pad_size
    token = tokenizer(raw_content)
    if len(token) < pad_size:
        token.extend([PAD] * (pad_size - len(token)))
    else:
        token = token[:pad_size]
    words_line = []
    for word in token:
        words_line.append(vocab.get(word, vocab.get(UNK)))
    return words_line

def predict_class(config, model, content):
    # test
    model.load_state_dict(torch.load(config.save_path))
    model.eval()
    with torch.no_grad():
        outputs = model(torch.tensor([content]))
    return outputs

@bp.route('/classify', methods=['GET'])
def classify_init():
    content = ''
    has_content = bool(len(content))
    amusing_ratio = 0.
    serious_ratio = 0.
    return render_template('paragraph/classify.html', content_init='' ,content=content, \
        amusing_ratio=amusing_ratio, serious_ratio=serious_ratio, has_content=has_content)

@bp.route('/classify', methods=['POST'])
def classify():
    raw_content = request.form['content']
    has_content = bool(len(raw_content))
    # print(has_content)
    if has_content:
        content = pre_process(config, raw_content)
        pred_result = predict_class(config, model, content)
        amusing_ratio, serious_ratio = torch.softmax(pred_result, dim=1, dtype=float)[0].detach().numpy().tolist()
    else:
        amusing_ratio = 1
        serious_ratio = 0
    return render_template('paragraph/classify.html', content_init='' ,content=raw_content, \
        amusing_ratio=amusing_ratio, serious_ratio=serious_ratio, has_content=has_content)
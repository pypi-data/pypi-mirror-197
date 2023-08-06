# -*-coding: utf-8 -*-
"""
    @Author : PKing
    @E-mail : 390737991@qq.com
    @Date   : 2022-12-21 17:34:38
    @Brief  :
"""
import os
import time
import xmltodict
import random
from tqdm import tqdm
from pybaseutils import file_utils, image_utils


def demo_copy_move():
    image_dir = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/trainval/val"
    out_dir = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/word-similar/dataset/val"
    file_utils.copy_move_file_dir(image_dir, out_dir, sub_names=None, max_nums=None, shuffle=True)


def demo_copy_move_by_sub_names():
    # image_dir = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/trainval/val"
    image_dir = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/word-similar/dataset/train"
    out_dir = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/word-similar/dataset/test"
    # file = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/word-similar/dataset/word_similar_table.txt"
    # file = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/trainval/形近字表v1.txt"
    file = "/home/dm/nasdata/dataset-dmai/handwriting/word-class/word-similar/dataset/形近字表-sample.txt"
    # sub_names = ["玉", "王", "主", "玊", "壬", "玍", "生"]
    # sub_names += ["工", "土", "干", "士"]
    words = file_utils.read_data(file, split=",")
    sub_names = []
    for word in words:
        word = [w.strip() for w in word if w]  # 去除一些空格
        sub_names += word
    sub_names = list(set(sub_names))
    sub_names = sorted(sub_names)
    file_utils.copy_move_file_dir(image_dir, out_dir, sub_names=sub_names, max_nums=4000, shuffle=True, move=False)
    out_file = os.path.join(os.path.dirname(file), "file.txt")
    file_utils.write_list_data(out_file, sub_names)


if __name__ == "__main__":
    # demo_copy_move()
    demo_copy_move_by_sub_names()

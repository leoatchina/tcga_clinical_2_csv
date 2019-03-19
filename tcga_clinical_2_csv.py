#!/usr/bin/env python3
# coding:utf8
# Import modules
import os
import sys
import re
import csv

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# return_cmd in list
def return_cmd_list(cmd):
    try:
        if cmd:
            tmp = os.popen(cmd).readlines()
            return [line.strip() for line in tmp]
        else:
            raise Exception("cmd is None")
    except Exception as e:
        print(e)
        return None


# a easy way write to file
def write_to_file(file, *lst, delim = ","):
    if lst:
        line = delim.join(lst)
        os.system("echo %s >> %s" % (line, file))


# 根据xml的第二行，解析xmlns后的参数，形成namespace
def get_namespaces_from_xml(xml_file):
    cat_cmd = "cat %s | awk '{if(NR==2){print $0}}'" % xml_file
    xml_head = return_cmd_list(cat_cmd)[0][1:-1]
    reg = "xmlns:\S*"
    xml_namespaces = {}
    for each in re.findall(reg, xml_head):
        key, value = each.split("=")
        value = value[1:-1]
        xml_namespaces[key] = value
    return(xml_namespaces)


# copy from xml file, and rearange
def parse_xml(xml_file, *items, namespaces):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    patient = root[1]
    for item in items:
        for child in patient.findall(item, namespaces):
            print(child.text)


# get the tag and text of a node, use re module to delete xmlns prefix
def get_key_value(node):
    key = node.tag
    key = re.sub(r'{[^)]*}', '', key)
    value = node.text
    if value:
        value = value.replace(r'\n', '').strip()
    else:
        value = ""
    return({key: value})


# 遍历node和子node
def walk_through_node(root_node):
    children_nodes = list(root_node)
    if children_nodes:
        return_dict = {}
        for child_node in children_nodes:
            return_dict = {**return_dict, ** walk_through_node(child_node)}
    else:
        return_dict = get_key_value(root_node)
    return return_dict


if __name__ == "__main__":
    try:
        input_dir = sys.argv[1]
    except IndexError:
        input_dir = "./clin"   # 默认目录
    if not os.path.isdir(input_dir):
        raise Exception("dir %s not exists" % input_dir)
    try:
        out_csv = sys.argv[2]   # 默认输出文件
    except IndexError:
        out_csv = "./merge.csv"
    basedir = os.path.dirname(out_csv)
    if not os.path.isdir(basedir) and basedir != '':  # 生成下目录
        os.mkdir(basedir)
    if os.path.isfile(out_csv):
        os.remove(out_csv)
    find_xml = "find {} | grep .xml".format(input_dir)
    cnt = 0
    xml_list = return_cmd_list(find_xml)
    if len(xml_list) == 0:
        raise Exception("Cannot find xml files in %s" % input_dir)
    try:
        dict_lst = []
        for xml in xml_list:
            tree = ET.parse(xml)  # 载入数据
            root = tree.getroot()
            return_dict = walk_through_node(root)
            dict_lst.append(return_dict)
        columns = set()
        for each in dict_lst:
            columns = columns.union(set(list(each.keys())))
        for each in dict_lst:
            diff_keys = columns.difference(set(list(each.keys())))
            for key in diff_keys:
                each[key] = ''
        # write header
        with open(out_csv, 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, dict_lst[0].keys())
            w.writeheader()
        # write each
        for each in dict_lst:
            with open(out_csv, 'a') as f:  # Just use 'a' mode in 3.x
                w = csv.DictWriter(f, each.keys())
                w.writerow(each)
        print("All done!")
    except Exception as e:
        print(xml, cnt)
        raise e

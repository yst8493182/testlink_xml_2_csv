#!/usr/bin/env python
# coding=utf-8
import os
from xml.dom.minidom import parse
import xml.dom.minidom
import csv


def txt_replace(text_content):
    """
    处理文本内容中的特殊HTML的特殊字符
    :param text_content:
    :return:
    """
    return text_content.replace("<p>", "").replace("&ldquo;", "“"). \
        replace("&rdquo;", "”").replace("<br />", "").replace("</p>", ""). \
        replace("\n", "").replace("&nbsp;", " ")


def write_csv(testcases, file_name):
    """
    生成csv文件，只存放以下信息：用例标题、前置条件、步骤、预期
    :param testcases:
    :param file_name:
    :return:
    """
    filepath = "./csvs/" + file_name + ".csv"
    with open(filepath, "w") as csv_file:
        fieldnames = ['用例编号', '所属产品', '所属模块', '用例标题', '前置条件', '步骤', '预期', '用例类型', '用例状态', '结果']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for testcase in testcases:
            writer.writerow({'用例标题': testcase["用例标题"],
                             '前置条件': testcase["前置条件"],
                             '用例类型': '功能测试',
                             '步骤': testcase["步骤"],
                             '预期': testcase["预期"]})


def parse_xml(xml_path):
    """
    解析传进来的xml文件
    :param xml_path:
    :return:
    """
    print("开始解析%s文件" % xml_path)
    dom_tree = xml.dom.minidom.parse("./xmls/" + xml_path)
    collections = dom_tree.documentElement
    test_cases = collections.getElementsByTagName("testcase")
    num = 1
    map_list = list()
    for test_case in test_cases:
        map = dict()
        print("用例标题: %s" % test_case.getAttribute("name"))
        testcase_name = test_case.getAttribute("name")
        map["用例标题"] = str(num) + "." + testcase_name.replace("/", "").replace("-", "")
        preconditions = test_case.getElementsByTagName("preconditions")[0]
        preconditions_txt_all = ""
        if preconditions.hasChildNodes():
            print("前置条件：%s" % txt_replace(preconditions.childNodes[0].data))
            preconditions_txt = txt_replace(preconditions.childNodes[0].data)
            preconditions_txt_all = preconditions_txt_all + preconditions_txt

        map["前置条件"] = preconditions_txt_all
        # print(txt_replace(testcases.getAttribute("preconditions")))
        steps = test_case.getElementsByTagName("step")
        actions_txt_all = ""
        expected_results_txt_all = ""
        for step in steps:
            step_number = step.getElementsByTagName('step_number')[0]
            print("步骤：%s" % txt_replace(step_number.firstChild.data))
            step_number_txt = txt_replace(step_number.firstChild.data)
            expected_results_txt_all = expected_results_txt_all + step_number_txt + "."
            actions_txt_all = actions_txt_all + step_number_txt + "."
            actions = step.getElementsByTagName('actions')[0]
            print("操作：%s" % txt_replace(actions.firstChild.data))
            actions_txt = txt_replace(actions.firstChild.data)
            actions_txt_all = actions_txt_all + actions_txt + "\n"
            expected_results = step.getElementsByTagName('expectedresults')[0]
            print("预期：%s" % txt_replace(expected_results.firstChild.data))
            expected_results_txt = txt_replace(expected_results.firstChild.data)
            expected_results_txt_all = expected_results_txt_all + expected_results_txt + "\n"
            print(txt_replace("<----------------------------------->"))

        map["步骤"] = actions_txt_all
        map["预期"] = expected_results_txt_all
        map_list.append(map)
        num += 1

    print("%s 解析完成" % xml_path)
    return map_list


def xml_2_csv():
    files = os.listdir("./xmls/")
    for file in files:
        print(file)
        maps = parse_xml(file)
        write_csv(maps, file.split(".")[0])

if __name__ == '__main__':
    xml_2_csv()

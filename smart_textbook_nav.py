# -*- coding: utf-8 -*-
"""
智能课文学习导航优化

需求：
1. 用户在单词表中点击"课文学习"按钮时
2. 如果当前在某个单词模块中（如"上1"），直接跳转到对应的课文模块的单元列表（如"Module 1"）
3. 如果不在单词模块中，则显示所有课文模块列表
4. 在单元列表中点击"课文学习"时，可以选择跳转到下一个单元（不返回单元选择）
5. 在单元详情中点击"课文学习"时，跳转到下一个单元的详情

映射规则：
- 上1 → Module 1 (三年级上册)
- 上2 → Module 2 (三年级上册)
- ...
- 上10 → Module 10 (三年级上册)
- 下1 → Module 1 (三年级下册) - 未来支持
- 下2 → Module 2 (三年级下册) - 未来支持
- ...
"""

# 单词模块到课文模块的映射
WORD_TO_LESSON_MODULE = {
    '上1': 'Module 1',
    '上2': 'Module 2',
    '上3': 'Module 3',
    '上4': 'Module 4',
    '上5': 'Module 5',
    '上6': 'Module 6',
    '上7': 'Module 7',
    '上8': 'Module 8',
    '上9': 'Module 9',
    '上10': 'Module 10',
    # 下册暂未添加课文
    '下1': None,
    '下2': None,
    '下3': None,
    '下4': None,
    '下5': None,
    '下6': None,
    '下7': None,
    '下8': None,
    '下9': None,
    '下10': None,
}


def get_lesson_module_from_word_module(word_module):
    """
    根据当前单词模块，获取对应的课文模块名
    返回 None 表示该单词模块没有对应的课文
    """
    return WORD_TO_LESSON_MODULE.get(word_module)


# 单元顺序：用于"下一个单元"导航
UNIT_ORDER = {
    'Module 1': ['Unit 1', 'Unit 2'],
    'Module 2': ['Unit 1', 'Unit 2'],
    # ...
}

if __name__ == '__main__':
    # 测试
    print("上1 →", get_lesson_module_from_word_module('上1'))
    print("上5 →", get_lesson_module_from_word_module('上5'))
    print("下1 →", get_lesson_module_from_word_module('下1'))
    print("无效模块 →", get_lesson_module_from_word_module('xxx'))
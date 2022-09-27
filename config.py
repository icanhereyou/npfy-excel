# 固定字符， 若对应为以下几个，则直接返回值
guding_str = ["Y", "N", "无", "其他费"]

# 诊疗导入模板： 采购平台
zldr_cgpt_mapping = {
    '项目编号': '项目编码',
    '项目名称': '通用名称',
    '生产厂家': '厂家',
    '剂型': '剂型',
    '发票项目': '发票项目',
    '项目规格': '规格',
    '药品类别': None,
    '是否医保项目': '是否医保',
    '自付比例': None,
    '参考单价': '最高销售限价（元）',
    '项目限价': '医保结算支付价（元）',
    '备注': '备注',
    '产品ID': '产品ID',
    '医保单位': '计价单位',
    '医保结算支付价': '医保结算支付价（元）',
    '最小计量单位': '最小销售计价单位',
    '计量单位限价': '最小最高销售限价（元）',
    '计量单位支付价': '最小医保结算支付价（元）',
    '是否药品': 'Y',
    '拆分比例': '拆分比率'
}

# 诊疗导入模板： 国家耗材
zldr_gjhc_mapping = {
    '项目编号': '医保耗材代码',
    '项目名称': '单件产品名称',
    '生产厂家': '生产企业名称',
    '剂型': None,
    '发票项目': '其他费',
    '项目规格': '无',
    '药品类别': None,
    '是否医保项目': 'Y',
    '自付比例': None,
    '参考单价': None,
    '项目限价': None,
    '备注': None,
    '产品ID': None,
    '医保单位': '计量单位',
    '医保结算支付价': None,
    '最小计量单位': '计量单位',
    '计量单位限价': None,
    '计量单位支付价': None,
    '是否药品': 'N',
    '拆分比例': None
}

# 诊疗导入模板： 医疗服务价格及项目
zldr_ylfw_mapping = {
    '项目编号': '国家结算编码',
    '项目名称': '项目名称',
    '生产厂家': None,
    '剂型': None,
    '发票项目': '财务项目',
    '项目规格': '无',
    '药品类别': None,
    '是否医保项目': '医保属性',
    '自付比例': None,
    '参考单价': '最高销售限价（元）',
    '项目限价': '医保结算支付价（元）',
    '备注': '备注',
    '产品ID': '产品ID',
    '医保单位': '计价单位',
    '医保结算支付价': '医保结算支付价（元）',
    '最小计量单位': '最小销售计价单位',
    '计量单位限价': '最小最高销售限价（元）',
    '计量单位支付价': '最小医保结算支付价（元）',
    '是否药品': 'Y',
    '拆分比例': '拆分比率'
}

# 配置文件名
zldr_config_list = [
    {
        "enable": True,
        "file_name": ["依据采购平台信息调整 - 医院"],
        "file_name_not_contains":[],
        "sheet_list": [0],
        "mapping": zldr_cgpt_mapping,
        "header": None,
        "copy_rule_list": [{
            # 要检测的列
            "check_column": "医保结算支付价（元）",
            # 是否包含词
            "if_contains": "销售",
            # 是的话用use_column替换
            "use_column": "最高销售限价（元）",
        }, {
            "check_column": "最小医保结算支付价（元）",
            "if_contains": "销售",
            "use_column": "最小最高销售限价（元）",
        }],
        "replace_rule_list": []
    }, {
        "enable": True,
        "file_name": ["国家耗材分类及编码信息表"],
        "file_name_not_contains":[],
        "sheet_list": [0],
        "mapping": zldr_gjhc_mapping,
        "copy_rule_list": [],
        "header": 1,
        "replace_rule_list": []
    }, {
        "enable": True,
        "file_name": ["医疗服务项目及价格"],
        "file_name_not_contains": ["补充调整表"],
        # sheet：-1：表示所有sheet， 其他表示第几个sheet
        "sheet_list": [0, 1, 2, 3, 4],
        "mapping": zldr_ylfw_mapping,
        "header": 3,
        "copy_rule_list": [],
        "replace_rule_list": [{
            "column_name": "医保属性",
            "check_str": "医保",
            "replace_str": "Y"
        }]
    }, {
        "enable": True,
        "file_name": ["补充调整表"],
        "file_name_not_contains": [],
        "sheet_list":  [0],
        "mapping": zldr_ylfw_mapping,
        "header": 1,
        "copy_rule_list": [],
        "replace_rule_list": []
    }
]


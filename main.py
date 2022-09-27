import datetime

import pandas as pd
import os
import config


# 如果字段不存在原表格内，返回一个空值
def if_column_exists(value, df):
    if value is None:
        return None
    try:
        return df[value]
    except Exception as e:
        if value in config.guding_str:
            return value
        else:
            print("原表不存在列：[" + value + "]")


# 判断文件名是否符合规则
def if_file_name_contain(file_name, contain_list, not_contain_list):
    for contain in contain_list:
        # 如果不存在应该包含的字符
        if not file_name.__contains__(contain):
            return False
    for not_contain in not_contain_list:
        # 如果存在不该存在的字符
        if file_name.__contains__(not_contain):
            return False
    return True


# 诊疗导入模板
def zldr_main():
    # 获取文件名
    file_names = os.listdir('res')

    for file_name in file_names:
        if file_name.__contains__("+HIS诊疗导入模板"):
            continue
        if_file_exported = 0
        for compare_file_name in file_names:
            if compare_file_name == file_name + '+HIS诊疗导入模板.xlsx':
                if_file_exported = 1
        if if_file_exported:
            print("已存在" + file_name + '+HIS诊疗导入模板.xlsx')
            continue
        for zldr_config in config.zldr_config_list:
            # 如果配置关闭则跳过
            if zldr_config.get("enable") is False:
                continue
            #     根据文件名字匹配规则
            if if_file_name_contain(file_name, zldr_config.get("file_name"), zldr_config.get("file_name_not_contains")):
                for sheet in zldr_config.get("sheet_list"):
                    print("正在执行: " + file_name)
                    df = pd.read_excel("./res" + "/" + file_name, sheet_name=sheet, header=zldr_config.get("header"))
                    # 只有"依据采购平台信息调整 - 医院"要处理标题
                    if file_name.__contains__("依据采购平台信息调整 - 医院"):
                        # 按列将将第二行数据复制到第一行
                        for i in range(0, df.iloc[1].size):
                            if str(df.iloc[1, i]) != "nan" and len(str(df.iloc[1, i])) > 1:
                                df.at[0, i] = str(df.iloc[1, i])
                        # 设置第一行为标题， 删除第二行(第二行也是列名)
                        df.columns = df.iloc[0]
                        df.drop(df.head(2).index, inplace=True)
                    # 若check_column包含 if_contains 对应的字符， 则使用其他列数据
                    for copy_rule in zldr_config.get("copy_rule_list"):
                        check_column_name = copy_rule.get("check_column")
                        df[check_column_name] = df.apply(
                            lambda x: x[check_column_name]
                            if not (str(x[check_column_name]).__contains__(copy_rule.get("if_contains")))
                            else x[copy_rule.get("use_column")], axis=1)
                    # 若指定列包含固定字符串check_str, 则修改成replace_str
                    for replace_rule in zldr_config.get("replace_rule_list"):
                        pass

                # 将处理后的数据输出成excel
                zldr_excel = pd.DataFrame(data=None)
                i = 0
                for key in zldr_config.get("mapping"):
                    zldr_excel.insert(i, key, if_column_exists(zldr_config.get("mapping").get(key), df))
                    i = i + 1

                # 输出改后数据
                if zldr_excel.shape[0] != df.shape[0]:
                    print("转换行数不匹配， 请先手动自行制作导入模板: " + str(zldr_excel.shape[0]) + "," + str(df.shape[0]))
                else:
                    zldr_excel.to_excel('./res/' + file_name + '+HIS诊疗导入模板.xlsx', index=False)
                    print('文件导出完成：' + file_name + '+HIS诊疗导入模板.xlsx')


if __name__ == '__main__':
    zldr_main()

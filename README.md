## PSMS提单系统
1、在拉取Facebook、Apple的campaign name与campaign id的对应关系时,已经获取到优化师的名字编号(optName)
2、get_fb_rebate.py 脚本是拉取完Facebook的数据后半个小时执行计算返点金额  (以后需要优化)
3、adwordsData.py,Geo.py 的文件已经不用
4、adwords_optization.py 文件已经加到计划任务中,每天10:30、15:30执行,此脚本是获取adwords平台的优化师数据
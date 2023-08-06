from cjdg_api.base import baseApixxYent
import os
import requests
import json
from cjdg_api.base import base

'''
@Author  :   顾一龙 
@Time    :   2022/11/27 21:06:23
@Version :   1.0
@Contact :   小爷怕什么就做什么，就是那么拽！
'''
# Hard to write shit mountain......
# 商品清单


class Goods_list(baseApixxYent):
    def __init__(self, token, domain=True, app_secret=None):
        super().__init__(token, domain, app_secret)
# 商品清单搜索用例

    def goods_list(self, data):
        api_name = f"enter/goods/center/mgt/goodslist/pageQuery"
        return self.request(api_name=api_name, data=data)

    # 商品清单查看用例
    def goods_detail(self, data):
        api_name = f"enter/goods/center/mgt/goodslist/detail"

        return self.request(api_name=api_name, data=data)

    def goods_list_id(self, data):
        api_name = f"enter/goods/center/mgt/goodslist/pageQuery"
        return self.request(api_name=api_name, data=data, )

    # 商品清单编辑用例

    def goods_findBizCount01(self, data):
        api_name = f"enter/goods/component//extension/goodsBiz/findBizCount"

        return self.request(api_name=api_name, data=data, )

    def goods_findBizCount02(self, data):
        api_name = f"enter/userCenter/extension/openBizSelect/findBizCount"

        return self.request(api_name=api_name, data=data, )

    # 查询商品

    def goods_list_01(self, data):
        api_name = f"shopguide/api/fab/goods/list"
        return self.request(api_name=api_name, data=data,)

    # 查询商品组

    def goods_list_role(self, data):
        api_name = f"shopguide/api/product/group/query"
        return self.request(api_name=api_name, data=data)

    # 添加商品组和商品

    def goods_save(self, data):
        api_name = f"enter/goods/component/extension/goodsBiz/save"
        return self.request(api_name=api_name, data=data, )

    # 商品清单-查询人员用例

    def goods_user_list(self, data):
        api_name = f"enter/userCenter/extension/user/list"
        return self.request(api_name=api_name, data=data, )

    # 商品清单-查询工号用例

    def goods_user_usercode(self, data):
        api_name = f"enter/userCenter/extension/user/list"

        return self.request(api_name=api_name, data=data, )

    # 商品清单-查询人员name用例

    def goods_user_name(self, data):
        api_name = f"enter/userCenter/extension/user/list"

        return self.request(api_name=api_name, data=data, )

    # 商品清单-查询人员tel用例

    def goods_user_tel(self, data):
        api_name = f"enter/userCenter/extension/user/list"

        return self.request(api_name=api_name, data=data, )

    # 商品清单-用户组用例

    def goods_userGroup(self, data):
        api_name = f"enter/userCenter/extension/userGroup/list"

        return self.request(api_name=api_name, data=data, )

    # 商品清单-查询组织用例

    def goods_treeList(self, data):
        api_name = f"enter/userCenter/extension/org/treeList"
        return self.request(api_name=api_name, data=data, )

    # 商品清单-编辑用例

    def goods_modify(self, data):
        api_name = f"enter/goods/component//extension/goodsBiz/findBizCount"
        return self.request(api_name=api_name, headers=data, )

    # 商品清单-新增用例

    def goods_add(self, data):
        api_name = f"enter/goods/center/mgt/goodslist/add"

        return self.request(api_name=api_name, data=data, )

    """


    清单分类
    """
    # 清单分类

    def goods_detailed_list(self, data):
        api_name = "enter/goods/center/mgt/category/add?"

        return self.request(api_name=api_name, data=data)

    # 清单的编辑

    def goods_edit_list(self, data):
        api_name = "enter/goods/center/mgt/category/modify?"

        return self.request(api_name=api_name, data=data)

    # 清单查询

    def goods_pagequery_list(self, data):
        api_name = "enter/goods/center/mgt/category/pageQuery?"
        return self.request(api_name=api_name, data=data)

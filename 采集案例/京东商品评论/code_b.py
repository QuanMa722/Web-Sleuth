
# -*- coding: utf-8 -*-
# 采集京东商品评论等信息(https://club.jd.com/comment/productPageComments.action)

# 导入需要的第三方库
from fake_useragent import UserAgent  # 构造ua
import requests  # 发送请求

"""

aesPin: null
afterDays: 0
anonymousFlag: 1
content: "＃三星AI手机爱了＃老三星粉了，从三星s6edge开始，一直到三星S20+，今年终于三星S24+恢复内存12G了，买的升杯套餐，做工还是一如既往的很不错的。今年升级的AI功能还是很不错的，修图、翻译都是刚需，有时玩switch游戏还可以翻译。手机重量也刚刚好，买的紫色，在有些角度像蓝色，还是很漂亮的。"
creationTime: "2024-02-06 19:16:04"
days: 17
discussionId: 1460469101
extMap: 
{buyCount: 3}
firstCategory: 9987
guid: "17ad10b23a31e5f6504227feffebaa91"
id: 20463008959
imageCount: 5
imageIntegral: 40
imageStatus: 1
images: [{id: -1830420478,…}, {id: -1830420477,…}, {id: -1830420476,…}, {id: -1830420475,…},…]
integral: 80
isDelete: false
isTop: false
location: "江苏"
mergeOrderStatus: 2
mobileVersion: "12.3.5"
nickname: "花***生"
orderId: 0
ownId: 1000003443
ownType: 0
plusAvailable: 201
productColor: "秘矿紫"
productSales: "[{\"dim\":3,\"saleName\":\"可选版本\",\"saleValue\":\"备用1\"}]"
productSize: "12GB+512GB"
referenceId: "100082692329"
referenceImage: "jfs/t1/236015/20/13423/92891/65d05e48F9b184675/34cae17b17a4e86f.jpg"
referenceName: "三星（SAMSUNG） Galaxy S24+ Al智享生活办公 智能修图建议 2K全视屏 12GB+256GB 水墨黑 5G AI手机"
referenceTime: "2024-01-20 23:03:24"
replyCount: 0
replyCount2: 0
score: 5
secondCategory: 653
status: 1
textIntegral: 40
thirdCategory: 655
topped: 0
usefulVoteCount: 0
userClient: 4
userImage: "misc.360buyimg.com/user/myjd-2015/css/i/peisong.jpg"
userImageUrl: "misc.360buyimg.com/user/myjd-2015/css/i/peisong.jpg"

"""


def get_comment(goods_id: int, page_num: int, comment_class: int) -> None:
    """
    发送请求，获取信息

    :param goods_id: int 商品id
    :param page_num: int 爬取页数
    :param comment_class: int 评论分类
    :return: None
    """

    try:
        # 初始url
        url = 'https://club.jd.com/comment/productPageComments.action'
        # 循环页数
        for page in range(0, page_num + 1):
            # 构造param
            param = {
                'productId': goods_id,  # 商品id
                'score': comment_class,  # 评论分类
                'sortType': '5',
                'page': page,  # 页数
                'pageSize': '10',
                'isShadowSku': '0',
                'fold': '1',
            }
            # 构造请求头
            ua = UserAgent()
            headers = {
                'User-Agent': ua.random
            }
            # 发送请求
            response = requests.get(url=url, headers=headers, params=param)

            for index in response.json()['comments']:
                # 获取评论数据，可根据需要获取其他数据
                content = index['content']

                # 打印数据，检验运行
                print(content)

                # 根据需求存储数据
                get_file(content)

    # 根据报错信息修改代码
    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def get_file(content: str) -> None:
    """
    将数据存储到文件中

    :param content: str 评论
    :return: None
    """

    with open("comment.txt", "a", encoding="utf-8") as f:
        f.write(content + "\n")

    return None


def main():
    """
    主函数，用于控制整个程序流程
    """
    while True:
        # 输入开始章节和结束章节
        try:
            # 获取商品id
            goods_id = int(input("goods_id: "))
            # 获取采集页数
            page_num = int(input("page_num: "))
            # 获取评论分类
            comment_class = int(input("1.bad 2.middle 3.good: "))

            # 判断comment_class是否为1、2或3，如果不是，则引发异常
            if comment_class not in [1, 2, 3]:
                raise ValueError
            get_comment(goods_id, page_num, comment_class)
            break

        except ValueError:
            print("comment_class只能输入1、2或3，请重新输入。")

        except Exception as e:
            print(f"An error occurred: {e}")

    return None


if __name__ == '__main__':
    main()





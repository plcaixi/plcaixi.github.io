from spider import Spider, SpiderItemType, SpiderItem
import requests
import re
import json
from utils import get_image_path
from bs4 import BeautifulSoup
import xbmcaddon

_ADDON = xbmcaddon.Addon()

class Spider91md(Spider):

    def name(self):
        return '91麻豆'

    def logo(self):
        return get_image_path('qiqi.png')

    def is_searchable(self):
        return False

    def hide(self):
        return not _ADDON.getSettingBool('data_source_91md_switch')

    def list_items(self, parent_item=None, page=1):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
        if parent_item is None:
            items = []
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id='23',
                    name='mini传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id='1',
                    name='麻豆视频',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="3",
                    name='天美传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="4",
                    name='蜜桃传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="5",
                    name='皇家华人',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="6",
                    name='星空传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="7",
                    name='精东影业',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="8",
                    name='乐播传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="10",
                    name='乌鸦传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="20",
                    name='兔子先生',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="21",
                    name='杏吧原创',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="22",
                    name='玩偶姐姐',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="24",
                    name='大象传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="9",
                    name='成人头条',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id='2',
                    name='91制片厂',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="27",
                    name='糖心Vlog',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="25",
                    name='开心鬼传媒',
                    params={
                        'type': 'category',
                    },
                ))
            items.append(
                SpiderItem(
                    type=SpiderItemType.Directory,
                    id="26",
                    name='PsychoPorn',
                    params={
                        'type': 'category',
                    },
                ))
            return items, False

        elif parent_item['params']['type'] == 'category':
            url = 'https://91md.me/index.php/vod/type/id/{0}/page/{1}.html'.format(parent_item['id'], page)
            r = requests.get(url=url, headers=header)
            soup = BeautifulSoup(r.text, 'html.parser')
            data = soup.select('div.detail_right_div > ul > li')
            items = []
            for video in data:
                vid = video.select('a')[0].get('href')
                name = video.select('img.lazy')[0].get('title')
                remark =video.select('p > i')[0].get_text()
                cover = video.select('img.lazy')[0].get('src')
                items.append(
                    SpiderItem(
                        type=SpiderItemType.Directory,
                        name='{0}/{1}'.format(remark,name),
                        id=vid,
                        cover=cover,
                        params={
                            'type': 'video',
                        },
                    ))
            numitems = int(len(items))
            if numitems == 18:
                has_next_page = True
            else:
                has_next_page = False
            return items, has_next_page

        elif parent_item['params']['type'] == 'video':
            url = 'https://91md.me/{0}'.format(parent_item['id'])
            r = requests.get(url, headers=header)
            cover = parent_item['cover']
            items = []
            sources = []
            name = parent_item['name']
            purl = json.loads(re.search(r'var player_aaaa=(.*?)</script>', r.text).group(1))['url']
            sources.append({
                'name': '91麻豆',
                'params': {
                    'id': purl,
                }
            })
            items.append(
                SpiderItem(
                    type=SpiderItemType.File,
                    name=name,
                    cover=cover,
                    sources=sources,
                ))
            return items, False
        else:
            return [], False

    def resolve_play_url(self, source_params):
        purl = source_params['id']
        return purl

    def search(self, keyword):
        return []

#if __name__ == '__main__':
    #spider = Spider91md()
    #res = spider.list_items(parent_item=None, page=1)
    #res = spider.resolve_play_url({'id': ''})
    #res = spider.search("")
    #print(res)
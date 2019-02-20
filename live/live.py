import requests, json, time, hashlib, subprocess

bilibili_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
        }

douyu_headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4'
        }

yy_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
    'Referer' : 'http://interface.yy.com/'
        }

def get_bilibili_roomlist():
    bilibili_roomlist_url = 'https://api.live.bilibili.com/room/v1/AmuseArea/getThirdPageData?parent_area_id=1&cate_id=3&area_id=33&sort_type=online&page_size=10&scrollTid=0&page_no=1'
    bilibili_music_roomlist_url = 'https://api.live.bilibili.com/room/v1/AmuseArea/getThirdPageData?parent_area_id=1&cate_id=3&area_id=34&sort_type=online&page_size=10&scrollTid=0&page_no=1'
    content = requests.get(bilibili_roomlist_url, headers=bilibili_headers).text
    json_content = json.loads(content)
    room_list = json_content['data']['room_list']
    rooms_list = []
    for rooms in room_list:
        room_id = rooms['roomid']
        title = rooms['title']
        cover = rooms['user_cover']
        preview = rooms['system_cover']
        rooms_list.append(cover)
        rooms_list.append(title)
    return rooms_list

def get_douyu_roomlist():
    douyu_roomlist_url = 'https://www.douyu.com/gapi/rkc/directory/2_208/1'
    content = requests.get(douyu_roomlist_url, headers=yy_headers).text
    json_content = json.loads(content)
    room_list = json_content['data']['rl']
    rooms_list = []
    for rooms in room_list:
        room_id = rooms['rid']
        title = rooms['rn']
        preview = rooms['rs1']
        rooms_list.append(preview)
        rooms_list.append(title)
    return rooms_list


def get_yy_roomlist():
    yy_music_roomlist_url = 'http://www.yy.com/more/page.action?biz=sing&subBiz=pop&page=1&moduleId=476&pageSize=10'
    content = requests.get(yy_music_roomlist_url, headers=yy_headers).text
    json_content = json.loads(content)
    room_list = json_content['data']['data']
    print(room_list)
    for rooms in room_list:
        room_id = rooms['sid']
        title = rooms['desc']
        preview = rooms['thumb']
        print(room_id, title, preview)


def bilibili_get_real_url(room_id):
    bilibili_url = 'https://live.bilibili.com/api/playurl?cid={}&otype=json'.format(room_id)
    content = requests.get(bilibili_url, headers=bilibili_headers).text
    json_content =json.loads(content)
    real_url = '"'+json_content['durl'][0]['url']+'"'
    subprocess.call('ffplay -x 1280 -y 720 {}'.format(real_url))


def douyu_get_real_url(room_id):
    api_url = "http://www.douyutv.com/api/v1/"
    args = "room/%s?aid=wp&client_sys=wp&time=%d" % (room_id, int(time.time()))
    auth_md5 = (args + "zNzMV1y4EMxOHS6I5WKm").encode("utf-8")
    auth_str = hashlib.md5(auth_md5).hexdigest()
    douyu_json_request_url = "%s%s&auth=%s" % (api_url, args, auth_str)
    content = requests.get(douyu_json_request_url, headers=douyu_headers).text
    json_content = json.loads(content)
    data = json_content['data']
    real_url = '"'+data.get('rtmp_url') + '/' + data.get('rtmp_live')+'"'
    subprocess.call('ffplay -x 1280 -y 720 {}'.format(real_url))


def yy_get_real_url(room_id):
    yy_url = 'http://interface.yy.com/hls/new/get/{}/{}/1200?source=wapyy&callback=jsonp2'.format(room_id, room_id)
    content = requests.get(yy_url, headers=yy_headers).text
    json_content = json.loads(content[7:-1])
    real_url = '"'+json_content['hls']+'"'
    subprocess.call('ffplay -x 1280 -y 720 {}'.format(real_url))


room_id = 'https://www.douyu.com/20415'
douyu_get_real_url(room_id.split('/')[-1])



import win32api, win32con, win32gui, os, time
import requests, re, random


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'desktoppapers.co',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
            }
def request_img(url):
    html = requests.get(url, headers=headers).text
    img_urls = re.findall(r'a href="(http://desktoppapers.co/\w+-\w+-.*?/)" title', html)
    imgurl = img_urls[random.randint(0, len(img_urls))-1].split('/')[-2]
    data = requests.get('http://papers.co/wallpaper/papers.co-'+imgurl+'-36-3840x2400-4k-wallpaper.jpg').content
    with open('D:/temp.jpg', 'wb') as f:
        f.write(data)

def set_wallpaper(img_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "10")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path, win32con.SPIF_SENDWININICHANGE)
def do():
    request_img('http://desktoppapers.co/sexy/page/{}/'.format(random.randint(1, 27)))
    time.sleep(5)
    set_wallpaper('D:/temp.jpg')
    time.sleep(3)
    os.remove('D:/temp.jpg')
while True:
    do()




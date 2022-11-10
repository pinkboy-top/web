import requests


def get_ip_info(host: str) -> str:
    """
    获取ip详情
    """
    if host:
        try:
            req = requests.post('https://ip.taobao.com/outGetIpInfo', data={'ip': host, 'accessKey': 'alibaba-inc'}).json()
            info = req.get('data')
            return f"{info.get('country')}{info.get('isp')}{info.get('region')}{info.get('city')}"
        except Exception as exp:
            return f"request error: {exp}"
    else:
        return "no host!"

if __name__ == '__main__':
    print(get_ip_info('101.68.66.194'))

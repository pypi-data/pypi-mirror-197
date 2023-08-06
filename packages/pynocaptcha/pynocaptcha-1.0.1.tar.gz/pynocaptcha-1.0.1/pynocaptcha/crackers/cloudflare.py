
import pyhttpx
from loguru import logger

from .base import BaseCracker

import warnings
warnings.filterwarnings('ignore')


class CloudFlareCracker(BaseCracker):
    
    cracker_name = "cloudflare"
    cracker_version = "universal"    

    """
    cloudflare cracker
    :param href: 触发 cloudfalre 验证的首页地址
    :param user_agent: 请求流程使用 ua, 必须使用 MacOS Firefox User-Agent, 否则可能破解失败
    :param html: 触发 cloudflare 验证的响应源码, 特征: window._cf_chl_opt=.../window["CF$params"]=...
    :param random_tls: 是否使用随机 tls 的请求客户端验证(即 chrome 110), 随机 tls 验证更容易, 可能不触发点击验证直接就过了, 但是某些站点强制要求前后 tls 指纹一致的话, 请不要开启该参数, 则破解流程使用的为 chrome 107 指纹
    :param check_tls: 是否检查前后 tls 指纹是否一致
    :param check_proxy: 是否检查前后代理是否一致
    调用示例:
    cracker = CloudFlareCracker(
        href=href,
        user_token="xxx",

        # debug=True,
        # check_useful=True,
        # proxy=proxy,
        # randomtls=False,
        # check_tls=True,  # 获取当前 cf 破解流程使用的 tls 指纹
        # check_proxy=True,
    )
    ret = cracker.crack()
    """
    
    # 必传参数
    must_check_params = ["href"]
    # 默认可选参数
    option_params = {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0",
        "html": "",
        "cookies": {},
        "random_tls": True,
        "check_tls": False,
        "check_proxy": False,
    }

    @staticmethod
    def parse_proxy(proxy):
        _auth, _proxy = None, None
        if proxy:
            _proxy = proxy.split("/")[-1]
            if "@" in _proxy:
                _proxy_split = _proxy.split("@")
                _proxy = _proxy_split[1]
                _auth = tuple(_proxy_split[0].split("/")[-1].split(":"))
        return _proxy, _auth

    def tls_session(self, ja3=None):
        if not hasattr(self, "_tls_session"):
            self._tls_session = pyhttpx.HttpSession(ja3=ja3, http2=True)
        return self._tls_session
    
    def _check_tls(self, tls={}):
        try: 
            ja3_ret = self.session.get('https://tls.peet.ws/api/clean', headers={
                "User-Agent": self.user_agent
            }, timeout=10).json
            node_ja3_hash = tls.get("ja3_hash")
            py_ja3_hash = ja3_ret.get("ja3_hash")
            node_h2_hash = tls.get("akamai_hash")
            py_h2_hash = ja3_ret.get("akamai_hash")
            
            if not self.randomtls:
                node_ja3_hash = 'cd08e31494f9531f560d64c695473da9'
                node_h2_hash = '46cedabdca2073198a42fa10ca4494d0'
            if node_ja3_hash:
                if node_ja3_hash == py_ja3_hash:
                    if self.debug: 
                        logger.success("ja3 指纹一致: {}".format(py_ja3_hash))
                else:
                    if self.debug: 
                        logger.warning("ja3 指纹不一致, node_ja3_hash: {} | py_ja3_hash: {}".format(node_ja3_hash, py_ja3_hash))
            else:
                if self.debug: 
                    logger.warning("未检查 node tls, py ja3 hash => " + py_ja3_hash)

            if node_h2_hash:
                if node_h2_hash == py_h2_hash:
                    if self.debug: 
                        logger.success("h2 指纹一致: {}".format(py_h2_hash))
                else:
                    if self.debug: 
                        logger.warning("h2 指纹不一致, node_h2_hash: {} | py_h2_hash: {}".format(node_h2_hash, py_h2_hash))
            else:
                if self.debug: 
                    logger.warning("未检查 node tls, py h2 hash => " + py_h2_hash)
        except Exception as e:
            if self.debug: 
                logger.warning("检查 tls 出错: {}".format(e.args))
        self.check_tls = False
    
    
    def _check_proxy(self):
        _proxy = self.session.get("https://icanhazip.com", proxies={
            "https": self._proxy
        }, proxy_auth=self._auth).text.strip()
        if _proxy == self._proxy.split(":")[0]:
            if self.debug: 
                logger.success("代理一致")
        else:
            if self.debug: 
                logger.error("代理不一致: {}".format(_proxy))
        self.check_proxy = False
    
    def response(self, result):
        cookies = result.get("cookies") or {}
        self.cookies.update(cookies)
        if self.debug: 
            logger.debug("cookies: {}".format(self.cookies))
        return self.cookies
    
    def check(self, ret):
        verify_type = ret["type"]
        if self.debug: 
            logger.debug(f"触发 {verify_type} 验证")
        # 刷新代理
        proxy_return = ret.get("proxy")
        proxy_recieve = proxy_return.get("recieve")
        if proxy_recieve:
            self.proxy = proxy_recieve
        else:
            self.proxy = proxy_return.get("http")
        self._proxy, self._auth = self.parse_proxy(self.proxy)

        tls = ret.get("tls", {})
        ja3 = tls.get("ja3")
        if not self.random_tls:
            ja3 = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0"    
            # ja3 = '771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21-41,29-23-24,0'
        self.session = self.tls_session(ja3)

        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Dnt': '1',
            'Referer': self.href,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        if self.check_tls:
            self._check_tls(tls)
        if self.check_proxy:
            self._check_proxy()

        try:
            resp = self.session.get(self.href, headers=headers, cookies=self.cookies, timeout=10, proxies={
                "http": self._proxy,
                "https": self._proxy
            }, proxy_auth=self._auth, allow_redirects=False)

            if self.debug: 
                logger.debug("测试状态码: {}".format(resp.status_code))
            if resp.status_code == 403 or "Access denied" in resp.text or "window._cf_chl_opt" in resp.text:
                if self.debug: 
                    logger.warning("cookie 不可用, 请检查代理是否一致, 或者该网站强制 tls 指纹一致, 请开启 check_tls 选项获取 ja3 指纹, 然后使用可自定义 ja3 指纹的请求客户端")
            elif "__CF$cv$params" in resp.text:
                if self.debug: 
                    logger.warning("继续触发 cloudfalre alpha 验证")
                self.wanda_args["html"] = resp.text
                return self.crack()
            else:
                return True
        except Exception as e:
            if self.debug: 
                logger.error(e)   
            
        return False

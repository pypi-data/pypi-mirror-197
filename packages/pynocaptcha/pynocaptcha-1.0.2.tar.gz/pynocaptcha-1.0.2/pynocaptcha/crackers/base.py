
import requests
from loguru import logger
from typing import Any


class BaseCracker:
    
    # 破解器
    cracker_name = "base"
    
    # 破解版本
    cracker_version = "universal"
    
    # 必须参数列表
    must_check_params = []
    
    # 可选参数
    option_params = {}
    
    def __init__(
        self,    
        user_token: str = None,
        developer_token: str = "",   
        user_agent: str = "",
        proxy: str = None, 
        timeout: int = 30,
        debug: bool = False,  
        check_useful: bool = False,
        **kwargs
    ) -> None:
        """
        :param user_token: nocaptcha.io 用户 token
        :param developer_token: nocaptcha.io 用户上级代理 token
        :param user_agent: 请求流程使用 ua
        :param proxy: 请求流程代理, 不传默认使用系统代理, 某些强制要求代理一致或者特定区域的站点请传代理, 支持协议 http/https/socks5, 代理格式: {protocol}://{ip}:{port}（如有账号验证：{protocol}://{user}:{password}@{ip}:{port}）
        :param timeout: 破解接口超时时间(秒)
        :param debug: 是否开启 debug 模式
        :param check_useful: 检查破解是否成功
        """
        self.user_token = user_token
        if not self.user_token:
            raise Exception("缺少用户 token")
        self.developer_token = developer_token
        self.user_agent = user_agent
        self.proxy = proxy
        self.timeout = timeout
        self.debug = debug
        self.check_useful = check_useful

        self.wanda_args = {}
        for k in self.must_check_params:
            v = kwargs.get(k)
            setattr(self, k, v)
            self.wanda_args.update({ k: v })
        for k, v in self.option_params.items():
            _v = kwargs.get(k, v)
            setattr(self, k, _v)
            self.wanda_args.update({ k: _v })

    def response(self, result: Any):
        return result
        
    def check(self):
        raise NotImplemented
    
    def crack(self):
        headers = {
            "User-Token": self.user_token
        }
        if self.developer_token:
            headers["Developer-Token"] = self.developer_token
        resp = requests.post(f"http://api.nocaptcha.io/api/wanda/{self.cracker_name}/{self.cracker_version}", headers=headers, json={
            **self.wanda_args,
            "user_agent": self.user_agent,
            "proxy": self.proxy
        }, timeout=self.timeout).json()
        if self.debug:
            logger.info(resp)
        assert resp.get("status") == 1, resp.get("msg")
        wanda_ret = resp.get("data") or {}
        
        ret = self.response(wanda_ret)
        if self.check_useful:
            if self.check(wanda_ret):
                logger.success("破解成功")
            else:
                logger.error("破解失败")
        return ret

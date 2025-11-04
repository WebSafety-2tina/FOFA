"""
FOFA配置管理类
"""
import os
from typing import List, Optional


class FofaConfig:
    """FOFA API配置类"""
    _instance: Optional['FofaConfig'] = None
    
    def __init__(self):
        self.key = ""
        self.max = 10000
        self.size = "1000"
        self.API = "https://fofa.info"
        self.personalInfoAPI = "https://fofa.info/api/v1/info/my?key=%s"
        self.path = "/api/v1/search/next"
        self.TIP_API = "https://api.fofa.info/v1/search/tip?q="
        self.fields = ["host", "title", "ip", "domain", "port", "protocol", "server", "link"]
        self.additionalField: List[str] = []
        self.checkStatus = False
    
    @classmethod
    def getInstance(cls) -> 'FofaConfig':
        """单例模式获取配置实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def setKey(self, key: str):
        """设置API密钥"""
        self.key = key
    
    def setSize(self, size: str):
        """设置查询大小"""
        self.size = size
    
    def setAPI(self, api: str):
        """设置API地址"""
        self.API = api
    
    def getParam(self, isAll: bool = False) -> str:
        """获取查询参数URL"""
        fields_str = ",".join(self.fields + self.additionalField)
        full_param = "&full=true" if isAll else ""
        return f"{self.API}{self.path}?key={self.key}{full_param}&size={self.size}&fields={fields_str}&qbase64="


class ProxyConfig:
    """代理配置类"""
    _instance: Optional['ProxyConfig'] = None
    
    class ProxyType:
        HTTP = "HTTP"
        SOCKS5 = "SOCKS5"
    
    def __init__(self):
        self.status = False
        self.proxy_type = self.ProxyType.HTTP
        self.proxy_ip = ""
        self.proxy_port = ""
        self.proxy_user = ""
        self.proxy_password = ""
    
    @classmethod
    def getInstance(cls) -> 'ProxyConfig':
        """单例模式获取代理配置实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def getProxyDict(self) -> Optional[dict]:
        """获取代理字典"""
        if not self.status or not self.proxy_ip or not self.proxy_port:
            return None
        
        proxy_url = f"{self.proxy_type.lower()}://"
        if self.proxy_user and self.proxy_password:
            proxy_url += f"{self.proxy_user}:{self.proxy_password}@"
        proxy_url += f"{self.proxy_ip}:{self.proxy_port}"
        
        return {
            "http": proxy_url,
            "https": proxy_url
        }


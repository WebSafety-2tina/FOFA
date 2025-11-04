"""
HTTP请求工具类
"""
import base64
import re
import ssl
import time
import random
import urllib.parse
from typing import Dict, Optional
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
try:
    from requests.packages.urllib3.util.retry import Retry
except ImportError:
    from urllib3.util.retry import Retry
import mmh3  # murmurhash3 for icon hash
from bs4 import BeautifulSoup
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import socket

from main.config import FofaConfig, ProxyConfig


class RequestUtil:
    """请求工具类"""
    _instance: Optional['RequestUtil'] = None
    
    # User-Agent列表
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 Safari/537.36 Edg/88.0.705.22"
    ]
    
    # 证书信息提取正则
    CN_PATTERN = re.compile(r"CommonName:\s([-|*|\w|\.|\s]+)\n\nSubject Public")
    SN_PATTERN = re.compile(r"Serial Number:\s(\d+)\n")
    
    def __init__(self):
        self.config = ProxyConfig.getInstance()
        self.session = self._create_session()
    
    @classmethod
    def getInstance(cls) -> 'RequestUtil':
        """单例模式获取请求工具实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _create_session(self) -> requests.Session:
        """创建带重试机制的session"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """获取随机User-Agent的请求头"""
        return {
            "User-Agent": random.choice(self.USER_AGENTS)
        }
    
    def _get_proxies(self) -> Optional[Dict[str, str]]:
        """获取代理配置"""
        return self.config.getProxyDict()
    
    def getHTML(self, url: str, connectTimeout: int = 120000, readTimeout: int = 120000) -> Dict[str, str]:
        """
        发起HTTP请求获取响应内容
        
        Args:
            url: 请求URL
            connectTimeout: 连接超时时间（毫秒）
            readTimeout: 读取超时时间（毫秒）
        
        Returns:
            {"code": "200/error/其他状态码", "msg": "响应内容或错误信息"}
        """
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                proxies=self._get_proxies(),
                timeout=(connectTimeout / 1000, readTimeout / 1000),
                verify=False  # 忽略SSL证书验证（与Java版本保持一致）
            )
            
            result = {"code": str(response.status_code)}
            
            if response.status_code == 200:
                result["msg"] = response.text
            elif response.status_code == 401:
                result["msg"] = "请求错误状态码401，可能是没有在config中配置有效的key，或者您的账号权限不足无法使用api进行查询。"
            elif response.status_code == 502:
                result["msg"] = "请求错误状态码502，可能是账号限制了每次请求的最大数量，建议尝试修改config中的max_size为100"
            else:
                result["msg"] = f"请求响应错误,状态码{response.status_code}"
            
            return result
        except requests.exceptions.Timeout:
            return {"code": "error", "msg": "请求超时"}
        except requests.exceptions.RequestException as e:
            return {"code": "error", "msg": str(e)}
        except Exception as e:
            return {"code": "error", "msg": str(e)}
    
    def getLeftAmount(self, url: str, connectTimeout: int = 120000, readTimeout: int = 120000) -> Dict[str, str]:
        """获取剩余查询量"""
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                proxies=self._get_proxies(),
                timeout=(connectTimeout / 1000, readTimeout / 1000),
                verify=False
            )
            
            if response.status_code == 200:
                import json
                obj = json.loads(response.text)
                remain_api_query = obj.get("remain_api_query", 0)
                remain_api_data = obj.get("remain_api_data", 0)
                msg = f"剩余查询量: {remain_api_query}  剩余数据量: {remain_api_data}"
                return {"code": "200", "msg": msg}
            else:
                return {"code": str(response.status_code), "msg": response.text}
        except Exception as e:
            return {"code": "error", "msg": str(e)}
    
    def getImageFavicon(self, url: str) -> Optional[Dict[str, str]]:
        """
        提取网站favicon并计算hash（添加安全验证）
        
        Args:
            url: favicon URL
            
        Returns:
            {"code": "200/error", "msg": "icon_hash=\"xxx\"" 或错误信息}
        """
        try:
            # 验证URL格式
            if not url or len(url) > 2048:
                return {"code": "error", "msg": "无效的URL"}
            
            # 验证URL安全性
            parsed = urlparse(url)
            if parsed.scheme not in ['http', 'https']:
                return {"code": "error", "msg": "不支持的协议"}
            
            # 验证URL格式
            parsed = urlparse(url)
            if not parsed.scheme or parsed.scheme not in ['http', 'https']:
                return {"code": "error", "msg": "无效的URL协议"}
            if not parsed.netloc:
                return {"code": "error", "msg": "无效的URL"}
            if len(url) > 2048:  # 防止URL过长攻击
                return {"code": "error", "msg": "URL过长"}
            
            # 注意：verify=False存在安全风险，但为了兼容某些情况，暂时保留
            response = self.session.get(
                url,
                headers=self._get_headers(),
                proxies=self._get_proxies(),
                timeout=(10, 10),  # 减少超时时间
                verify=False,  # 警告：忽略SSL证书验证存在安全风险
                stream=True  # 使用流式下载，避免大文件内存溢出
            )
            
            if response.status_code == 200:
                # 限制文件大小（防止内存溢出）
                max_size = 5 * 1024 * 1024  # 5MB
                content = b""
                for chunk in response.iter_content(chunk_size=8192):
                    content += chunk
                    if len(content) > max_size:
                        return {"code": "error", "msg": "文件过大"}
                
                if len(content) == 0:
                    return {"code": "error", "msg": "无响应内容"}
                
                # Base64编码
                encoded = base64.b64encode(content).decode('utf-8')
                # 计算icon hash (murmurhash3)
                hash_value = self.getIconHash(encoded)
                return {"code": "200", "msg": f'icon_hash="{hash_value}"'}
            else:
                return {"code": "error", "msg": f"HTTP {response.status_code}"}
        except requests.exceptions.Timeout:
            return {"code": "error", "msg": "请求超时"}
        except requests.exceptions.RequestException as e:
            return {"code": "error", "msg": str(e)}
        except Exception as e:
            return {"code": "error", "msg": str(e)}
    
    def getLinkIcon(self, url: str) -> Optional[str]:
        """
        从HTML中提取favicon链接（添加安全验证）
        
        Args:
            url: 网页URL
            
        Returns:
            favicon链接或None
        """
        try:
            # 验证URL格式
            if not url or len(url) > 2048:
                return None
            
            parsed = urlparse(url)
            if parsed.scheme not in ['http', 'https']:
                return None
            
            response = self.session.get(
                url,
                headers=self._get_headers(),
                proxies=self._get_proxies(),
                timeout=(10, 10),  # 减少超时时间
                verify=False,
                stream=True
            )
            
            if response.status_code == 200:
                # 限制HTML大小
                max_size = 10 * 1024 * 1024  # 10MB
                content = b""
                for chunk in response.iter_content(chunk_size=8192):
                    content += chunk
                    if len(content) > max_size:
                        return None
                
                soup = BeautifulSoup(content.decode('utf-8', errors='ignore'), 'html.parser')
                links = soup.find_all('link')
                
                for link in links:
                    rel = link.get('rel', [])
                    if isinstance(rel, list):
                        rel = ' '.join(rel)
                    if rel in ['icon', 'shortcut icon']:
                        href = link.get('href', '')
                        if not href:
                            continue
                        # 验证href长度
                        if len(href) > 2048:
                            continue
                        if href.startswith('http'):
                            return href
                        elif href.startswith('/'):
                            parsed = urlparse(url)
                            return f"{parsed.scheme}://{parsed.netloc}{href}"
                
                return None
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.RequestException:
            return None
        except Exception:
            return None
    
    def getIconHash(self, content: str) -> str:
        """
        计算favicon hash值（murmurhash3）
        
        Args:
            content: Base64编码的favicon内容
            
        Returns:
            hash值字符串
        """
        # 移除\r，添加\n
        content = content.replace('\r', '') + '\n'
        # 使用mmh3计算murmurhash3
        hash_value = mmh3.hash(content.encode('utf-8'))
        # 转换为无符号32位整数
        if hash_value < 0:
            hash_value = hash_value + 2**32
        return str(hash_value)
    
    def getCertSerialNum(self, host: str) -> Optional[str]:
        """
        获取证书序列号（添加安全验证）
        
        Args:
            host: 域名
            
        Returns:
            cert="序列号" 或 None
        """
        try:
            # 验证host格式
            if not host or len(host) > 255:
                return None
            
            # 移除协议前缀
            clean_host = host.replace('https://', '').replace('http://', '').strip()
            if not clean_host:
                return None
            
            # 防止注入攻击：移除危险字符
            dangerous_chars = ['<', '>', '"', "'", '&', '|', ';', '`', '$', '(', ')']
            if any(char in clean_host for char in dangerous_chars):
                return None
            
            # 解析hostname和port
            if ':' in clean_host:
                parts = clean_host.split(':')
                hostname = parts[0]
                try:
                    port = int(parts[1])
                except (ValueError, IndexError):
                    port = 443
            else:
                hostname = clean_host
                port = 443
            
            # 验证hostname格式
            if not hostname or len(hostname) > 253:
                return None
            
            # 验证端口范围
            if port < 1 or port > 65535:
                return None
            
            # 创建SSL上下文
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # 连接到服务器获取证书（设置超时）
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert_der = ssock.getpeercert(True)
                    if not cert_der:
                        return None
                    cert = x509.load_der_x509_certificate(cert_der, default_backend())
                    serial = cert.serial_number
                    return f'cert="{serial}"'
        except (socket.timeout, socket.error):
            return None
        except Exception as e:
            # 记录错误但不抛出
            return None
    
    def getTips(self, key: str) -> Optional[Dict[str, str]]:
        """
        获取自动提示
        
        Args:
            key: 查询关键词
            
        Returns:
            {提示名称: 查询语句} 或 None
        """
        try:
            # 注意：这里需要实现签名逻辑，但Java版本使用了私钥签名
            # 为了简化，这里先返回空，实际使用时需要实现完整的签名逻辑
            ts = str(int(time.time() * 1000))
            encoded_key = urllib.parse.quote(key)
            # 简化版本，实际需要实现RSA签名
            url = f"{FofaConfig.getInstance().TIP_API}{encoded_key}&ts={ts}"
            result = self.getHTML(url, 5000, 10000)
            
            if result.get("code") == "200":
                import json
                obj = json.loads(result["msg"])
                if obj.get("code") == 0:
                    data = {}
                    for item in obj.get("data", []):
                        name = item.get("name", "")
                        company = item.get("company", "")
                        data[f"{name}--{company}"] = f'app="{name}"'
                    return data
            return None
        except Exception as e:
            return None
    
    def encode(self, text: str) -> str:
        """Base64编码字符串"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')


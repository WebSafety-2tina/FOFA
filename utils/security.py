"""
安全工具类 - 修复安全漏洞
"""
import re
import html
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, quote


class SecurityUtil:
    """安全工具类"""
    
    # 输入验证正则
    IP_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    PORT_PATTERN = re.compile(r'^\d{1,5}$')
    DOMAIN_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$')
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000) -> str:
        """
        清理用户输入，防止XSS攻击
        
        Args:
            text: 输入文本
            max_length: 最大长度
            
        Returns:
            清理后的文本
        """
        if not text:
            return ""
        
        # 限制长度
        text = text[:max_length]
        
        # HTML转义
        text = html.escape(text)
        
        # 移除危险字符
        text = re.sub(r'[<>"\']', '', text)
        
        return text.strip()
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """
        验证IP地址格式
        
        Args:
            ip: IP地址
            
        Returns:
            是否为有效IP
        """
        if not ip:
            return False
        
        if not SecurityUtil.IP_PATTERN.match(ip):
            return False
        
        parts = ip.split('.')
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        
        return True
    
    @staticmethod
    def validate_port(port: str) -> bool:
        """
        验证端口号
        
        Args:
            port: 端口号
            
        Returns:
            是否为有效端口
        """
        if not port:
            return False
        
        if not SecurityUtil.PORT_PATTERN.match(port):
            return False
        
        try:
            num = int(port)
            return 1 <= num <= 65535
        except ValueError:
            return False
    
    @staticmethod
    def validate_domain(domain: str) -> bool:
        """
        验证域名格式
        
        Args:
            domain: 域名
            
        Returns:
            是否为有效域名
        """
        if not domain:
            return False
        
        return bool(SecurityUtil.DOMAIN_PATTERN.match(domain))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        验证URL格式
        
        Args:
            url: URL
            
        Returns:
            是否为有效URL
        """
        if not url:
            return False
        
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def safe_path(path: str, base_dir: Optional[Path] = None) -> Optional[Path]:
        """
        验证文件路径，防止路径遍历攻击
        
        Args:
            path: 文件路径
            base_dir: 基础目录
            
        Returns:
            安全路径或None
        """
        try:
            path_obj = Path(path).resolve()
            
            # 检查是否包含危险字符
            if '..' in str(path_obj) or path_obj.is_absolute() and base_dir:
                # 如果指定了基础目录，确保路径在基础目录内
                if base_dir:
                    base_path = Path(base_dir).resolve()
                    try:
                        path_obj.relative_to(base_path)
                    except ValueError:
                        return None
            
            return path_obj
        except Exception:
            return None
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        """
        清理FOFA查询语句，防止注入攻击（增强验证）
        
        Args:
            query: 查询语句
            
        Returns:
            清理后的查询语句
        """
        if not query:
            return ""
        
        # 限制长度（防止DoS攻击）
        if len(query) > 5000:
            query = query[:5000]
        
        # 移除控制字符（保留换行和制表符）
        query = ''.join(char for char in query if ord(char) >= 32 or char in ['\n', '\r', '\t'])
        
        return query.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        清理文件名，防止路径遍历
        
        Args:
            filename: 文件名
            
        Returns:
            清理后的文件名
        """
        if not filename:
            return "file"
        
        # 移除路径分隔符
        filename = filename.replace('/', '_').replace('\\', '_')
        
        # 移除危险字符
        filename = re.sub(r'[<>:"|?*]', '_', filename)
        
        # 限制长度
        if len(filename) > 255:
            filename = filename[:255]
        
        return filename.strip() or "file"


"""
表格数据模型
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TableBean:
    """表格数据Bean"""
    num: int = 0
    host: str = ""
    title: str = ""
    ip: str = ""
    domain: str = ""
    port: int = 0
    protocol: str = ""
    server: str = ""
    lastupdatetime: str = ""
    fid: str = ""
    os: str = ""
    icp: str = ""
    product: str = ""
    certCN: str = ""
    certOrg: str = ""
    status: str = ""
    
    def __eq__(self, other):
        """相等性比较（用于去重）"""
        if not isinstance(other, TableBean):
            return False
        if self is other:
            return True
        
        # 端口相同
        port_match = self.port == other.port
        
        # Host匹配（考虑443和80端口的情况）
        host_match = self.host == other.host
        if port_match:
            if self.port == 443 and (":443" in self.host or ":443" in other.host):
                host_match = True
            if self.port == 80 and (":80" in self.host or ":80" in other.host):
                host_match = True
        
        # IP相同
        ip_match = self.ip == other.ip
        
        return host_match and ip_match and port_match
    
    def __hash__(self):
        """哈希值（用于去重）"""
        return hash((self.ip, self.port))


@dataclass
class ExcelBean:
    """Excel导出数据Bean"""
    host: str = ""
    title: str = ""
    domain: str = ""
    ip: str = ""
    port: int = 0
    protocol: str = ""
    server: str = ""
    lastupdatetime: str = ""
    fid: str = ""
    os: str = ""
    icp: str = ""
    product: str = ""
    certs_subject_org: str = ""
    certs_subject_cn: str = ""
    
    def __eq__(self, other):
        """相等性比较（用于去重）"""
        if not isinstance(other, ExcelBean):
            return False
        if self is other:
            return True
        
        port_match = self.port == other.port
        
        host_match = self.host == other.host
        if port_match:
            if self.port == 443 and (":443" in self.host or ":443" in other.host):
                host_match = True
            if self.port == 80 and (":80" in self.host or ":80" in other.host):
                host_match = True
        
        ip_match = self.ip == other.ip
        
        return host_match and ip_match and port_match
    
    def __hash__(self):
        """哈希值（用于去重）"""
        return hash((self.ip, self.port))


@dataclass
class TabDataBean:
    """Tab页数据Bean"""
    count: int = 0
    total: int = 0
    dataList: set = field(default_factory=set)
    hasMoreData: bool = True
    page: int = 1
    next: Optional[str] = None


"""
Pydantic models for Network Pulse API responses
"""
from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Dict
from datetime import datetime, timezone


def serialize_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to ISO format with Z suffix"""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.isoformat().replace('+00:00', 'Z')
    return dt.isoformat() + 'Z'


class GatewayStats(BaseModel):
    """Gateway health statistics"""
    model: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    uptime: Optional[int] = None  # seconds
    cpu_utilization: Optional[float] = None
    mem_utilization: Optional[float] = None
    wan_status: Optional[str] = None
    wan_ip: Optional[str] = None


class WanHealth(BaseModel):
    """WAN connection health"""
    status: str = "unknown"
    wan_ip: Optional[str] = None
    isp_name: Optional[str] = None
    availability: Optional[float] = None  # percentage
    latency: Optional[float] = None  # ms
    tx_bytes_rate: int = 0
    rx_bytes_rate: int = 0


class APStatus(BaseModel):
    """Access point status"""
    mac: str
    name: str
    model: str
    model_code: Optional[str] = None
    num_sta: int = 0
    user_num_sta: int = 0
    guest_num_sta: int = 0
    channels: Optional[str] = None
    state: int = 0  # 1 = online, 0 = offline
    uptime: int = 0
    satisfaction: Optional[int] = None
    tx_bytes: int = 0
    rx_bytes: int = 0


class TopClient(BaseModel):
    """Top client by bandwidth"""
    mac: str
    name: str
    hostname: Optional[str] = None
    ip: Optional[str] = None
    tx_bytes: int = 0
    rx_bytes: int = 0
    total_bytes: int = 0
    rssi: Optional[int] = None
    is_wired: bool = False
    uptime: Optional[int] = None
    essid: Optional[str] = None
    network: Optional[str] = None
    radio: Optional[str] = None  # "2.4 GHz", "5 GHz", "6 GHz", or None for wired
    ap_mac: Optional[str] = None  # MAC of connected AP


class NetworkHealth(BaseModel):
    """Network subsystem health"""
    wan: Optional[dict] = None
    wan2: Optional[dict] = None
    lan: Optional[dict] = None
    wlan: Optional[dict] = None
    vpn: Optional[dict] = None
    www: Optional[dict] = None


class DeviceCounts(BaseModel):
    """Device counts summary"""
    clients: int = 0
    wired_clients: int = 0
    wireless_clients: int = 0
    aps: int = 0
    switches: int = 0


class ChartData(BaseModel):
    """Aggregated data for dashboard charts"""
    clients_by_band: Dict[str, int] = Field(default_factory=dict)
    clients_by_ssid: Dict[str, int] = Field(default_factory=dict)


class DashboardData(BaseModel):
    """Combined dashboard data response"""
    # Gateway info
    gateway: GatewayStats = Field(default_factory=GatewayStats)

    # WAN health
    wan: WanHealth = Field(default_factory=WanHealth)

    # Device counts
    devices: DeviceCounts = Field(default_factory=DeviceCounts)

    # Current throughput (from health data)
    current_tx_rate: int = 0  # bytes/sec
    current_rx_rate: int = 0  # bytes/sec

    # AP status list
    access_points: List[APStatus] = Field(default_factory=list)

    # Top clients (top 10 by bandwidth for display)
    top_clients: List[TopClient] = Field(default_factory=list)

    # All clients (for AP detail pages and chart aggregation)
    all_clients: List[TopClient] = Field(default_factory=list)

    # Chart data (aggregated client stats)
    chart_data: ChartData = Field(default_factory=ChartData)

    # Network health by subsystem
    health: NetworkHealth = Field(default_factory=NetworkHealth)

    # Metadata
    last_refresh: Optional[datetime] = None
    refresh_interval: int = 60

    @field_serializer('last_refresh')
    def serialize_last_refresh(self, value: Optional[datetime]) -> Optional[str]:
        return serialize_datetime(value)


class SystemStatus(BaseModel):
    """Tool status endpoint response"""
    last_refresh: Optional[datetime] = None
    is_connected: bool = False
    error: Optional[str] = None

    @field_serializer('last_refresh')
    def serialize_last_refresh(self, value: Optional[datetime]) -> Optional[str]:
        return serialize_datetime(value)

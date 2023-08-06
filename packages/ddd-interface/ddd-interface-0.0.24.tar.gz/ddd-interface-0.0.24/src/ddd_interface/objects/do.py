from typing import List, Optional, Dict, Tuple, Union
import datetime
from pydantic import BaseModel



class ConditionDO(BaseModel):
    min_cpu_num: Optional[int] = 1
    max_cpu_num: Optional[int] = 1
    min_memory_size: Optional[int] = 1
    max_memory_size: Optional[int] = 1
    min_gpu_num: Optional[int] = None
    max_gpu_num: Optional[int] = None
    min_gpu_memory_size: Optional[int] = None
    max_gpu_memory_size: Optional[int] = None



class DatapipeServerInfoDO(BaseModel):
    id: str
    secret: str
    endpoint: str



class DatapipeDataInfoDO(BaseModel):
    bucket: str
    remote_path: str
    local_path: str
    timeout: int = 3



class ClusterConfigDataDO(BaseModel):
    data_server: DatapipeServerInfoDO
    data: List[DatapipeDataInfoDO]



class ClusterConfigDO(BaseModel):
    cluster_name: str
    region_id: str
    config_data: Optional[ClusterConfigDataDO] = None
    entry_point: Optional[List[str]] = None
    timeout: int = 20



class BootstrapInfoDO(BaseModel):
    cluster_config: ClusterConfigDO
    template: str = 'normal'
    platform: str = 'aliyun'
    patch_setting: Optional[dict] = None



class RandomTemplateVariablesDO(BaseModel):
    variables: List[str]
    lengths: Optional[List[int]] = None



class FileTemplateVariablesDO(BaseModel):
    variables: Optional[List[str]]
    path: str



class FilesTemplateVariablesDO(BaseModel):
    variables: List[str]
    paths: List[str]



class APIGatewayRequestDO(BaseModel):
    service_name: str
    method: str
    ip: Optional[str] = None
    port: Optional[int] = None
    route: Optional[str] = None
    action: Optional[str] = None
    auth: Optional[dict] = None
    data: Optional[dict] = None



class APIGatewayBlacklistItemDO(BaseModel):
    ip: str
    creation_time: str
    limit_time: int
    limit_reason: str



class TaskRequestDO(BaseModel):
    task_name: str
    region_id: str
    condition: ConditionDO
    git_url: Optional[str]
    git_branch: Optional[str]
    task_type: Optional[str] = 'cluster'
    task_template: Optional[str] = None
    task_env: Optional[dict] = None
    task_command: Optional[List[str]] = ['sleep', '100000']
    task_arg: Optional[List[str]] = None
    task_working_dir: Optional[str] = None
    task_image: Optional[str] = 'alpine:3.12'
    task_start_time: Optional[str] = None
    priority: int = 3
    amount: int = 1
    duration: Optional[int] = None
    disk_size: Optional[int] = 20
    end_style: str = 'delete'
    restart_policy: str = 'never'
    timeout: int = 500
    cluster_name: Optional[str] = None



class TaskDeleteRequestDO(BaseModel):
    task_name: Optional[str]
    task_id: Optional[str]
    delay: Optional[int]



class TaskDetailDO(BaseModel):
    detail_id: str
    ip: str
    node_status: Optional[str]
    job_status: Optional[str]
    exception: Optional[str]



class TaskItemDO(BaseModel):
    request: Optional[TaskRequestDO]
    delete_request: Optional[TaskDeleteRequestDO]
    task_id: str
    creation_time: datetime.datetime
    status: str
    details: Optional[List[TaskDetailDO]]
    entry_time: Optional[datetime.datetime]
    exit_time: Optional[datetime.datetime]
    exception: Optional[str]



class NodeInventoryDO(BaseModel):
    node_type: str
    amount: int



class DNSInventoryDO(BaseModel):
    domain: str
    subdomain: str
    node_type: Optional[str]
    pod_name: Optional[str]
    namespace_name: Optional[str]



class RecoverSettingDO(BaseModel):
    node_inventory: Optional[List[NodeInventoryDO]]
    dns_inventory: Optional[List[DNSInventoryDO]]



class SearchRequestDO(BaseModel):
    keyword: str
    limit: int = 5
    request_id: Optional[str] = None
    others: Optional[dict] = None



class SearchResponseDO(BaseModel):
    status: str
    exception: Optional[str] = None
    result: Optional[dict] = None
    others: Optional[dict] = None



class SearchItemDO(BaseModel):
    item_id: str
    status: str
    exception: Optional[str] = None
    request: Optional[SearchRequestDO] = None
    response: Optional[SearchResponseDO] = None
    entry_time: Optional[datetime.datetime] = None
    exit_time: Optional[datetime.datetime] = None
    create_time: Optional[datetime.datetime] = None
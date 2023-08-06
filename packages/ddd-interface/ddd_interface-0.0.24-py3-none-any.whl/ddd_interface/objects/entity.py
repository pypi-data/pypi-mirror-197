import datetime
from typing import List, Optional, Dict, Tuple, Union
from ..domain.entity import Entity
from .value_obj import (
    K3SNodeType,
    Status,
    UDate,
    UDict,
    UInt,
    UStr
)



class Condition(Entity):
    def __init__(
        self,
        min_cpu_num: Optional[UInt] = 1,
        max_cpu_num: Optional[UInt] = 1,
        min_memory_size: Optional[UInt] = 1,
        max_memory_size: Optional[UInt] = 1,
        min_gpu_num: Optional[UInt] = None,
        max_gpu_num: Optional[UInt] = None,
        min_gpu_memory_size: Optional[UInt] = None,
        max_gpu_memory_size: Optional[UInt] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.min_cpu_num = min_cpu_num
        self.max_cpu_num = max_cpu_num
        self.min_memory_size = min_memory_size
        self.max_memory_size = max_memory_size
        self.min_gpu_num = min_gpu_num
        self.max_gpu_num = max_gpu_num
        self.min_gpu_memory_size = min_gpu_memory_size
        self.max_gpu_memory_size = max_gpu_memory_size



class DatapipeServerInfo(Entity):
    def __init__(
        self,
        id: UStr,
        secret: UStr,
        endpoint: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.id = id
        self.secret = secret
        self.endpoint = endpoint



class DatapipeDataInfo(Entity):
    def __init__(
        self,
        bucket: UStr,
        remote_path: UStr,
        local_path: UStr,
        timeout: UInt = 3,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.bucket = bucket
        self.remote_path = remote_path
        self.local_path = local_path
        self.timeout = timeout



class ClusterConfigData(Entity):
    def __init__(
        self,
        data_server: DatapipeServerInfo,
        data: List[DatapipeDataInfo],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.data_server = data_server
        self.data = data



class ClusterConfig(Entity):
    def __init__(
        self,
        cluster_name: UStr,
        region_id: UStr,
        config_data: Optional[ClusterConfigData] = None,
        entry_point: Optional[List[UStr]] = None,
        timeout: UInt = 20,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.cluster_name = cluster_name
        self.region_id = region_id
        self.config_data = config_data
        self.entry_point = entry_point
        self.timeout = timeout



class BootstrapInfo(Entity):
    def __init__(
        self,
        cluster_config: ClusterConfig,
        template: UStr = 'normal',
        platform: UStr = 'aliyun',
        patch_setting: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.cluster_config = cluster_config
        self.template = template
        self.platform = platform
        self.patch_setting = patch_setting



class RandomTemplateVariables(Entity):
    def __init__(
        self,
        variables: List[UStr],
        lengths: Optional[List[UInt]] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.lengths = lengths



class FileTemplateVariables(Entity):
    def __init__(
        self,
        variables: Optional[List[UStr]],
        path: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.path = path



class FilesTemplateVariables(Entity):
    def __init__(
        self,
        variables: List[UStr],
        paths: List[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.paths = paths



class APIGatewayRequest(Entity):
    def __init__(
        self,
        service_name: UStr,
        method: UStr,
        ip: Optional[UStr] = None,
        port: Optional[UInt] = None,
        route: Optional[UStr] = None,
        action: Optional[UStr] = None,
        auth: Optional[UDict] = None,
        data: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.service_name = service_name
        self.method = method
        self.ip = ip
        self.port = port
        self.route = route
        self.action = action
        self.auth = auth
        self.data = data



class APIGatewayBlacklistItem(Entity):
    def __init__(
        self,
        ip: UStr,
        creation_time: UStr,
        limit_time: UInt,
        limit_reason: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.ip = ip
        self.creation_time = creation_time
        self.limit_time = limit_time
        self.limit_reason = limit_reason



class TaskRequest(Entity):
    def __init__(
        self,
        task_name: UStr,
        region_id: UStr,
        condition: Condition,
        git_url: Optional[UStr],
        git_branch: Optional[UStr],
        task_type: Optional[UStr] = 'cluster',
        task_template: Optional[UStr] = None,
        task_env: Optional[UDict] = None,
        task_command: Optional[List[UStr]] = ['sleep', '100000'],
        task_arg: Optional[List[UStr]] = None,
        task_working_dir: Optional[UStr] = None,
        task_image: Optional[UStr] = 'alpine:3.12',
        task_start_time: Optional[UStr] = None,
        priority: UInt = 3,
        amount: UInt = 1,
        duration: Optional[UInt] = None,
        disk_size: Optional[UInt] = 20,
        end_style: UStr = 'delete',
        restart_policy: UStr = 'never',
        timeout: UInt = 500,
        cluster_name: Optional[UStr] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.task_name = task_name
        self.region_id = region_id
        self.condition = condition
        self.git_url = git_url
        self.git_branch = git_branch
        self.task_type = task_type
        self.task_template = task_template
        self.task_env = task_env
        self.task_command = task_command
        self.task_arg = task_arg
        self.task_working_dir = task_working_dir
        self.task_image = task_image
        self.task_start_time = task_start_time
        self.priority = priority
        self.amount = amount
        self.duration = duration
        self.disk_size = disk_size
        self.end_style = end_style
        self.restart_policy = restart_policy
        self.timeout = timeout
        self.cluster_name = cluster_name



class TaskDeleteRequest(Entity):
    def __init__(
        self,
        task_name: Optional[UStr],
        task_id: Optional[UStr],
        delay: Optional[UInt],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.task_name = task_name
        self.task_id = task_id
        self.delay = delay



class TaskDetail(Entity):
    def __init__(
        self,
        detail_id: UStr,
        ip: UStr,
        node_status: Optional[Status],
        job_status: Optional[Status],
        exception: Optional[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.detail_id = detail_id
        self.ip = ip
        self.node_status = node_status
        self.job_status = job_status
        self.exception = exception



class TaskItem(Entity):
    def __init__(
        self,
        request: Optional[TaskRequest],
        delete_request: Optional[TaskDeleteRequest],
        task_id: UStr,
        creation_time: UDate,
        status: Status,
        details: Optional[List[TaskDetail]],
        entry_time: Optional[UDate],
        exit_time: Optional[UDate],
        exception: Optional[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.request = request
        self.delete_request = delete_request
        self.task_id = task_id
        self.creation_time = creation_time
        self.status = status
        self.details = details
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.exception = exception



class NodeInventory(Entity):
    def __init__(
        self,
        node_type: UStr,
        amount: UInt,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.node_type = node_type
        self.amount = amount



class DNSInventory(Entity):
    def __init__(
        self,
        domain: UStr,
        subdomain: UStr,
        node_type: Optional[K3SNodeType],
        pod_name: Optional[UStr],
        namespace_name: Optional[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.domain = domain
        self.subdomain = subdomain
        self.node_type = node_type
        self.pod_name = pod_name
        self.namespace_name = namespace_name



class RecoverSetting(Entity):
    def __init__(
        self,
        node_inventory: Optional[List[NodeInventory]],
        dns_inventory: Optional[List[DNSInventory]],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.node_inventory = node_inventory
        self.dns_inventory = dns_inventory



class SearchRequest(Entity):
    def __init__(
        self,
        keyword: UStr,
        limit: UInt = 5,
        request_id: Optional[UStr] = None,
        others: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.keyword = keyword
        self.limit = limit
        self.request_id = request_id
        self.others = others



class SearchResponse(Entity):
    def __init__(
        self,
        status: Status,
        exception: Optional[UStr] = None,
        result: Optional[UDict] = None,
        others: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.status = status
        self.exception = exception
        self.result = result
        self.others = others



class SearchItem(Entity):
    def __init__(
        self,
        item_id: UStr,
        status: Status,
        exception: Optional[UStr] = None,
        request: Optional[SearchRequest] = None,
        response: Optional[SearchResponse] = None,
        entry_time: Optional[UDate] = None,
        exit_time: Optional[UDate] = None,
        create_time: Optional[UDate] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.item_id = item_id
        self.status = status
        self.exception = exception
        self.request = request
        self.response = response
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.create_time = create_time
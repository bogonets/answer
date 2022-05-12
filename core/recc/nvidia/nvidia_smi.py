# -*- coding: utf-8 -*-

from io import StringIO
from shutil import which
from typing import List, Optional
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import parse as _xml_parse

from recc.packet.nvidia import (
    Clocks,
    ClocksThrottleReasons,
    Gpu,
    MemoryUsage,
    NvidiaSmiLog,
    ProcessInfo,
    Temperature,
    Utilization,
)
from recc.subprocess.async_subprocess import start_async_subprocess_simply
from recc.variables.nvidia import (
    NVIDIA_SMI_EXECUTABLE_NAME,
    NVIDIA_SMI_QUERY_FLAG,
    NVIDIA_SMI_XML_FORMAT_FLAG,
)


def _t(e: Optional[Element]) -> Optional[str]:
    return e.text if e is not None else None


def parse_element_to_clocks_throttle_reasons(
    e: Optional[Element],
) -> Optional[ClocksThrottleReasons]:
    if e is None:
        return None

    gpu_idle = e.find("clocks_throttle_reason_gpu_idle")
    apps_clocks_setting = e.find("clocks_throttle_reason_applications_clocks_setting")
    sw_power_cap = e.find("clocks_throttle_reason_sw_power_cap")
    hw_slowdown = e.find("clocks_throttle_reason_hw_slowdown")
    hw_thermal_slowdown = e.find("clocks_throttle_reason_hw_thermal_slowdown")
    hw_power_brake_slowdown = e.find("clocks_throttle_reason_hw_power_brake_slowdown")
    sync_boost = e.find("clocks_throttle_reason_sync_boost")
    sw_thermal_slowdown = e.find("clocks_throttle_reason_sw_thermal_slowdown")
    display_clocks_setting = e.find("clocks_throttle_reason_display_clocks_setting")

    return ClocksThrottleReasons(
        _t(gpu_idle),
        _t(apps_clocks_setting),
        _t(sw_power_cap),
        _t(hw_slowdown),
        _t(hw_thermal_slowdown),
        _t(hw_power_brake_slowdown),
        _t(sync_boost),
        _t(sw_thermal_slowdown),
        _t(display_clocks_setting),
    )


def parse_element_to_memory_usage(e: Optional[Element]) -> Optional[MemoryUsage]:
    if e is None:
        return None

    total = e.find("total")
    used = e.find("used")
    free = e.find("free")

    return MemoryUsage(
        _t(total),
        _t(used),
        _t(free),
    )


def parse_element_to_utilization(e: Optional[Element]) -> Optional[Utilization]:
    if e is None:
        return None

    gpu_util = e.find("gpu_util")
    memory_util = e.find("memory_util")
    encoder_util = e.find("encoder_util")
    decoder_util = e.find("decoder_util")

    return Utilization(
        _t(gpu_util),
        _t(memory_util),
        _t(encoder_util),
        _t(decoder_util),
    )


def parse_element_to_temperature(e: Optional[Element]) -> Optional[Temperature]:
    if e is None:
        return None

    gpu_temp = e.find("gpu_temp")
    gpu_temp_max_threshold = e.find("gpu_temp_max_threshold")
    gpu_temp_slow_threshold = e.find("gpu_temp_slow_threshold")
    gpu_temp_max_gpu_threshold = e.find("gpu_temp_max_gpu_threshold")
    gpu_target_temperature = e.find("gpu_target_temperature")
    memory_temp = e.find("memory_temp")
    gpu_temp_max_mem_threshold = e.find("gpu_temp_max_mem_threshold")

    return Temperature(
        _t(gpu_temp),
        _t(gpu_temp_max_threshold),
        _t(gpu_temp_slow_threshold),
        _t(gpu_temp_max_gpu_threshold),
        _t(gpu_target_temperature),
        _t(memory_temp),
        _t(gpu_temp_max_mem_threshold),
    )


def parse_element_to_clocks(e: Optional[Element]) -> Optional[Clocks]:
    if e is None:
        return None

    graphics_clock = e.find("graphics_clock")
    sm_clock = e.find("sm_clock")
    mem_clock = e.find("mem_clock")
    video_clock = e.find("video_clock")

    return Clocks(
        _t(graphics_clock),
        _t(sm_clock),
        _t(mem_clock),
        _t(video_clock),
    )


def parse_element_to_process_info(e: Element) -> ProcessInfo:
    gpu_instance_id = e.find("gpu_instance_id")
    compute_instance_id = e.find("compute_instance_id")
    pid = e.find("pid")
    type_ = e.find("type")
    process_name = e.find("process_name")
    used_memory = e.find("used_memory")

    return ProcessInfo(
        _t(gpu_instance_id),
        _t(compute_instance_id),
        _t(pid),
        _t(type_),
        _t(process_name),
        _t(used_memory),
    )


def parse_element_to_gpu(e: Element) -> Gpu:
    product_name = e.find("product_name")
    product_brand = e.find("product_brand")
    display_mode = e.find("display_mode")
    display_active = e.find("display_active")
    persistence_mode = e.find("persistence_mode")
    uuid = e.find("uuid")
    fan_speed = e.find("fan_speed")
    performance_state = e.find("performance_state")
    clocks_throttle_reasons = e.find("clocks_throttle_reasons")
    fb_memory_usage = e.find("fb_memory_usage")
    bar1_memory_usage = e.find("bar1_memory_usage")
    compute_mode = e.find("compute_mode")
    utilization = e.find("utilization")
    temperature = e.find("temperature")
    clocks = e.find("clocks")
    max_clocks = e.find("max_clocks")
    processes = e.find("processes")

    process_infos: List[ProcessInfo] = list()
    if processes is not None:
        for process_info in processes.findall("process_info"):
            process_infos.append(parse_element_to_process_info(process_info))

    return Gpu(
        _t(product_name),
        _t(product_brand),
        _t(display_mode),
        _t(display_active),
        _t(persistence_mode),
        _t(uuid),
        _t(fan_speed),
        _t(performance_state),
        parse_element_to_clocks_throttle_reasons(clocks_throttle_reasons),
        parse_element_to_memory_usage(fb_memory_usage),
        parse_element_to_memory_usage(bar1_memory_usage),
        _t(compute_mode),
        parse_element_to_utilization(utilization),
        parse_element_to_temperature(temperature),
        parse_element_to_clocks(clocks),
        parse_element_to_clocks(max_clocks),
        process_infos,
    )


def parse_nvidia_smi_query(xml: str) -> NvidiaSmiLog:
    tree = _xml_parse(StringIO(xml))
    root = tree.getroot()
    if root.tag != "nvidia_smi_log":
        raise ValueError("The root tag must be `nvidia_smi_log`")

    timestamp = root.find("timestamp")
    driver_version = root.find("driver_version")
    cuda_version = root.find("cuda_version")
    attached_gpus = root.find("attached_gpus")
    gpu = [parse_element_to_gpu(g) for g in root.findall("gpu")]

    return NvidiaSmiLog(
        _t(timestamp),
        _t(driver_version),
        _t(cuda_version),
        _t(attached_gpus),
        gpu,
    )


def find_nvidia_smi_executable() -> str:
    path = which(NVIDIA_SMI_EXECUTABLE_NAME)
    if path is not None:
        return path
    raise FileNotFoundError(f"Not found `{NVIDIA_SMI_EXECUTABLE_NAME}` executable")


def exists_nvidia_smi_executable() -> bool:
    try:
        return bool(find_nvidia_smi_executable())
    except FileNotFoundError:
        return False


async def nvidia_smi_query(encoding="utf-8") -> NvidiaSmiLog:
    nvidia_smi = find_nvidia_smi_executable()

    code, stdout, stderr = await start_async_subprocess_simply(
        nvidia_smi, NVIDIA_SMI_QUERY_FLAG, NVIDIA_SMI_XML_FORMAT_FLAG
    )

    if code != 0:
        stdout_msg = stdout.decode(encoding=encoding)
        stderr_msg = stderr.decode(encoding=encoding)
        params = f"code={code},stdout='{stdout_msg}',stderr='{stderr_msg}'"
        raise RuntimeError(f"nvidia-smi query failed ({params})")

    return parse_nvidia_smi_query(stdout.decode(encoding=encoding))

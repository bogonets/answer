# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ClocksThrottleReasons:
    clocks_throttle_reason_gpu_idle: Optional[str]
    clocks_throttle_reason_applications_clocks_setting: Optional[str]
    clocks_throttle_reason_sw_power_cap: Optional[str]
    clocks_throttle_reason_hw_slowdown: Optional[str]
    clocks_throttle_reason_hw_thermal_slowdown: Optional[str]
    clocks_throttle_reason_hw_power_brake_slowdown: Optional[str]
    clocks_throttle_reason_sync_boost: Optional[str]
    clocks_throttle_reason_sw_thermal_slowdown: Optional[str]
    clocks_throttle_reason_display_clocks_setting: Optional[str]


@dataclass
class MemoryUsage:
    total: Optional[str]
    used: Optional[str]
    free: Optional[str]


@dataclass
class Utilization:
    gpu_util: Optional[str]
    memory_util: Optional[str]
    encoder_util: Optional[str]
    decoder_util: Optional[str]


@dataclass
class Temperature:
    gpu_temp: Optional[str]
    gpu_temp_max_threshold: Optional[str]
    gpu_temp_slow_threshold: Optional[str]
    gpu_temp_max_gpu_threshold: Optional[str]
    gpu_target_temperature: Optional[str]
    memory_temp: Optional[str]
    gpu_temp_max_mem_threshold: Optional[str]


@dataclass
class Clocks:
    graphics_clock: Optional[str]
    sm_clock: Optional[str]
    mem_clock: Optional[str]
    video_clock: Optional[str]


@dataclass
class ProcessInfo:
    gpu_instance_id: Optional[str]
    compute_instance_id: Optional[str]
    pid: Optional[str]
    type: Optional[str]
    process_name: Optional[str]
    used_memory: Optional[str]


@dataclass
class Gpu:
    product_name: Optional[str]
    product_brand: Optional[str]
    display_mode: Optional[str]
    display_active: Optional[str]
    persistence_mode: Optional[str]
    # mig_mode
    # mig_devices
    # accounting_mode
    # accounting_mode_buffer_size
    # driver_model
    # serial
    uuid: Optional[str]
    # minor_number
    # vbios_version
    # multigpu_board
    # board_id
    # gpu_part_number
    # gpu_module_id
    # inforom_version
    # gpu_operation_mode
    # gsp_firmware_version
    # gpu_virtualization_mode
    # ibmnpu
    # pci
    fan_speed: Optional[str]
    performance_state: Optional[str]
    clocks_throttle_reasons: Optional[ClocksThrottleReasons]
    fb_memory_usage: Optional[MemoryUsage]
    bar1_memory_usage: Optional[MemoryUsage]
    compute_mode: Optional[str]
    utilization: Optional[Utilization]
    # encoder_stats
    # fbc_stats
    # ecc_mode
    # ecc_errors
    # retired_pages
    # remapped_rows
    temperature: Optional[Temperature]
    # supported_gpu_target_temp
    # power_readings
    clocks: Optional[Clocks]
    # applications_clocks
    # default_applications_clocks
    max_clocks: Optional[Clocks]
    # max_customer_boost_clocks
    # clock_policy
    # voltage
    # supported_clocks
    processes: List[ProcessInfo]
    # accounted_processes


@dataclass
class NvidiaSmiLog:
    timestamp: Optional[str]
    driver_version: Optional[str]
    cuda_version: Optional[str]
    attached_gpus: Optional[str]
    gpu: List[Gpu]

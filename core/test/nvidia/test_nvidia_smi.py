# -*- coding: utf-8 -*-

from unittest import TestCase, main
from tester.samples.read_samples import read_sample
from recc.nvidia.nvidia_smi import parse_nvidia_smi_query


class NvidiaSmiTestCase(TestCase):
    def test_parse_nvidia_smi_query(self):
        xml = read_sample("nvidia_smi_470.57.02_query.xml")
        log = parse_nvidia_smi_query(xml)

        self.assertEqual("Fri Mar  4 13:44:51 2022", log.timestamp)
        self.assertEqual("470.57.02", log.driver_version)
        self.assertEqual("2", log.attached_gpus)
        self.assertEqual(2, len(log.gpu))

        gpu0 = log.gpu[0]
        gpu1 = log.gpu[1]
        c0 = gpu0.clocks_throttle_reasons
        c1 = gpu1.clocks_throttle_reasons
        t0 = gpu0.temperature
        t1 = gpu1.temperature

        # fmt: off
        self.assertEqual("NVIDIA GeForce RTX 3070 Ti", gpu0.product_name)
        self.assertEqual("GeForce", gpu0.product_brand)
        self.assertEqual("Disabled", gpu0.display_mode)
        self.assertEqual("Disabled", gpu0.display_active)
        self.assertEqual("Enabled", gpu0.persistence_mode)
        self.assertEqual("GPU-1234567890-1", gpu0.uuid)
        self.assertEqual("0 %", gpu0.fan_speed)
        self.assertEqual("P8", gpu0.performance_state)
        self.assertEqual("Active", c0.clocks_throttle_reason_gpu_idle)
        self.assertEqual("Not Active", c0.clocks_throttle_reason_applications_clocks_setting)  # noqa
        self.assertEqual("Not Active", c0.clocks_throttle_reason_sw_power_cap)
        self.assertEqual("Not Active", c0.clocks_throttle_reason_hw_slowdown)
        self.assertEqual("Not Active", c0.clocks_throttle_reason_hw_thermal_slowdown)
        self.assertEqual("Not Active", c0.clocks_throttle_reason_hw_power_brake_slowdown)  # noqa
        self.assertEqual("Not Active", c0.clocks_throttle_reason_sync_boost)
        self.assertEqual("Not Active", c0.clocks_throttle_reason_sw_thermal_slowdown)
        self.assertEqual("Not Active", c0.clocks_throttle_reason_display_clocks_setting)
        self.assertEqual("7982 MiB", gpu0.fb_memory_usage.total)
        self.assertEqual("2069 MiB", gpu0.fb_memory_usage.used)
        self.assertEqual("5913 MiB", gpu0.fb_memory_usage.free)
        self.assertEqual("256 MiB", gpu0.bar1_memory_usage.total)
        self.assertEqual("5 MiB", gpu0.bar1_memory_usage.used)
        self.assertEqual("251 MiB", gpu0.bar1_memory_usage.free)
        self.assertEqual("Default", gpu0.compute_mode)
        self.assertEqual("0 %", gpu0.utilization.gpu_util)
        self.assertEqual("0 %", gpu0.utilization.memory_util)
        self.assertEqual("0 %", gpu0.utilization.encoder_util)
        self.assertEqual("0 %", gpu0.utilization.decoder_util)
        self.assertEqual("44 C", t0.gpu_temp)
        self.assertEqual("98 C", t0.gpu_temp_max_threshold)
        self.assertEqual("95 C", t0.gpu_temp_slow_threshold)
        self.assertEqual("93 C", t0.gpu_temp_max_gpu_threshold)
        self.assertEqual("83 C", t0.gpu_target_temperature)
        self.assertEqual("N/A", t0.memory_temp)
        self.assertEqual("N/A", t0.gpu_temp_max_mem_threshold)
        self.assertEqual("210 MHz", gpu0.clocks.graphics_clock)
        self.assertEqual("210 MHz", gpu0.clocks.sm_clock)
        self.assertEqual("405 MHz", gpu0.clocks.mem_clock)
        self.assertEqual("555 MHz", gpu0.clocks.video_clock)
        self.assertEqual("2130 MHz", gpu0.max_clocks.graphics_clock)
        self.assertEqual("2130 MHz", gpu0.max_clocks.sm_clock)
        self.assertEqual("9501 MHz", gpu0.max_clocks.mem_clock)
        self.assertEqual("1950 MHz", gpu0.max_clocks.video_clock)
        self.assertEqual(2, len(gpu0.processes))
        self.assertEqual("N/A", gpu0.processes[0].gpu_instance_id)
        self.assertEqual("N/A", gpu0.processes[0].compute_instance_id)
        self.assertEqual("1111", gpu0.processes[0].pid)
        self.assertEqual("G", gpu0.processes[0].type)
        self.assertEqual("/usr/lib/xorg/Xorg", gpu0.processes[0].process_name)
        self.assertEqual("4 MiB", gpu0.processes[0].used_memory)
        self.assertEqual("N/A", gpu0.processes[1].gpu_instance_id)
        self.assertEqual("N/A", gpu0.processes[1].compute_instance_id)
        self.assertEqual("0000", gpu0.processes[1].pid)
        self.assertEqual("C", gpu0.processes[1].type)
        self.assertEqual("/usr/local/python", gpu0.processes[1].process_name)
        self.assertEqual("2061 MiB", gpu0.processes[1].used_memory)

        self.assertEqual("NVIDIA GeForce RTX 3070 Ti", gpu1.product_name)
        self.assertEqual("GeForce", gpu1.product_brand)
        self.assertEqual("Disabled", gpu1.display_mode)
        self.assertEqual("Disabled", gpu1.display_active)
        self.assertEqual("Enabled", gpu1.persistence_mode)
        self.assertEqual("GPU-1234567890-2", gpu1.uuid)
        self.assertEqual("0 %", gpu1.fan_speed)
        self.assertEqual("P8", gpu1.performance_state)
        self.assertEqual("Active", c1.clocks_throttle_reason_gpu_idle)
        self.assertEqual("Not Active", c1.clocks_throttle_reason_applications_clocks_setting)  # noqa
        self.assertEqual("Not Active", c1.clocks_throttle_reason_sw_power_cap)
        self.assertEqual("Not Active", c1.clocks_throttle_reason_hw_slowdown)
        self.assertEqual("Not Active", c1.clocks_throttle_reason_hw_thermal_slowdown)
        self.assertEqual("Not Active", c1.clocks_throttle_reason_hw_power_brake_slowdown)  # noqa
        self.assertEqual("Not Active", c1.clocks_throttle_reason_sync_boost)
        self.assertEqual("Not Active", c1.clocks_throttle_reason_sw_thermal_slowdown)
        self.assertEqual("Not Active", c1.clocks_throttle_reason_display_clocks_setting)
        self.assertEqual("7982 MiB", gpu1.fb_memory_usage.total)
        self.assertEqual("8 MiB", gpu1.fb_memory_usage.used)
        self.assertEqual("7974 MiB", gpu1.fb_memory_usage.free)
        self.assertEqual("256 MiB", gpu1.bar1_memory_usage.total)
        self.assertEqual("3 MiB", gpu1.bar1_memory_usage.used)
        self.assertEqual("253 MiB", gpu1.bar1_memory_usage.free)
        self.assertEqual("Default", gpu1.compute_mode)
        self.assertEqual("0 %", gpu1.utilization.gpu_util)
        self.assertEqual("0 %", gpu1.utilization.memory_util)
        self.assertEqual("0 %", gpu1.utilization.encoder_util)
        self.assertEqual("0 %", gpu1.utilization.decoder_util)
        self.assertEqual("37 C", t1.gpu_temp)
        self.assertEqual("98 C", t1.gpu_temp_max_threshold)
        self.assertEqual("95 C", t1.gpu_temp_slow_threshold)
        self.assertEqual("93 C", t1.gpu_temp_max_gpu_threshold)
        self.assertEqual("83 C", t1.gpu_target_temperature)
        self.assertEqual("N/A", t1.memory_temp)
        self.assertEqual("N/A", t1.gpu_temp_max_mem_threshold)
        self.assertEqual("210 MHz", gpu1.clocks.graphics_clock)
        self.assertEqual("210 MHz", gpu1.clocks.sm_clock)
        self.assertEqual("405 MHz", gpu1.clocks.mem_clock)
        self.assertEqual("555 MHz", gpu1.clocks.video_clock)
        self.assertEqual("2130 MHz", gpu1.max_clocks.graphics_clock)
        self.assertEqual("2130 MHz", gpu1.max_clocks.sm_clock)
        self.assertEqual("9501 MHz", gpu1.max_clocks.mem_clock)
        self.assertEqual("1950 MHz", gpu1.max_clocks.video_clock)
        self.assertEqual(1, len(gpu1.processes))
        self.assertEqual("N/A", gpu1.processes[0].gpu_instance_id)
        self.assertEqual("N/A", gpu1.processes[0].compute_instance_id)
        self.assertEqual("2222", gpu1.processes[0].pid)
        self.assertEqual("G", gpu1.processes[0].type)
        self.assertEqual("/usr/lib/xorg/Xorg", gpu1.processes[0].process_name)
        self.assertEqual("4 MiB", gpu1.processes[0].used_memory)
        # fmt: on


if __name__ == "__main__":
    main()

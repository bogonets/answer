export interface ClocksThrottleReasons {
  clocks_throttle_reason_gpu_idle?: string;
  clocks_throttle_reason_applications_clocks_setting?: string;
  clocks_throttle_reason_sw_power_cap?: string;
  clocks_throttle_reason_hw_slowdown?: string;
  clocks_throttle_reason_hw_thermal_slowdown?: string;
  clocks_throttle_reason_hw_power_brake_slowdown?: string;
  clocks_throttle_reason_sync_boost?: string;
  clocks_throttle_reason_sw_thermal_slowdown?: string;
  clocks_throttle_reason_display_clocks_setting?: string;
}

export interface MemoryUsage {
  total?: string;
  used?: string;
  free?: string;
}

export interface Utilization {
  gpu_util?: string;
  memory_util?: string;
  encoder_util?: string;
  decoder_util?: string;
}

export interface Temperature {
  gpu_temp?: string;
  gpu_temp_max_threshold?: string;
  gpu_temp_slow_threshold?: string;
  gpu_temp_max_gpu_threshold?: string;
  gpu_target_temperature?: string;
  memory_temp?: string;
  gpu_temp_max_mem_threshold?: string;
}

export interface Clocks {
  graphics_clock?: string;
  sm_clock?: string;
  mem_clock?: string;
  video_clock?: string;
}

export interface ProcessInfo {
  gpu_instance_id?: string;
  compute_instance_id?: string;
  pid?: string;
  type?: string;
  process_name?: string;
  used_memory?: string;
}

export interface Gpu {
  product_name?: string;
  product_brand?: string;
  display_mode?: string;
  display_active?: string;
  persistence_mode?: string;
  uuid?: string;
  fan_speed?: string;
  performance_state?: string;
  clocks_throttle_reasons?: ClocksThrottleReasons;
  fb_memory_usage?: MemoryUsage;
  bar1_memory_usage?: MemoryUsage;
  compute_mode?: string;
  utilization?: Utilization;
  temperature?: Temperature;
  clocks?: Clocks;
  max_clocks?: Clocks;
  processes: Array<ProcessInfo>;
}

export interface NvidiaSmiLog {
  timestamp?: string;
  driver_version?: string;
  cuda_version?: string;
  attached_gpus?: number;
  gpu: Array<Gpu>;
}

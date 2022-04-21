export interface VmsLayoutA {
  layout_uid: number;
  group_slug: string;
  project_slug: string;
  name: string;
  description: string;
  index: number;
  device_uid: number;
  created_at: string;
  updated_at: string;
}

export interface VmsCreateLayoutQ {
  name: string;
  description: string;
  index: number;
  device_uid: number;
}

export interface VmsUpdateLayoutQ {
  group_slug?: string;
  project_slug?: string;
  name?: string;
  description?: string;
  index?: number;
  device_uid?: number;
}

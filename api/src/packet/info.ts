export interface InfoA {
  key: string;
  value?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CreateInfoQ {
  key: string;
  value: string;
}

export interface UpdateInfoQ {
  value: string;
}

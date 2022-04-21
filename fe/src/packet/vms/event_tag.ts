export interface VmsEventTagA {
  event_uid: number;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface VmsCreateEventTagQ {
  event_uid: number;
  description: string;
}

export interface VmsUpdateEventTagQ {
  description?: string;
}

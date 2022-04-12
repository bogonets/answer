export interface GroupA {
  slug: string;
  name?: string;
  description?: string;
  features?: Array<string>;
  visibility?: number;
  extra?: any; // eslint-disable-line @typescript-eslint/no-explicit-any
  created_at?: string;
  updated_at?: string;
}

export interface CreateGroupQ {
  slug: string;
  name?: string;
  description?: string;
  features?: Array<string>;
  visibility?: number;
  extra?: any; // eslint-disable-line @typescript-eslint/no-explicit-any
}

export interface UpdateGroupQ {
  name?: string;
  description?: string;
  features?: Array<string>;
  visibility?: number;
  extra?: any; // eslint-disable-line @typescript-eslint/no-explicit-any
}

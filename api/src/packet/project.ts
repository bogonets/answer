export interface ProjectA {
  group_slug: string;
  project_slug: string;
  name?: string;
  description?: string;
  features?: Array<string>;
  visibility?: number;
  extra?: any; // eslint-disable-line @typescript-eslint/no-explicit-any
  created_at?: string;
  updated_at?: string;
}

export interface CreateProjectQ {
  group_slug: string;
  project_slug: string;
  name?: string;
  description?: string;
  features?: Array<string>;
  visibility?: number;
  extra?: any; // eslint-disable-line @typescript-eslint/no-explicit-any
}

export interface UpdateProjectQ {
  name?: string;
  description?: string;
  features?: Array<string>;
  visibility?: number;
  extra?: any; // eslint-disable-line @typescript-eslint/no-explicit-any
}

export interface ProjectOverviewA {
  layouts?: number;
  tables?: number;
  tasks?: number;
  members?: number;
}

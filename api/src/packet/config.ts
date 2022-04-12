export interface ConfigA {
  key: string;
  type: string;
  value: string;
}

export function newConfigA(key?: string, type?: string, value?: string) {
  return {
    key: key ?? '',
    type: type ?? '',
    value: value ?? '',
  } as ConfigA;
}

export interface UpdateConfigValueQ {
  value: string;
}

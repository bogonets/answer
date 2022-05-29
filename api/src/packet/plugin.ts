export interface PluginMenuA {
  icon: string;
  name: string;
  path: string;
  translations: Record<string, string>;
  permission: string;
}

export interface PluginMenusA {
  admin: Array<PluginMenuA>;
  group: Array<PluginMenuA>;
  project: Array<PluginMenuA>;
  user: Array<PluginMenuA>;
}

export interface PluginA {
  name: string;
  menus: PluginMenusA;
}

export interface PluginNameA {
  name: string;
}

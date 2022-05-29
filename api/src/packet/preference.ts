import type {PluginA} from './plugin';

export interface PreferenceA {
  oem: string;
  plugins: Array<PluginA>;
}

export function newPreference(oem?: string, plugins?: Array<PluginA>) {
  return {
    oem: oem ?? '',
    plugins: plugins ?? [],
  } as PreferenceA;
}

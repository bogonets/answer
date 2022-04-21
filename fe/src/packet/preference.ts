export const OEM_AIRJOY = 'airjoy';

export interface PreferenceA {
  oem: string;
}

export function createEmptyPreference() {
  return {
    oem: '',
  } as PreferenceA;
}

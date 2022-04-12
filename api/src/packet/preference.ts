export const OEM_AIRJOY = 'airjoy';

export interface PreferenceA {
  oem: string;
}

export function newPreference(oem?: string) {
  return {
    oem: oem ?? '',
  } as PreferenceA;
}

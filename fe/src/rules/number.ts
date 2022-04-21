import i18n from '@/translations';

const INTEGER_REGEX = /^[0-9][0-9]*$/;

export function isInteger(value): boolean {
  return INTEGER_REGEX.test(value);
}

export default function integerField(value): boolean | string {
  return isInteger(value) || i18n.t('rules.integer').toString();
}

import i18n from '@/translations';

export default function requiredField(value): boolean | string {
  return !!value || i18n.t('rules.required').toString();
}

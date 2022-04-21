import i18n from '@/translations';

const SLUG_FORMAT_REGEX = /^[a-zA-Z0-9_-]+$/;

export function isSlugFormat(value): boolean {
  return SLUG_FORMAT_REGEX.test(value);
}

export default function slugFormat(value): boolean | string {
  return isSlugFormat(value) || i18n.t('rules.slug').toString();
}

import i18n from '@/translations';

export default function atLeast4Char(value): boolean | string {
    return (value && value.length >= 4) || i18n.t('rules.at_least_4char').toString();
}

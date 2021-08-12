import i18n from '@/translations';

const ERROR_RULES_AT_LEAST_4CHAR = i18n.t('rules.at_least_4char').toString();

export default function atLeast4Char(value): boolean | string {
    return (value && value.length >= 4) || ERROR_RULES_AT_LEAST_4CHAR;
}

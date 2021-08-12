import i18n from '@/translations';

const RECC_REGEX = /^[Rr][Ee][Cc][Cc]\..*/;
const ERROR_RULES_NO_RECC_PREFIX = i18n.t('rules.no_recc_prefix').toString();

export function isReccKey(value): boolean {
    return RECC_REGEX.test(value);
}

export default function noReccPrefix(value): boolean | string {
    return !isReccKey(value) || ERROR_RULES_NO_RECC_PREFIX;
}

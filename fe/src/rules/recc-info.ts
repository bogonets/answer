import i18n from '@/translations';

const RECC_REGEX = /^[Rr][Ee][Cc][Cc]\..*/;

export function isReccKey(value): boolean {
    return RECC_REGEX.test(value);
}

export default function noReccPrefix(value): boolean | string {
    return !isReccKey(value) || i18n.t('rules.no_recc_prefix').toString();
}

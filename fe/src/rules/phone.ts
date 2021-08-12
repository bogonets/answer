import i18n from '@/translations';

const PHONE_FORMAT_REGEX = /^[-+0-9]+$/;
const ERROR_RULES_PHONE = i18n.t('rules.phone').toString();

export function isPhoneFormat(value): boolean {
    return PHONE_FORMAT_REGEX.test(value);
}

export default function emptyOrPhoneFormat(value): boolean | string {
    if (!value) {
        return true;
    }
    return isPhoneFormat(value) || ERROR_RULES_PHONE;
}

import i18n from '@/translations';

const EMAIL_FORMAT_REGEX = /^\S+@\S+\.\S+$/;
const ERROR_RULES_EMAIL = i18n.t('rules.email').toString();

export function isEmailFormat(value): boolean {
    return EMAIL_FORMAT_REGEX.test(value);
}

export default function emptyOrEmailFormat(value): boolean | string {
    if (!value) {
        return true;
    }
    return isEmailFormat(value) || ERROR_RULES_EMAIL;
}

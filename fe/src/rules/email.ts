import i18n from '@/translations';

const EMAIL_FORMAT_REGEX = /^\S+@\S+\.\S+$/;

export function isEmailFormat(value): boolean {
    return EMAIL_FORMAT_REGEX.test(value);
}

export default function emptyOrEmailFormat(value): boolean | string {
    if (!value) {
        return true;
    }
    return isEmailFormat(value) || i18n.t('rules.email').toString();
}

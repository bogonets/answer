import atLeast4Char from '@/rules/at-least';
import emptyOrEmailFormat from '@/rules/email';
import emptyOrPhoneFormat from '@/rules/phone';
import requiredField from '@/rules/required';
import noReccPrefix from '@/rules/recc-info';
import slugFormat from '@/rules/slug';


export const USERNAME_RULES = [
    requiredField,
    atLeast4Char,
];

export const GROUP_SLUG_RULES = [
    requiredField,
    slugFormat,
];

export const PASSWORD_RULES = [
    requiredField,
    atLeast4Char,
];

export const EMAIL_RULES = [
    emptyOrEmailFormat,
];

export const PHONE_RULES = [
    emptyOrPhoneFormat,
];

export const INFO_RULES = [
    requiredField,
    noReccPrefix,
];

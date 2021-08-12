import atLeast4Char from '@/rules/at-least';
import emptyOrEmailFormat from '@/rules/email';
import emptyOrPhoneFormat from '@/rules/phone';
import requiredField from '@/rules/required';


export const USERNAME_RULES = [
    requiredField,
    atLeast4Char,
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

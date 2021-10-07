import moment from 'moment';

export function splitDateAndTime(text: string) {
    return text.split('T');
}

export function iso8601ToLocal(text: string) {
    if (text) {
        return moment(text).format('LLLL');
    } else {
        return '';
    }
}

export function iso8601ToLocalDate(text?: string) {
    if (text) {
        return moment(text).format('YYYY-MM-DD');
    } else {
        return '';
    }
}

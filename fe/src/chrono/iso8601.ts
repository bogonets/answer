import moment from 'moment-timezone';

export function splitDateAndTime(text: string) {
    return text.split('T');
}

export function iso8601ToLocal(text?: string) {
    if (text) {
        return moment(text).tz(moment.tz.guess()).format('LLLL');
    } else {
        return '';
    }
}

export function iso8601ToLocalDate(text?: string) {
    if (text) {
        return moment(text).tz(moment.tz.guess()).format('YYYY-MM-DD');
    } else {
        return '';
    }
}

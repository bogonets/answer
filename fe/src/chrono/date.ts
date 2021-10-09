import moment from 'moment-timezone';

export function createMoment(inp?: moment.MomentInput) {
    return moment(inp).tz(moment.tz.guess());
}

export function momentDurationSeconds(x: moment.Moment, y: moment.Moment) {
    return x.diff(y, 'seconds');
}

export function today() {
    return new Date(Date.now());
}

export function yesterday() {
  const date = today();
  const result = new Date();
  result.setDate(date.getDate() - 1);
  return result;
}

export function dateString(year: number, month: number, day: number) {
    const yearText = `${year}`.padStart(4, '0');
    const monthText = `${month}`.padStart(2, '0');
    const dayText = `${day}`.padStart(2, '0');

    return `${yearText}-${monthText}-${dayText}`;
}

export function dateToString(date: Date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    return dateString(year, month, day);
}

export function todayString() {
    return dateToString(today());
}

export function yesterdayString() {
    return dateToString(yesterday());
}

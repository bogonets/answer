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

export function iso8601ToLocalDateTime(text?: string) {
  if (text) {
    return moment(text).tz(moment.tz.guess()).format('YYYY-MM-DD hh:mm:ss');
  } else {
    return '';
  }
}

export function updatedOrCreated(updatedAt?: string, createdAt?: string) {
  if (updatedAt) {
    return iso8601ToLocalDate(updatedAt);
  }
  if (createdAt) {
    return iso8601ToLocalDate(createdAt);
  }
  return '';
}

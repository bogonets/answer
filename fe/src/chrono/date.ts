export function now() {
    return new Date(Date.now());
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

export function nowString() {
    return dateToString(now());
}

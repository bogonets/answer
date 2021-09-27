export function randomInteger(min: number, max: number) {
    const min0 = Math.ceil(min);
    const max0 = Math.floor(max);
    return Math.floor(Math.random() * (max0 - min0)) + min0;
}

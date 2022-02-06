export function valueToRatio(value: number, min: number, max: number) {
    console.assert(min <= value && value <= max);
    console.assert(min < max);

    const width = max - min;
    const x = value - min;

    return x / width;
}

export function ratioToValue(ratio: number, min: number, max: number) {
    console.assert(0 <= ratio && ratio <= 1);
    console.assert(min < max);

    const width = max - min;
    const pos = ratio * width;

    return min + pos;
}

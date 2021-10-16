const HEX_REF = '0123456789abcdef';

export function generateRandomSession(size = 64) {
    let result = '';
    for (let n = 0; n < size; n++) {
        result += HEX_REF[Math.floor(Math.random() * 16)];
    }
    return result;
}

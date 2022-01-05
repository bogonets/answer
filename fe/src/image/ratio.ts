import {TypeException} from "@/exceptions";

export interface Size {
    width?: number;
    height?: number;
}

export function aspectRatio(original: Size, destination: Size) {
    const ow = original.width;
    const oh = original.height;
    if (typeof ow !== 'number') {
        throw new TypeException('The `original.width` argument is not a numeric type.');
    }
    if (typeof oh !== 'number') {
        throw new TypeException('The `original.height` argument is not a numeric type.');
    }

    const dw = destination.width;
    const dh = destination.height;

    if (dw && dh) {
        return {width: dw, height: dh} as Size;
    } else if (!dw && dh) {
        return {width: ow * dh / oh, height: dh} as Size;
    } else if (dw && !dh) {
        return {width: dw, height: oh * dw / ow} as Size;
    } else {
        return {width: ow, height: oh} as Size;
    }
}

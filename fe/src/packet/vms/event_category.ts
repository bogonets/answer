export const ANY_DEVICE_UID = -1;

export const EVENT_CATEGORY_ID_COLOR = 1;
export const EVENT_CATEGORY_ID_DETECTION = 2;
export const EVENT_CATEGORY_ID_MATCHING = 3;
export const EVENT_CATEGORY_ID_OCR = 4;

export const EVENT_CATEGORY_NAME_COLOR = 'color';
export const EVENT_CATEGORY_NAME_DETECTION = 'detection';
export const EVENT_CATEGORY_NAME_MATCHING = 'matching';
export const EVENT_CATEGORY_NAME_OCR = 'ocr';

export const EVENT_CATEGORIES = [
    EVENT_CATEGORY_NAME_COLOR,
    EVENT_CATEGORY_NAME_DETECTION,
    EVENT_CATEGORY_NAME_MATCHING,
    EVENT_CATEGORY_NAME_OCR,
];

export enum EventCategory {
    Color = 1,
    Detection = 2,
    Matching = 3,
    Ocr = 4,
}

function create_event_category_to_icon() {
    const result = {};
    result[EventCategory.Color] = 'mdi-palette';
    result[EventCategory.Detection] = 'mdi-image-search';
    result[EventCategory.Matching] = 'mdi-compare';
    result[EventCategory.Ocr] = 'mdi-ocr';
    return result;
}

export const EVENT_CATEGORY_TO_ICON = create_event_category_to_icon();

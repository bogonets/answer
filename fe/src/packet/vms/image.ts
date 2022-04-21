export interface VmsImageA {
  content_type: string;
  encoding: string;
  content: string;
}

export interface VmsUploadImageQ {
  content: string;
  name?: string;
  encoding?: string;
  content_type?: string;
}

export interface VmsUploadImageA {
  name: string;
}

export function imageDataUrlToVmsImageA(image: string) {
  const prefix = 'data:';
  if (!image.startsWith(prefix)) {
    throw Error('Unsupported DataUrl');
  }

  const separatorIndex = image.indexOf(';');
  const typeStart = prefix.length;
  const typeLength = separatorIndex - prefix.length;
  const resultContentType = image.substr(typeStart, typeLength);

  const encodingStart = separatorIndex + 1;
  const commaIndex = image.indexOf(',', encodingStart);
  const encodingLength = commaIndex - encodingStart;
  const resultEncoding = image.substr(encodingStart, encodingLength);

  const contentBegin = commaIndex + 1;
  const resultContent = image.substr(contentBegin);

  return {
    content_type: resultContentType,
    encoding: resultEncoding,
    content: resultContent,
  } as VmsImageA;
}

export function imageDataUrlToVmsUploadImageQ(image: string, name?: string) {
  const vmsImageA = imageDataUrlToVmsImageA(image);
  return {
    content: vmsImageA.content,
    name: name,
    encoding: vmsImageA.encoding,
    content_type: vmsImageA.content_type,
  } as VmsUploadImageQ;
}

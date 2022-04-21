import downloadJs from 'downloadjs';

export function download(data, fileName, mime) {
  downloadJs(data, fileName, mime);
}

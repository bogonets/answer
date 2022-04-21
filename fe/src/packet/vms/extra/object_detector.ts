export interface VmsEventConfigDetectionQ {
  model: string;
  checkpoint: string;
  label: Array<string>;
  threshold: number;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

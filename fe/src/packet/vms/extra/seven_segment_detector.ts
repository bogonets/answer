export interface VmsEventConfigOcrFilterQ {
  logical: string;
  operator: string;
  value: number;
}

export interface VmsEventConfigOcrQ {
  model: string;
  checkpoint: string;
  threshold: number;
  filters: Array<VmsEventConfigOcrFilterQ>;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

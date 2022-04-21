import type {VmsImageA, VmsUploadImageQ, VmsUploadImageA} from '@/packet/vms/image';

export interface VmsEventConfigMatchingQ {
  train_image_uuid: string;
  train_x1: number;
  train_y1: number;
  train_x2: number;
  train_y2: number;
  distance: number;
  threshold: number;
  operator: string;
  emit_condition: boolean;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export type VmsEventConfigMatchingSnapshotA = VmsImageA;
export type VmsEventConfigMatchingSnapshotUploadQ = VmsUploadImageQ;
export type VmsEventConfigMatchingSnapshotUploadA = VmsUploadImageA;

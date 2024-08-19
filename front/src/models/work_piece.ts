export interface WorkPiece {
  id: number;
  name?: string;
  description?: string;
  start?: string;
  finish?: string;
  invoice_item?: number;
  client?: number;
  project?: number;
  worker?: number;
}
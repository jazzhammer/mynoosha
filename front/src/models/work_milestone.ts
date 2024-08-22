export interface WorkMilestone {
  id: number;
  name?: string;
  description?: string;
  start?: string;
  invoice_item?: number;
  client?: number;
  project?: number;
  worker?: number;
}
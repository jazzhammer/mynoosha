export interface InvoiceItem {
  id: number;
  amount_total?: number;
  detail?: string;
  invoice_id: number;
  work_type_id?: number;
}
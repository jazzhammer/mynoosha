export interface InvoiceItem {
  id: number;
  amount_total?: number;
  detail?: string;
  invoice_id: number;
  type_id?: number;
}
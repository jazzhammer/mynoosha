import {type InvoiceItem} from '../models/invoice_item';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

export interface InvoiceItemDto {
  invoice: number,
  work_interval: number,
  work_type: number,
}

const InvoiceItemService = {
  create: (toCreate: InvoiceItemDto): Promise<InvoiceItem> => {
    return axios.post(`${apiBaseUrl}invoice_items/`, toCreate);
  },
  find: (search: Partial<InvoiceItem>): Promise<InvoiceItem[]> => {
    const params = search
    return axios.get(`${apiBaseUrl}invoice_items/`, {params});
  },
  update: (toUpdate: Partial<InvoiceItem>): Promise<InvoiceItem> => {
    return axios.put(`${apiBaseUrl}invoice_items/`, toUpdate);
  },
  delete: (toDelete: Partial<InvoiceItem>): Promise<InvoiceItem> => {
    return axios.delete(`${apiBaseUrl}invoice_item/`, {data: {
      id: toDelete.id
      }});
  },
};
export default InvoiceItemService;

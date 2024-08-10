import {type Invoice} from '../models/invoice';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const InvoiceService = {

  create: (toCreate: Partial<Invoice>): Promise<Invoice> => {
    return axios.post(`${apiBaseUrl}invoices/`, toCreate);
  },
  update: (toUpdate: Partial<Invoice>): Promise<Invoice> => {
    return axios.put(`${apiBaseUrl}invoices/`, toUpdate);
  },
  find: (search: any): Promise<Invoice[]> => {
    return axios.get(`${apiBaseUrl}invoices/`, {params: search});
  }
};
export default InvoiceService;

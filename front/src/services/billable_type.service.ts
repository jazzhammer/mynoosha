import {type BillableType} from '../models/billable_type';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const BillableTypeService = {
  create: (toCreate: Partial<BillableType>): Promise<BillableType> => {
    return axios.post(`${apiBaseUrl}billable_types/`, toCreate);
  },
  update: (toUpdate: Partial<BillableType>): Promise<BillableType> => {
    return axios.put(`${apiBaseUrl}billable_types/`, toUpdate);
  },
  find: (search: string | null): Promise<BillableType[]> => {
    const params = {search}
    return axios.get(`${apiBaseUrl}billable_types/`, {params});
  }
};
export default BillableTypeService;

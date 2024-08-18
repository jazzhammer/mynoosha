import {type Agreement} from '../models/agreement';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

export interface AgreementDto {
  client?: number;
  name?: string;
}

export interface SearchAgreementDto {
  search?: string;
  client?: number;
  worker?: number;
  name?: string;
  created_from?: string;
  created_through?: string;
}
const AgreementService = {
  create: (toCreate: AgreementDto): Promise<Agreement> => {
    return axios.post(`${apiBaseUrl}agreements/`, {...toCreate});
  },
  update: (toUpdate: Partial<Agreement>): Promise<Agreement> => {
    return axios.put(`${apiBaseUrl}agreements/`, toUpdate);
  },
  find: (search: SearchAgreementDto): Promise<Agreement[]> => {
    const params = {...search}
    return axios.get(`${apiBaseUrl}agreements/`, {params});
  },
  count: (search: SearchAgreementDto): Promise<number> => {
    const params = {...search}
    return axios.get(`${apiBaseUrl}agreements/count`, {params});
  }
};
export default AgreementService;

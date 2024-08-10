import {type Agreement} from '../models/agreement';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const AgreementService = {
  create: (toCreate: Partial<Agreement>): Promise<Agreement> => {
    return axios.post(`${apiBaseUrl}agreements/`, toCreate);
  },
  update: (toUpdate: Partial<Agreement>): Promise<Agreement> => {
    return axios.put(`${apiBaseUrl}agreements/`, toUpdate);
  },
  find: (search: string | null): Promise<Agreement[]> => {
    const params = {search}
    return axios.get(`${apiBaseUrl}agreements/`, {params});
  }
};
export default AgreementService;
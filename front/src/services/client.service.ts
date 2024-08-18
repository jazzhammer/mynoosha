import {type Client} from '../models/client';
import axios from "axios";
import type {SearchAgreementDto} from "./agreement.service";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

export interface ClientSearchDto {
  id?: number;
  name?: string;
}

const ClientService = {
  create: (toCreate: Partial<Client>): Promise<Client> => {
    return axios.post(`${apiBaseUrl}clients/`, toCreate);
  },
  update: (toUpdate: Partial<Client>): Promise<Client> => {
    return axios.put(`${apiBaseUrl}clients/`, toUpdate);
  },
  find: (search: ClientSearchDto): Promise<Client[]> => {
    const params = {...search}
    return axios.get(`${apiBaseUrl}clients/`, {params});
  },
  count: (search: ClientSearchDto): Promise<number> => {
    const params = {...search}
    return axios.get(`${apiBaseUrl}clients/count`, {params});
  }

};
export default ClientService;

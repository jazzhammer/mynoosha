import {type Client} from '../models/client';
import axios from "axios";
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
  }
};
export default ClientService;

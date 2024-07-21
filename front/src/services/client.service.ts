import {type Client} from '../models/client';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const ClientService = {
  createClient: (toCreate: Client): Promise<Client> => {
    return axios.post(`${apiBaseUrl}clients/`, toCreate);
  },
  find: (search: string | null): Promise<Client[]> => {
    const params = {search}
    return axios.get(`${apiBaseUrl}clients/`, {params});
  }
};
export default ClientService;

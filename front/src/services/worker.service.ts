import {type Worker} from '../models/worker';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const WorkerService = {
  create: (toCreate: Partial<Worker>): Promise<Worker> => {
    return axios.post(`${apiBaseUrl}workers/`, toCreate);
  },
  update: (toUpdate: Partial<Worker>): Promise<Worker> => {
    return axios.put(`${apiBaseUrl}workers/`, toUpdate);
  },
  find: (search: string | null): Promise<Worker[]> => {
    const params = {search}
    return axios.get(`${apiBaseUrl}workers/`, {params});
  }
};
export default WorkerService;

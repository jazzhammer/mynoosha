import {type Worker} from '../models/worker';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
export interface WorkerDto {
  last_name?: string;
  first_name?: string;
  ymd_birth?: string;
}
const WorkerService = {
  create: (toCreate: WorkerDto): Promise<any> => {
    return axios.post(`${apiBaseUrl}workers/`, toCreate).catch((error)=>{
      return new Promise((resolve, reject) => {
        resolve(null);
      });
    });
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

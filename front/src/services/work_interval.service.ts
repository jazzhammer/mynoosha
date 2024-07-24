import {type WorkInterval} from '../models/work_interval';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const WorkIntervalService = {
  create: (toCreate: WorkInterval): Promise<WorkInterval> => {
    return axios.post(`${apiBaseUrl}work_intervals/`, toCreate);
  },
  find: (search: {}): Promise<WorkInterval[]> => {
    const params = search
    return axios.get(`${apiBaseUrl}work_intervals/`, {params});
  },
  update: (toUpdate: Partial<WorkInterval>): Promise<WorkInterval> => {
    return axios.put(`${apiBaseUrl}work_intervals/`, toUpdate);
  },
  delete: (toDelete: Partial<WorkInterval>): Promise<WorkInterval> => {
    return axios.delete(`${apiBaseUrl}work_interval/`, {data: {
      id: toDelete.id
      }});
  },
};
export default WorkIntervalService;

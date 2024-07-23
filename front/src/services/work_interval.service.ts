import {type WorkInterval} from '../models/work_interval';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const WorkIntervalService = {
  create: (toCreate: WorkInterval): Promise<WorkInterval> => {
    return axios.post(`${apiBaseUrl}work_intervals/`, toCreate);
  },
  update: (toUpdate: Partial<WorkInterval>): Promise<WorkInterval> => {
    return axios.put(`${apiBaseUrl}work_intervals/`, toUpdate);
  },
  find: (search: {}): Promise<WorkInterval[]> => {
    const params = search
    return axios.get(`${apiBaseUrl}work_intervals/`, {params});
  }
};
export default WorkIntervalService;

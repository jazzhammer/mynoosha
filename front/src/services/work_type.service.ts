import {type WorkType} from '../models/work_type';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
export interface WorkTypeDto {
  name?: string;
  search?: string;
}
const WorkTypeService = {
  create: (toCreate: Partial<WorkType>): Promise<WorkType> => {
    return axios.post(`${apiBaseUrl}work_types/`, toCreate);
  },
  update: (toUpdate: Partial<WorkType>): Promise<WorkType> => {
    return axios.put(`${apiBaseUrl}work_types/`, toUpdate);
  },
  find: (search: WorkTypeDto): Promise<WorkType[]> => {
    const params = {search}
    return axios.get(`${apiBaseUrl}work_types/`, {params});
  }
};
export default WorkTypeService;

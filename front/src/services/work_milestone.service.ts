import {type WorkMilestone} from '../models/work_milestone';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

export interface WorkMilestoneDto {
  name?: string;
  description?: string;
  start?: string;
  invoice_item?: number;
  client?: number;
  project?: number;
  worker?: number;
}

const WorkMilestoneService = {
  create: (toCreate: WorkMilestoneDto): Promise<WorkMilestone> => {
    return axios.post(`${apiBaseUrl}work_milestones/`, toCreate);
  },
  find: (search: {}): Promise<WorkMilestone[]> => {
    const params = search
    return axios.get(`${apiBaseUrl}work_milestones/`, {params});
  },
  update: (toUpdate: Partial<WorkMilestone>): Promise<WorkMilestone> => {
    return axios.put(`${apiBaseUrl}work_milestones/`, toUpdate);
  },
  delete: (toDelete: Partial<WorkMilestone>): Promise<WorkMilestone> => {
    return axios.delete(`${apiBaseUrl}work_milestone/`, {data: {
      id: toDelete.id
      }});
  },
};
export default WorkMilestoneService;

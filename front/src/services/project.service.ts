import {type Project} from '../models/project';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
export interface ProjectDto {
  name?: string;
  description?: string;
  search?: string;
  created_from?: string;
  created_through?: string;
  client?: number;
  client_name?: string;
  agreement?: number;
  workInterval?: number;
}
const ProjectService = {
  create: (toCreate: ProjectDto): Promise<Project> => {
    return axios.post(`${apiBaseUrl}projects/`, {...toCreate});
  },
  update: (toUpdate: Partial<Project>): Promise<Project> => {
    return axios.put(`${apiBaseUrl}projects/`, toUpdate);
  },
  find: (search: ProjectDto): Promise<Project[]> => {
    const params = {...search}
    return axios.get(`${apiBaseUrl}projects/`, {params});
  }
};
export default ProjectService;

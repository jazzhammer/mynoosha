import {type Project} from '../models/project';
import axios from "axios";
import type {ClientSearchDto} from "./client.service";
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
export interface ProjectSearchDto {
  name?: string;
  description?: string;
  search?: string;
  pre_created_from?: string;
  post_created_from?: string;
  pre_created_through?: string;
  post_created_through?: string;
  client?: number;
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
  },
  count: (search: ProjectSearchDto): Promise<number> => {
    const params = {...search}
    return axios.get(`${apiBaseUrl}projects/count`, {params});
  }
};
export default ProjectService;

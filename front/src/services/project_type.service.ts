import {type ProjectType} from '../models/project_type';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
export interface ProjectTypeDto {
  name?: string;
  search?: string;
}
const ProjectTypeService = {
  create: (toCreate: Partial<ProjectType>): Promise<ProjectType> => {
    return axios.post(`${apiBaseUrl}project_types/`, toCreate);
  },
  update: (toUpdate: Partial<ProjectType>): Promise<ProjectType> => {
    return axios.put(`${apiBaseUrl}project_types/`, toUpdate);
  },
  find: (search: ProjectTypeDto): Promise<ProjectType[]> => {
    const params = {search}
    return axios.get(`${apiBaseUrl}project_types/`, {params});
  }
};
export default ProjectTypeService;

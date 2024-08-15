import {type Medium} from '../models/medium';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
export interface MediumDto {
  name?: string;
  file: File;
}
const MediumService = {
  create: (toCreate: MediumDto): Promise<any> => {
    const formData = new FormData();
    formData.append('image_file', toCreate.file);
    return axios.post(`${apiBaseUrl}mediums/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  update: (toUpdate: Partial<Medium>): Promise<Medium> => {
    return axios.put(`${apiBaseUrl}workers/`, toUpdate);
  },
  find: (search: string | null): Promise<Medium[]> => {
    const params = {search}
    return axios.get(`${apiBaseUrl}workers/`, {params});
  }
};
export default MediumService;

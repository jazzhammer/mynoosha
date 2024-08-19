import {type WorkPiece} from '../models/work_piece';
import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

export interface WorkPieceDto {
  id: number;
  name?: string;
  description?: string;
  start?: string;
  finish?: string;
  invoice_item?: number;
  client?: number;
  project?: number;
  worker?: number;
}

const WorkPieceService = {
  create: (toCreate: WorkPieceDto): Promise<WorkPiece> => {
    return axios.post(`${apiBaseUrl}work_pieces/`, toCreate);
  },
  find: (search: {}): Promise<WorkPiece[]> => {
    const params = search
    return axios.get(`${apiBaseUrl}work_pieces/`, {params});
  },
  update: (toUpdate: Partial<WorkPiece>): Promise<WorkPiece> => {
    return axios.put(`${apiBaseUrl}work_pieces/`, toUpdate);
  },
  delete: (toDelete: Partial<WorkPiece>): Promise<WorkPiece> => {
    return axios.delete(`${apiBaseUrl}work_piece/`, {data: {
      id: toDelete.id
      }});
  },
};
export default WorkPieceService;

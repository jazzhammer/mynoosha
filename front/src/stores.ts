import {writable} from "svelte/store";
import type {Client} from "./models/client";
import type {WorkInterval} from "./models/work_interval";

export enum crud {
  CREATE,
  READ,
  UPDATE,
  DELETE,
}

export interface NavEvent {
  type: string;
  value: string;
}
export const NavStore = writable<NavEvent>();


export interface ClientCrud {
  type: crud;
  payload: Client | Client[];
}
export const ClientStore = writable<ClientCrud>();

export const RecordableClientsStore = writable<Client[]>();

export const WorkIntervalListsByClient = writable<{[key: number]: WorkInterval[]}>({});


export interface WorkIntervalCrud {
  type: crud;
  payload: WorkInterval | WorkInterval[];
}
export const WorkIntervalStore = writable<WorkIntervalCrud>();


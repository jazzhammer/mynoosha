import {writable} from "svelte/store";
import type {Client} from "./models/client";

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

// const initialClientCrud: ClientCrud = {
//   type: crud.NOOP,
//   payload: null
// };
export const ClientStore = writable<ClientCrud>();
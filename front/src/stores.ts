import {writable} from "svelte/store";
import type {Client} from "./models/client";
import type {WorkInterval} from "./models/work_interval";
import type {BillableType} from "./models/billable_type";
import type {Agreement} from "./models/agreement";
import type {Invoice} from "./models/invoice";


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

export interface AgreementCrud {
  type: crud;
  payload: Agreement | Agreement[];
}
export const AgreementStore = writable<AgreementCrud>();

export interface ClientCrud {
  type: crud;
  payload: Client | Client[];
}
export const ClientStore = writable<ClientCrud>();

export interface InvoiceCrud {
  type: crud;
  payload: Invoice | Invoice[];
}
export const InvoiceStore = writable<InvoiceCrud>();

export interface WorkerCrud {
  type: crud;
  payload: Worker | Worker[];
}
export const WorkerStore = writable<WorkerCrud>();

export interface BillableTypeCrud {
  type: crud;
  payload: BillableType | BillableType[];
}
export const BillableTypeStore = writable<BillableTypeCrud>();


export const RecordableClientsStore = writable<Client[]>();

export const WorkIntervalListsByClient = writable<{[key: number]: WorkInterval[]}>({});


export interface WorkIntervalCrud {
  type: crud;
  payload: WorkInterval | WorkInterval[];
}
export const WorkIntervalStore = writable<WorkIntervalCrud>();


export interface MynooshaEvent {
  type: string;
  message: string;
}

export const MessageStore = writable<MynooshaEvent>();

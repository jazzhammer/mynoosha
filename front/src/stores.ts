import {writable} from "svelte/store";
import type {Client} from "./models/client";
import type {WorkInterval} from "./models/work_interval";
import type {BillableType} from "./models/billable_type";
import type {Agreement} from "./models/agreement";
import type {Invoice} from "./models/invoice";
import type {InvoiceItem} from "./models/invoice_item";
import type {WorkType} from "./models/work_type";
import type {Project} from "./models/project";
import type {Medium} from "./models/medium";
import type {ProjectType} from "./models/project_type";
import type {WorkPiece} from "./models/work_piece";
import type {WorkMilestone} from "./models/work_milestone";


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


export interface WorkMilestoneCrud {
  type: crud;
  payload: WorkMilestone | WorkMilestone[];
}
export const WorkMilestoneStore = writable<WorkMilestoneCrud>();

export interface WorkPieceCrud {
  type: crud;
  payload: WorkPiece | WorkPiece[];
}
export const WorkPieceStore = writable<WorkPieceCrud>();

export interface WorkIntervalCrud {
  type: crud;
  payload: WorkInterval | WorkInterval[];
}
export const WorkIntervalStore = writable<WorkIntervalCrud>();

export interface WorkTypeCrud {
  type: crud;
  payload: WorkType | WorkType[];
}
export const WorkTypeStore = writable<WorkTypeCrud>();

export interface ProjectCrud {
  type: crud;
  payload: Project | Project[];
}
export const ProjectStore = writable<ProjectCrud>();

export interface ProjectTypeCrud {
  type: crud;
  payload: ProjectType | ProjectType[];
}
export const ProjectTypeStore = writable<ProjectTypeCrud>();

export interface InvoiceItemCrud {
  type: crud;
  payload: InvoiceItem | InvoiceItem[];
}
export const InvoiceItemStore = writable<InvoiceItemCrud>();

export interface MediumCrud {
  type: crud;
  payload: Medium | Medium[];
}
export const MediumStore = writable<MediumCrud>();


export interface MynooshaEvent {
  type: string;
  message: string;
}

export const MessageStore = writable<MynooshaEvent>();

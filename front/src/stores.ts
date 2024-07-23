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
// let workIntervalListsByClient = {};
// const unsubscribeWorkIntervalListsByClient = WorkIntervalListsByClient.subscribe((wilbc) => {
//   workIntervalListsByClient = wilbc;
//   console.log('!next workIntervalListsByClient');
// });
// // onDestroy(unsubscribeWorkIntervalListsByClient);

export interface WorkIntervalCrud {
  type: crud;
  payload: WorkInterval | WorkInterval[];
}
export const WorkIntervalStore = writable<WorkIntervalCrud>();

//
// const unsubscribeWorkInterval = WorkIntervalStore.subscribe((wic: WorkIntervalCrud) => {
//   console.log(`!WorkIntervalCrud`);
//   if (!workIntervalListsByClient) {
//     workIntervalListsByClient = {};
//   }
//   const nextWorkIntervalListsByClient: {[key: number]: WorkInterval[]} = structuredClone(workIntervalListsByClient);
//   debugger;
//   if (wic && wic.payload.constructor !== Array) {
//     console.log(`!next WprkInterval`)
//     const updated: WorkInterval = wic.payload as unknown as WorkInterval;
//     let wil: WorkInterval[] = nextWorkIntervalListsByClient[updated.id as number]
//     if (!wil) {
//       wil = [];
//       nextWorkIntervalListsByClient[updated.id as number] = wil;
//     }
//     wil.push(updated);
//     WorkIntervalListsByClient.set(nextWorkIntervalListsByClient);
//   } else {
//     console.log(`!WorkIntervalStore(wic=${JSON.stringify(wic)})`);
//   }
// });
// // onDestroy(unsubscribeWorkInterval);

<script lang="ts">
  import {DateTime} from "luxon";

  import {
    type ClientCrud,
    ClientStore,
    crud,
    NavStore,
    RecordableClientsStore,
    type WorkIntervalCrud,
    WorkIntervalListsByClient,
    WorkIntervalStore
  } from "../stores";
  import type {Client} from "../models/client";
  import ClientService from "../services/client.service";
  import {onDestroy} from "svelte";
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkInterval} from "../models/work_interval";
  import {padLeft} from "../utils/numbers";


  let recordableClients: Client[] = [];
  let workIntervalListsByClient: {[key: number]: WorkInterval[]};
  $: workIntervalListsByClient
  $: recordableClients

  /**
                 ,d
   ,adPPYba,  MM88MMM  ,adPPYba,   8b,dPPYba,   ,adPPYba,
    `"Y8ba,     88    8b       d8  88          8PP"""""""
   `"YbbdP"'    "Y888  `"YbbdP"'   88           `"Ybbd8"'
   */
  let clients: Client[] = [];
  $: clients
  const unsubscribeClients = ClientStore.subscribe((event: ClientCrud) => {
    if (event && (event.type === crud.CREATE)) {
      clients = [...clients, event.payload as Client];
    }
  })
  onDestroy(unsubscribeClients);
//---------------------------------------------------------------
  const unsubscribe = RecordableClientsStore.subscribe((founds: Client[]) => {
    recordableClients = founds;
  })
  onDestroy(unsubscribe);
  //---------------------------------------------------------------
  const unsubWorkIntervalListsByClient = WorkIntervalListsByClient.subscribe((next) => {
    workIntervalListsByClient = next;
  });
  onDestroy(unsubWorkIntervalListsByClient);
  //---------------------------------------------------------------
  const unsubscribeWorkInterval = WorkIntervalStore.subscribe((wic: WorkIntervalCrud) => {
    if (!workIntervalListsByClient) {
      workIntervalListsByClient = {};
    }
    const nextWorkIntervalListsByClient: {[key: number]: WorkInterval[]} = structuredClone(workIntervalListsByClient);
    if (wic && wic.payload.constructor !== Array) {
      if (wic.type === crud.UPDATE || wic.type === crud.CREATE) {
        const nextWI: WorkInterval = wic.payload as unknown as WorkInterval;
        let wil: WorkInterval[] = nextWorkIntervalListsByClient[nextWI.client as number]
        if (!wil) {
          wil = [];
          nextWorkIntervalListsByClient[nextWI.client as number] = wil;
        }
        if (wic.type === crud.UPDATE) {
          const index = wil.findIndex((one: WorkInterval) => {
            return one.id === nextWI.id;
          });
          // console.log(`!home nav WorkInterval index ${index}`)
          if (index >= 0) {
            wil[index] = nextWI;
          }
        } else {
          wil.push(nextWI);
        }
        WorkIntervalListsByClient.set(nextWorkIntervalListsByClient);
      } else
      if (wic.type === crud.DELETE) {
        const deletedWI: WorkInterval = wic.payload as unknown as WorkInterval;
        let wil: WorkInterval[] = nextWorkIntervalListsByClient[deletedWI.client as number]
        if (!wil) {
          wil = [];
        }
        const index = wil.findIndex((one: WorkInterval) => {
          return one.id === deletedWI.id;
        });
        if (index >= 0) {
          wil.splice(index, 1);
        }
        WorkIntervalListsByClient.set(nextWorkIntervalListsByClient);
      } else {
        console.log(`!WorkIntervalStore unhandled crud type: ${wic.type}:(wic=${JSON.stringify(wic)})`);
      }
    } else {
      console.log(`workIntervalListEvent !!!`);
    }
  });
  onDestroy(unsubscribeWorkInterval);
  //---------------------------------------------------------------
  const unsubscribeWorkIntervalListsByClient = WorkIntervalListsByClient.subscribe((wilbc) => {
    workIntervalListsByClient = wilbc;
    console.log('!next workIntervalListsByClient');
  });
  onDestroy(unsubscribeWorkIntervalListsByClient);
  //---------------------------------------------------------------
  let mode = 'clients';
  $: mode
  function go(next: string): void {
    mode = next;
    NavStore.set({type: 'home', value: mode});
  }

  function refreshClients(): void {
    ClientService.find(null).then((founds: any) => {
      clients = founds.data;
    })
  }
  refreshClients();


  function addTimeRecorderClient(client: Client): void {
    ClientStore.set({type: crud.READ, payload: client});
    NavStore.set({type: 'home', value: 'client'})
    NavStore.set({type: 'client', value: 'time'})
    if (!recordableClients) {
      recordableClients = [];
    }
    let nextRecordables = [...recordableClients];
    const indexAlready = nextRecordables.findIndex((one: Client) => {
      return one.id === client.id;
    });
    if (indexAlready < 0) {
      nextRecordables.push(client);
      WorkIntervalService.find({client: client.id}).then((response: any) => {
        const founds = response.data;
        workIntervalListsByClient = !workIntervalListsByClient ? {} : workIntervalListsByClient;
        const next = structuredClone(workIntervalListsByClient);
        founds.forEach((each: WorkInterval) => {
          const isoStart = DateTime.fromISO(each.start, {zone: 'utc'})
          const isoStartLocal = isoStart.toLocal();
          each.localHHMMStart = `${padLeft(isoStartLocal.hour, 2)}:${padLeft(isoStartLocal.minute, 2)}`;
          if (each.stop) {
            const isoStop = DateTime.fromISO(each.stop, {zone: 'utc'})
            const isoStopLocal = isoStop.toLocal();
            each.localHHMMStop = `${padLeft(isoStopLocal.hour, 2)}:${padLeft(isoStopLocal.minute, 2)}`;
          }
        });

        next[client.id as unknown as number] = founds;
        WorkIntervalListsByClient.set(next);
      });
    }
    RecordableClientsStore.set(nextRecordables);
  }


</script>
<div class="bg-mylow_white flex flex-col" style="min-width: 150px;">
  <img src="logo_mynoosha_nav.png" alt="nav logo">
  <div  on:click={() => {go('clients')}}
        on:keyup={() => {go('clients')}}
        role="button"
        tabindex="0"
        class="cursor-pointer hover:border hover:border-myroon-900 text-left ml-2 bg-myhigh_white pl-2 rounded w-11/12">
    clients({clients?.length})
  </div>
  <div class="flex flex-col text-left ml-4">
    <ul>
      {#each clients as client}
        <li class="cursor-pointer hover:border mr-3 pl-2 mt-2 rounded">
          <div on:click={() => addTimeRecorderClient(client)}
            on:keyup={() => addTimeRecorderClient(client)}
            tabindex="0"
            role="button"
            >
          {client.name}
        </div></li>
      {/each}
    </ul>
  </div>
  <div  on:click={() => {go('invoices')}}
        on:keyup={() => {go('invoices')}}
        role="button"
        tabindex="0"
        class="cursor-pointer hover:border hover:border-myroon-900 text-left ml-2 mt-2 bg-myhigh_white pl-2 rounded w-11/12">
    invoices
  </div>

  <div  on:click={() => {go('workers')}}
        on:keyup={() => {go('workers')}}
        role="button"
        tabindex="0"
        class="cursor-pointer hover:border hover:border-myroon-900 text-left ml-2 mt-2 bg-myhigh_white pl-2 rounded w-11/12">
    workers
  </div>

  <div  on:click={() => {go('billable types')}}
        on:keyup={() => {go('billable types')}}
        role="button"
        tabindex="0"
        class="cursor-pointer hover:border hover:border-myroon-900 text-left ml-2 mt-2 bg-myhigh_white pl-2 rounded w-11/12">
    billable types
  </div>

  <div  on:click={() => {go('media')}}
        on:keyup={() => {go('media')}}
        role="button"
        tabindex="0"
        class="cursor-pointer hover:border hover:border-myroon-900 text-left ml-2 mt-2 bg-myhigh_white pl-2 rounded w-11/12">
    media
  </div>

</div>

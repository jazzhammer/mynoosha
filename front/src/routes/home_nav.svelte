<script lang="ts">

  import {type ClientCrud, ClientStore, crud, NavStore, RecordableClientsStore} from "../stores";
  import type {Client} from "../models/client";
  import ClientService from "../services/client.service";
  import {onDestroy} from "svelte";

  let clients: Client[] = [];

  ClientStore.subscribe((event: ClientCrud) => {
    if (event && (event.type === crud.CREATE)) {
      clients = [...clients, event.payload as Client];
    }
  })

  let mode = 'clients';
  function go(next: string): void {
    mode = next;
    NavStore.set({type: 'home', value: mode});
  }

  function refreshClients(): void {
    ClientService.find(null).then((founds) => {
      clients = JSON.parse(founds.data);
    })
  }

  refreshClients();

  let recordableClients: Client[] = [];

  const unsubscribe = RecordableClientsStore.subscribe((founds: Client[]) => {
    recordableClients = founds;
  })
  onDestroy(unsubscribe);

  function addTimeRecorderClient(client: Client): void {
    NavStore.set({type: 'home', value: 'time-recorders'})
    if (!recordableClients) {
      recordableClients = [];
    }
    let nextRecordables = [...recordableClients];
    const indexAlready = nextRecordables.findIndex((one: Client) => {
      return one.id === client.id;
    });
    if (indexAlready < 0) {
      nextRecordables.push(client);
      // get this client's workIntervals for .... today

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
</div>

<script lang="ts">

  import {type ClientCrud, ClientStore, crud, NavStore} from "../stores";
  import type {Client} from "../models/client";
  import ClientService from "../services/client.service";

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
        <li>{client.name}</li>
      {/each}
    </ul>
  </div>
</div>

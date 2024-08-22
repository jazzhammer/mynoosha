<style>
  .browse-clients {
    width: 100%;
    text-align: left;
  }
</style>
<script lang="ts">
  import {type ClientCrud, ClientStore, crud, MessageStore, type MynooshaEvent} from "../stores";
  import type {Client} from "../models/client";
  import {onDestroy} from "svelte";
  import ClientService from "../services/client.service";
  import SearchClient from './search-client.svelte';
  import ClientList from './client_list.svelte';
  let client: Client;
  $: client
  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      client = ccrud.payload as Client
    }
  });
  onDestroy(unsubClient);

  let clients: Client[];
  $: clients

  function fetchClients(): void {
    ClientService.find({}).then((response) => {
      clients = response.data;
      MessageStore.set({
        type: 'clients',
        message: `found clients: ${clients && clients.length > 0 ? clients.length : 'none'}`
      });
    });
  }
  fetchClients()

  let message = '';
  $: message

  const unsubMessage = MessageStore.subscribe((mynooshaEvent: MynooshaEvent) => {
    if (mynooshaEvent && mynooshaEvent.type === 'clients') {
      message = mynooshaEvent.message;
      setTimeout(() => {
        message = '';
      }, 3000)
    }
  });

  onDestroy(unsubMessage);
  const foundClients = (next: Client[]): void => {
    clients = next;
  }
</script>
<div class="flex flex-col p-3 ml-3 rounded w-4/12 text-myhigh_white text-mywood-900 browse-clients "
     style="min-width: 226px;
     max-width: 700px;
     font-size: 10pt;"
     data-testid="browse_clients"
>
  <div>
    <SearchClient foundClients={foundClients}></SearchClient>
    <ClientList clients={clients}></ClientList>
  </div>
</div>

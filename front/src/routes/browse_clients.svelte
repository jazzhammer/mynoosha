<style>
</style>
<script lang="ts">
  import ClientService from '../services/client.service';
  import {type ClientCrud, ClientStore, crud} from "../stores";
  import type {Client} from "../models/client";
  import {onDestroy} from "svelte";

  let client: Client;
  $: client

  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      client = ccrud.payload as Client
    }
  });
  onDestroy(unsubClient);

</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="browse_clients">
  browse
</div>

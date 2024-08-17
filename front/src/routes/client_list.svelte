<style>
  .client-list {
  }
  .client-list-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
  }
  .client-headers {

  }
  .client-headers > * {
    text-align: center;
  }

</style>
<script lang="ts">

  import type {Client} from "../models/client";

  export let clients: Client[] = [];
  $: clients;

  export let selectClient = (client: Client) => {
    console.log(`selectClient:${JSON.stringify(client)}`);
  };

</script>
<div class="client-list">
  <div class="client-list-row client-headers">
    <div class="bg-mymid_white">id</div>
    <div class="bg-mymid_white">name</div>
    <div class="bg-mymid_white">street</div>
    <div class="bg-mymid_white">city</div>
    <div class="bg-mymid_white">province</div>
    <div class="bg-mymid_white">postal</div>
  </div>
  {#each clients as client}
    <div class="client-list-row">
      <div on:click={() => selectClient(client)} class="cursor-pointer hover:bg-myblue-100 text-mywood-900 hover:text-mywood-500 hover:text-myhigh_white">{client.id}</div>
      <div>{client.name}</div>
      <div>{client.address_street}</div>
      <div>{client.address_city}</div>
      <div>{client.address_province_state}</div>
      <div>{client.address_postal_zip_code}</div>
    </div>
  {/each}
</div>
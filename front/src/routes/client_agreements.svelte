<style>
  .client-agreements {

  }
  .menu-item {

  }

  .menu-item:hover {
    font-weight: bold;
    box-shadow: #0d1117;
  }
</style>
<script lang="ts">
  import {type Client} from '../models/client';
  import {type ClientCrud, ClientStore, type AgreementCrud, AgreementStore} from "../stores";
  import NewClientAgreement from './new_client_agreement.svelte';
  import EditClientAgreement from './edit_client_agreement.svelte';
  import BrowseClientAgreement from './browse_client_agreement.svelte';
  import {onDestroy} from "svelte";
  import type {Agreement} from "../models/agreement";


  let mode = 'agreements';
  $: mode

  const setMode = (next: string) => {
    mode = next;
  }

  let agreement: Agreement;
  $: agreement
  const unsubAgreement = AgreementStore.subscribe((icrud: AgreementCrud) => {
    if (icrud) {
      if (!Array.isArray(icrud.payload)) {
        agreement = icrud.payload as Agreement;
        mode = 'edit';
      }
    }
  });

  onDestroy(unsubAgreement)
  let client: Client;
  $: client
  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if(ccrud){
      if (!Array.isArray(ccrud.payload)) {
        client = ccrud.payload as Client
      }
    }

  });
  onDestroy(unsubClient)

</script>
<div class="client-manager border-2 border-myroon-100 rounded text-mywood-900 m-2 time-recorder pb-4"
     style="min-width: 400px; min-height: 200px; max-width: 450px;">
  <div class="bg-myroon-100 text-myhigh_white">agreements</div>
  <div class="flex flex-row ml-3 mb-3 w-2/12 mt-4">
    {#if mode!=='browse'}
      <div on:click={() => {setMode('browse')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        browse
      </div>
    {/if}
    {#if mode!=='new'}
      <div on:click={() => {setMode('new')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        new
      </div>
    {/if}
  </div>
  {#if mode==='new'}
    <NewClientAgreement></NewClientAgreement>
  {/if}
  {#if mode==='edit'}
    <EditClientAgreement></EditClientAgreement>
  {/if}
  {#if mode==='browse'}
    <BrowseClientAgreement></BrowseClientAgreement>
  {/if}
</div>
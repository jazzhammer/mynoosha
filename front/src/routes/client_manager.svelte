<style>
  .client-manager {

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
  import {type ClientCrud, ClientStore, crud, type InvoiceCrud, InvoiceStore} from "../stores";
  import ClientInvoices from './client_invoices.svelte';
  import {onDestroy} from "svelte";
  import {type Invoice} from "../models/invoice";
  let client: Client;
  $: client

  let mode = 'invoices';
  $: mode

  const setMode = (next: string) => {
    mode = next;
  }

  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (!Array.isArray(ccrud.payload)) {
      client = ccrud.payload as Client
    }
  });
  onDestroy(unsubClient)

  let invoice: Invoice;
  $: invoice
  const unsubInvoice = InvoiceStore.subscribe((ccrud: InvoiceCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      invoice = ccrud.payload as Invoice
    }
  });
  onDestroy(unsubInvoice);

</script>
<div class="client-manager border-2 border-myroon-100 rounded text-mywood-900 m-2 time-recorder"
     style="min-width: 400px; min-height: 200px; max-width: 450px;">
  <div class="bg-myroon-100 text-myhigh_white">{client?.name} details</div>
  <div class="flex flex-row ml-3 mb-3 w-2/12 mt-4">
    {#if mode!=='invoices'}
      <div on:click={() => {setMode('invoices')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        invoices
      </div>
    {/if}
    {#if mode!=='invoicables'}
      <div on:click={() => {setMode('invoicables')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        invoicables
      </div>
    {/if}
  </div>
  {#if mode==='invoices'}
    <ClientInvoices></ClientInvoices>
  {/if}
</div>
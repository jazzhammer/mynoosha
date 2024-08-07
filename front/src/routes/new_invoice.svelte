<style>
  .invoice-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 180px;
  }

  .invoice-form-fields > * {
    margin-bottom: 2px;
  }

  .field-label {
    text-align: left;
    width: 110px;
  }

  .invoice-form-header {
    width: 262px;
  }
</style>
<script lang="ts">
  import InvoiceService from '../services/invoice.service';
  import {InvoiceStore, crud} from "../stores";
  import type {Client} from "../models/client";
  import ClientService from "../services/client.service";



  let clients: Client[] = [];
  $: clients
  let client: Partial<Client>;

  ClientService.find({}).then((founds: Client[]) => {
    clients = founds.data;
  });

  function createInvoice(): void {
    InvoiceService.create({
      client: client.id
    }).then((response: any) => {
      const created = response.data;
      InvoiceStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }
  function keyupName(event: any) {
    if (event.key === 'Enter') {
      createInvoice();
    }
  }


</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="new_invoice"
>
  <div class="invoice-form-header bg-mywood-900 rounded mb-5" data-testid="new_invoice_header" id="new_invoice_header">new invoice</div>
  <div class="invoice-form-fields w-3/12 text-mywood-900" data-testid="new_invoice_form">
    <label class="field-label" data-testid="new_invoice_name">client
      <select
        bind:value={client}
        style="padding-top: 0; width: 260px; height: 28px; font-size: 10pt; color: black; background-color: white; vertical-align: top"
        id="new_invoice_client"
        name="new_invoice_client"
        data-testid="new_invoice_client_select"
      >
        <option>select client to invoice</option>
        {#each clients as client_option}
          <option value={client_option}>{client_option.name}</option>
        {/each}
      </select>
    </label>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow">
    <button on:click={createInvoice}
            type="button"
            value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
            style="margin: auto;"
            data-testid="create_invoice_button"
    >
      create
    </button>
  </div>
</div>

<style>
  .invoice-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 200px;
  }
  .invoice-form-fields > * {
    margin-bottom: 2px;
  }
  .invoice-form-header {
    width: 265px;
  }
  .field-label {
    text-align: left;
  }
  .field-input {
    text-align: left;
    width: 200px;
    margin-left: 3px;
  }
</style>
<script lang="ts">
  import InvoiceService from '../services/invoice.service';
  import {type InvoiceCrud, InvoiceStore, crud} from "../stores";
  import type {Invoice} from "../models/invoice";
  import {onDestroy} from "svelte";
  // ------------------------------------------------------------
  let created: any = null;
  $: created
  let issued = '';
  $: issued
  // ------------------------------------------------------------
  let invoice: Invoice;
  $: invoice
  const unsubInvoice = InvoiceStore.subscribe((ccrud: InvoiceCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      invoice = ccrud.payload as Invoice
      created = invoice.created as string;
      issued = invoice.issued as string;
    }
  });
  onDestroy(unsubInvoice);

  function updateInvoice(): void {
    InvoiceService.update({
      id: invoice.id,
      created,
      issued,
    }).then((response: any) => {
      const updated = response.data;
      invoice = updated;
      InvoiceStore.set({
        type: crud.UPDATE,
        payload: updated
      });
    })
  }

  function keyupName(event: any) {
    if (event.key === 'Enter') {
      updateInvoice();
    }
    console.log(name)
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="new_invoice">
  <div class="invoice-form-header bg-mywood-900 rounded mb-5" data-testid="new_invoice_header" id="new_invoice_header">edit invoice</div>
  <div class="invoice-form-fields w-3/12 text-mywood-900" data-testid="new_invoice_form">
    <label class="field-label" data-testid="new_invoice_name">issued
      <input type="text"
             bind:value={issued}
             on:keyup={() => {}}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             id="new_invoice_issued_input"
             data-testid="new_invoice_issued_input"
      />
    </label>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow">
    <button on:click={updateInvoice}
            type="button"
            value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
            style="margin: auto;"
            data-testid="edit_invoice_button"
    >
      update
    </button>
  </div>
</div>

<style>
</style>
<script lang="ts">
  import {type InvoiceCrud, InvoiceStore, crud} from "../stores";
  import type {Invoice} from "../models/invoice";
  import {onDestroy} from "svelte";

  let invoice: Invoice;
  $: invoice
  const unsubInvoice = InvoiceStore.subscribe((ccrud: InvoiceCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      invoice = ccrud.payload as Invoice
    }
  });
  onDestroy(unsubInvoice);

</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="browse_invoices">
  browse
</div>

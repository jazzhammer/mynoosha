<style>
  .invoice-list {
    display: grid;
    grid-template-columns: 1fr;
    font-size: 9pt;
  }
  .invoice-list-header {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 9pt;
  }
  .invoice-field {
    text-align: center;
  }
</style>

<script lang="ts">
  import {type Invoice} from '../models/invoice';
  export let invoices: Invoice[] = [];

  export let selectInvoice: (invoice: Invoice) => void;



</script>
<div class="invoice-list w-full border border-myblue-50">
  <div class="invoice-list-header bg-mylow_white">ymdIssue</div>
  {#each invoices as invoice}
    <div class="invoice-field text-black cursor-pointer hover:bg-myblue-100" on:click={() => {selectInvoice(invoice)}}>
      {invoice.issued.substring(0, invoice.issued.indexOf(' '))}
    </div>
  {/each}
</div>

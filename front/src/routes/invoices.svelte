<style>
  .menu-item {

  }
</style>
<script lang="ts">
  import NewInvoice from './new_invoice.svelte';
  import EditInvoice from './edit_invoice.svelte';
  import BrowseInvoices from './browse_invoices.svelte';
  // ------------------------------------------------------------
  let mode = 'new';
  $: mode
  function setMode(next: string): void {
    mode = next;
  }
</script>
<div class="">
  <div class="flex flex-row ml-3 mb-3 w-2/12">
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
    {#if mode!=='edit'}
      <div on:click={() => {setMode('edit')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        edit
      </div>
    {/if}
  </div>
  {#if mode === 'browse'}
    <BrowseInvoices></BrowseInvoices>
  {/if}
  {#if mode === 'new'}
    <NewInvoice></NewInvoice>
  {/if}
  {#if mode === 'edit'}
    <EditInvoice></EditInvoice>
  {/if}
</div>
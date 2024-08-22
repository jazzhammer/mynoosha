<style>
  .menu-item {

  }
  .clients {
    width: calc(100% - 15px);
  }
</style>
<script lang="ts">
  import NewClient from './new_client.svelte';
  import EditClient from './edit_client.svelte';
  import BrowseClients from './browse_clients.svelte';
  // ------------------------------------------------------------
  let mode = 'new';
  $: mode
  function setMode(next: string): void {
    mode = next;
  }
</script>
<div class="clients">
  <div class="projects-header bg-mywood-100 text-myhigh_white text-xl flex flex-row mb-3"
    style="height: 30px;"
  >
    <div style="margin-left: 10px;">clients</div>
    {#if mode!=='browse'}
      <div on:click={() => {setMode('browse')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           style="font-size: 11pt; margin-left: 4px; height: 26px; margin-top: 2px; padding-top: -1;"
           class="text-mywood-900 bg-mymid_white menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        browse
      </div>
    {/if}
    {#if mode!=='new'}
      <div on:click={() => {setMode('new')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           style="font-size: 11pt; margin-left: 4px; height: 26px; margin-top: 2px; padding-top: -1;"
           class="text-mywood-900 bg-mymid_white menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        new
      </div>
    {/if}
    {#if mode!=='edit'}
      <div on:click={() => {setMode('edit')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           style="font-size: 11pt; margin-left: 4px; height: 26px; margin-top: 2px; padding-top: -1;"
           class="text-mywood-900 bg-mymid_white menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        edit
      </div>
    {/if}
  </div>
  {#if mode === 'browse'}
    <BrowseClients></BrowseClients>
  {/if}
  {#if mode === 'new'}
    <NewClient></NewClient>
  {/if}
  {#if mode === 'edit'}
    <EditClient></EditClient>
  {/if}
</div>
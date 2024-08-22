<style>
  .menu-item {
    padding-left: 4px;
    padding-right: 4px;
    min-width: 80px;
    text-align: center;
    background-color: antiquewhite;
    cursor: pointer;
    border-radius: 2px;
    color: #3b1000;
    margin: 3px;
    font-size: 11pt;
  }
  .menu-item:hover {
    background-color: #2aabd2;
    color: #efefef;
  }

</style>
<script lang="ts">
  import type {Client} from "../models/client";
  import NewWorkMilestone from './new_work_milestone.svelte';
  let mode = '';
  $: mode

  let client: Client;
  $: client

  function setMode(next: string): void  {
    mode = next;
  }
</script>
<div class="work-milestones flex flex-col">
  <div class="work-milestones-header bg-mywood-100 text-myhigh_white text-xl flex flex-row">
    <div style="margin-left: 10px;">work-milestones {client ? `for client: ${client.name}` : ''}</div>
    {#if mode!=='new'}
      <div class="menu-item" on:click={() => setMode('new')}>new</div>
    {/if}
    {#if mode!=='browse'}
      <div class="menu-item" on:click={() => setMode('browse')}>browse</div>
    {/if}
  </div>
  {#if mode === 'new'}
    <NewWorkMilestone client={client}></NewWorkMilestone>
  {/if}
  {#if mode === 'search'}
  {/if}
</div>
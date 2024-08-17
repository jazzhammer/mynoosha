 <script lang="ts">
  import Client from './client.svelte';
  import Nav from './home_nav.svelte';
  import TimeRecorders from './time_recorders.svelte';
  import {NavStore} from "../stores";
  import {onDestroy} from "svelte";
  import Clients from './clients.svelte';
  import Invoices from './invoices.svelte';
  import BillableTypes from './billable_types.svelte';
  import MediaManager from './media_manager.svelte';
  import Workers from './workers.svelte';
  import Projects from './projects.svelte';
  import Message from './message.svelte';

  let mode: string | null = 'clients'
  $: mode

  const unsubscribe = NavStore.subscribe((next) => {
    if (next && next.type === 'home') {
      mode = next ? next.value : mode;
    }
  });
  onDestroy(unsubscribe);
</script>
<style>
  .home-layout {
    display: grid;
    grid-template-columns: 1fr 8fr;
  }
</style>
<div class="p-1 rounded w-full h-lvh flex flex-col text-center home-layout bg-mylow_white" data-testid="home">
  <Nav></Nav>
  <div class="h-lvh bg-myhigh_white rounded pt-2" style="width: 100%">
    <div style="height: 60px; width: 100%;">
      <Message></Message>
    </div>
    {#if mode === 'clients'}
      <div class="bg-myhigh_white rounded-lg">
        <Clients></Clients>
      </div>
    {/if}
    {#if mode === 'invoices'}
      <div class="bg-myhigh_white rounded-lg">
        <Invoices></Invoices>
      </div>
    {/if}
    {#if mode === 'workers'}
      <div class="bg-myhigh_white rounded-lg">
        <Workers></Workers>
      </div>
    {/if}
    {#if mode === 'billable types'}
      <div class="bg-myhigh_white rounded-lg">
        <BillableTypes></BillableTypes>
      </div>
    {/if}
    {#if mode === 'client'}
      <div class="bg-myhigh_white rounded-lg">
        <Client></Client>
      </div>
    {/if}
    {#if mode === 'time-recorders'}
      <div class="bg-myhigh_white rounded-lg">
        <TimeRecorders></TimeRecorders>
      </div>
    {/if}
    {#if mode === 'media'}
      <div class="bg-myhigh_white rounded-lg" style="width: 100%;">
        <MediaManager></MediaManager>
      </div>
    {/if}
    {#if mode === 'projects'}
      <div class="bg-myhigh_white rounded-lg" style="width: 100%;">
        <Projects></Projects>
      </div>
    {/if}
  </div>
</div>

 <script lang="ts">
  import Client from './client.svelte';
  import Nav from './home_nav.svelte';
  import TimeRecorders from './time_recorders.svelte';
  import {type NavEvent, NavStore} from "../stores";
  import {onDestroy} from "svelte";
  import Clients from './clients.svelte';

  let mode: string | null = 'clients'
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
  <div class="h-lvh bg-myhigh_white rounded pt-20">
    {#if mode === 'clients'}
      <div class="bg-myhigh_white rounded-lg">
        <Clients></Clients>
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
  </div>
</div>

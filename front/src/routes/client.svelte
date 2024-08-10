<style>
  .menu-item {

  }
</style>
<script lang="ts">
  import NewClient from './new_client.svelte';
  import TimeRecorder from './time_recorder.svelte';
  import ClientManager from './client_manager.svelte';
  import type {Client} from "../models/client";
  import {
    type ClientCrud,
    ClientStore,
    crud, type NavEvent,
    NavStore,
    WorkIntervalListsByClient
  } from "../stores";
  import {type WorkInterval} from "../models/work_interval";
  import {onDestroy} from "svelte";
  import EditClient from './edit_client.svelte';

  let workIntervalList: WorkInterval[];
  $: workIntervalList
  // MODE ------------------------------------------------------------
  let mode = 'time';
  $: mode
  const unsubNav = NavStore.subscribe((nav: NavEvent) => {
    if (nav && nav.type === 'client') {
      mode = nav.value;
    }
  });
  onDestroy(unsubNav)
  function setMode(next: string): void {
    mode = next;
  }
  // ------------------------------------------------------------
  let workIntervalListsByClient: {[key: number]: WorkInterval[]};
  $: workIntervalListsByClient
  const unsubWorkIntervalListByClients = WorkIntervalListsByClient.subscribe((lists: {[key: number]: WorkInterval[]}) => {
    workIntervalListsByClient = lists;
  });
  onDestroy(unsubWorkIntervalListByClients)
  // ------------------------------------------------------------
  let client: Client;
  $: client
  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      client = ccrud.payload as Client;
      workIntervalList = workIntervalListsByClient?.[client.id as unknown as number]
    }
  });
  onDestroy(unsubClient)

</script>
<div class="">
  <div class="flex flex-row ml-3 mb-3 w-2/12">
    {#if mode!=='time'}
      <div on:click={() => {setMode('time')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        time
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
    {#if mode!=='new'}
      <div on:click={() => {setMode('new')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        new
      </div>
    {/if}
  </div>
  {#if mode === 'new'}
    <NewClient></NewClient>
  {/if}
  {#if mode === 'edit'}
    <EditClient></EditClient>
  {/if}
  {#if mode === 'time'}
    <div class="flex flex-row">
      <TimeRecorder></TimeRecorder>
      <ClientManager></ClientManager>
    </div>
  {/if}
</div>
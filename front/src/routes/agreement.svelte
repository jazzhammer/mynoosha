<style>
  .menu-item {

  }
</style>
<script lang="ts">
  import NewAgreement from './new_agreement.svelte';
  import TimeRecorder from './time_recorder.svelte';
  import type {Agreement} from "../models/agreement";
  import {
    type AgreementCrud,
    AgreementStore,
    crud, type NavEvent,
    NavStore
  } from "../stores";
  import {type WorkInterval} from "../models/work_interval";
  import {onDestroy} from "svelte";
  import EditAgreement from './edit_agreement.svelte';

  let workIntervalList: WorkInterval[];
  $: workIntervalList
  // MODE ------------------------------------------------------------
  let mode = 'time';
  $: mode
  const unsubNav = NavStore.subscribe((nav: NavEvent) => {
    if (nav && nav.type === 'agreement') {
      mode = nav.value;
    }
  });
  onDestroy(unsubNav)
  function setMode(next: string): void {
    mode = next;
  }
  // ------------------------------------------------------------
  let workIntervalListsByAgreement: {[key: number]: WorkInterval[]};
  $: workIntervalListsByAgreement
  const unsubWorkIntervalListByAgreements = WorkIntervalListsByAgreement.subscribe((lists: {[key: number]: WorkInterval[]}) => {
    workIntervalListsByAgreement = lists;
  });
  onDestroy(unsubWorkIntervalListByAgreements)
  // ------------------------------------------------------------
  let agreement: Agreement;
  $: agreement
  const unsubAgreement = AgreementStore.subscribe((ccrud: AgreementCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      agreement = ccrud.payload as Agreement;
      workIntervalList = workIntervalListsByAgreement?.[agreement.id as unknown as number]
    }
  });
  onDestroy(unsubAgreement)

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
    <NewAgreement></NewAgreement>
  {/if}
  {#if mode === 'edit'}
    <EditAgreement></EditAgreement>
  {/if}
  {#if mode === 'time'}
    <TimeRecorder agreement={agreement} workIntervalList={workIntervalList}></TimeRecorder>
  {/if}
</div>
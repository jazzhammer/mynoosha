<style>
  .client-form-fields {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    width: 100%;
    margin-left: 3px;
  }

  .edit-agreement-menu {
    display: flex;
    flex-direction: row;
  }

  .client-form-fields > * {
    margin-bottom: 2px;
  }

  .new-agreement {
    font-size: 9pt;
  }

  .menu-item {
    color: black;
    margin-left: 2px;
    margi-right: 2px;
  }

  .agreementable-work-intervals {
    display: grid;
    grid-template-columns: 1fr 4fr 2fr 10fr;
    color: black;
    font-size: 9pt;
  }
</style>
<script lang="ts">

  import {
    type ClientCrud,
    ClientStore,
    crud,
    type AgreementCrud,
    AgreementStore, WorkTypeStore,
  } from "../stores";

  import { DatePicker } from "@svelte-plugins/datepicker";
  import { format } from 'date-fns';
  import {type Client} from "../models/client";
  import {onDestroy} from "svelte";
  import AgreementService from "../services/agreement.service";
  import {type Agreement} from "../models/agreement";
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkInterval} from "../models/work_interval";
  import WorkTypeService from "../services/work_type.service";
  import type {WorkType} from "../models/work_type";

  let startDate = new Date();
  $: startDate
  let dateFormat = 'yyyy-MM-dd';
  let isOpen = false;

  const toggleDatePicker = () => (isOpen = !isOpen);

  const formatDate = (dateString: Date) => {
    return dateString && format(new Date(dateString), dateFormat) || '';
  };

  let formattedYmdIssue = formatDate(startDate);

  let client: Client;
  $: client
  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (!Array.isArray(ccrud.payload)) {
      client = ccrud.payload as Client;
    }
  });
  onDestroy(unsubClient)
  let agreement: Agreement;
  $: agreement
  const unsubAgreement = AgreementStore.subscribe((icrud: AgreementCrud) => {
    if (icrud) {
      if (!Array.isArray(icrud.payload)) {
        agreement = icrud.payload as Agreement;

        startDate = new Date(agreement.created);
        formattedYmdIssue = formatDate(startDate);
      }
    }
  });
  onDestroy(unsubAgreement)
  $: formattedYmdIssue = formatDate(startDate);
  function updateAgreement(): void {
    agreement.created = (new Date(formattedYmdIssue)).toUTCString();
    AgreementService.update({

    }).then((response: any) => {
      const created = response.data;
      AgreementStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }

  let mode = 'agreementd-items';
  $: mode
  function setMode(next: string): void {
    mode = next;
  }

  let agreementableWorkIntervals: WorkInterval[];
  $: agreementableWorkIntervals
  let agreementableChecks: boolean[] = [];
  $: agreementableChecks

  let workTypes: WorkType[] = [];
  $: workTypes
  let workTypesByName: {[key: string]: WorkType} = {};
  $: workTypesByName


  let agreementablesToAdd = 0;
  $: agreementablesToAdd
  function countAgreementablesToAdd(next: WorkInterval): number {
    debugger;
    agreementableChecks[next.id] = !agreementableChecks[next.id];
    let trues = 0;
    agreementableChecks.forEach((checked: boolean) => {
      trues += checked ? 1 : 0;
    })
    agreementablesToAdd = trues;
    return trues;
  }


</script>
<div class="new-agreement flex flex-col border-myroon-100 border p-3 mr-6 ml-3 rounded w-full text-myhigh_white"
     style="min-width: 226px; max-width: 375px; font-size: 10pt;" data-testid="edit_agreement"
>
  <div class="bg-mywood-900 rounded mb-5 w-full" data-testid="edit_agreement_header" id="edit_agreement_header">edit agreement</div>
  <div class="client-form-fields text-mywood-900" data-testid="edit_agreement_form">
    <div><div class="" data-testid="edit_agreement_name">ymd issue:</div></div>
    <div>
      <DatePicker bind:isOpen bind:startDate enableFutureDates={true}>
        <input type="text"
               placeholder="Select ymd issue"
               bind:value={formattedYmdIssue}
               on:click={toggleDatePicker}
               style="width: 100px; font-size: 9pt; height: 18px; text-align: center;"
        />
      </DatePicker>
    </div>
    <div><div class="" data-testid="edit_agreement_name">ymd create:</div></div>
    <div>{agreement.created.substring(0, agreement.created.indexOf(' '))}</div>
  </div>
  <div class="edit-agreement-menu flex flex-row ml-3 mb-3 mt-4">
    {#if mode!=='agreementd-items'}
      <div on:click={() => {setMode('agreementd-items')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6"
           style="width:150px;"
      >
        agreementd-items
      </div>
    {/if}
    {#if mode!=='agreementables'}
      <div on:click={() => {setMode('agreementables')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        agreementables
      </div>
    {/if}
    {#if mode!=='payments'}
      <div on:click={() => {setMode('payments')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        payments
      </div>
    {/if}
  </div>
  {#if mode==='agreementables'}
    <div class="bg-mywood-100 rounded mb-5 w-full"
         data-testid="edit_agreement_header"
         id="agreementables_header">agreementables</div>
    {#if agreementableWorkIntervals}
    <div class="agreementable-work-intervals">
      {#each agreementableWorkIntervals as agreementable}
        <div><input type="checkbox"
          on:click={() => countAgreementablesToAdd(agreementable)}
        ></div>
        <div class="hover:bg-myblue-100 cursor-pointer">{agreementable.start.substring(0, agreementable.start.indexOf('T'))}</div>
        <div class="hover:bg-myblue-100 cursor-pointer">{agreementable.hhmm}</div>
        <div class="hover:bg-myblue-100 cursor-pointer">{agreementable.description}</div>
      {/each}
    </div>
    {/if}
  {/if}
</div>

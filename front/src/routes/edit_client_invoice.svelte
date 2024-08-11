<style>
  .client-form-fields {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    width: 100%;
    margin-left: 3px;
  }

  .edit-invoice-menu {
    display: flex;
    flex-direction: row;
  }

  .client-form-fields > * {
    margin-bottom: 2px;
  }

  .field-label {
    text-align: left;
    width: 110px;
  }

  .new-invoice {
    font-size: 9pt;
  }

  .menu-item {
    color: black;
    margin-left: 2px;
    margi-right: 2px;
  }

  .invoiceable-work-intervals {
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
    type InvoiceCrud, InvoiceItemStore,
    InvoiceStore,
    WorkIntervalListsByClient, WorkTypeStore
  } from "../stores";

  import { DatePicker } from "@svelte-plugins/datepicker";
  import { format } from 'date-fns';
  import {type Client} from "../models/client";
  import {onDestroy} from "svelte";
  import InvoiceService from "../services/invoice.service";
  import {type Invoice} from "../models/invoice";
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkInterval} from "../models/work_interval";
  import InvoiceItemService from "../services/invoice_item.service";
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
  let invoice: Invoice;
  $: invoice
  const unsubInvoice = InvoiceStore.subscribe((icrud: InvoiceCrud) => {
    if (icrud) {
      if (!Array.isArray(icrud.payload)) {
        invoice = icrud.payload as Invoice;

        startDate = new Date(invoice.issued);
        formattedYmdIssue = formatDate(startDate);
      }
    }
  });
  onDestroy(unsubInvoice)
  $: formattedYmdIssue = formatDate(startDate);
  function updateInvoice(): void {
    invoice.issued = (new Date(formattedYmdIssue)).toUTCString();
    InvoiceService.update({
      client: client.id,
      issued: invoice.issued
    }).then((response: any) => {
      const created = response.data;
      InvoiceStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }

  let mode = 'invoiced-items';
  $: mode
  function setMode(next: string): void {
    mode = next;
    if (mode === 'invoiceables') {
      retrieveInvoiceables();
    }
  }

  let invoiceableWorkIntervals: WorkInterval[];
  $: invoiceableWorkIntervals
  let invoiceableChecks: boolean[] = [];
  $: invoiceableChecks

  function retrieveInvoiceables(): void {
    invoiceableChecks = [];
    WorkIntervalService.find({
      client: client.id,
      invoice_item: 'isnull'
    }).then((response: any) => {
      // debugger;
      const founds = response.data;
      invoiceableWorkIntervals = founds
      invoiceableWorkIntervals.forEach((interval: WorkInterval) => {
        invoiceableChecks[interval.id] = false;
      });
    });
  }

  let workTypes: WorkType[] = [];
  $: workTypes
  let workTypesByName: {[key: string]: WorkType} = {};
  $: workTypesByName
  function retrieveWorkTypes(): void {
    WorkTypeService.find({}).then((response: any) => {
      workTypes = response.data;
      workTypesByName = {}
      workTypes.forEach((wt: WorkType) => {
        workTypesByName[wt.name] = wt;
      });
      WorkTypeStore.set({
        type: crud.READ,
        payload: workTypes
      });
    });
  }

  function addInvoiceables(): void {
    const work_type = workTypesByName['time'];
    invoiceableWorkIntervals.forEach((wi: WorkInterval) => {
      if (invoiceableChecks[wi.id]) {
        InvoiceItemService.create({
          invoice: invoice.id,
          work_interval: wi.id,
          work_type: work_type.id
        }).then((response) => {
          const created = response.data;
          if (created) {
            InvoiceItemStore.set({
              type: crud.CREATE,
              payload: created
            });
          }
        });
      }
    });
  }

  let invoiceablesToAdd = 0;
  $: invoiceablesToAdd
  function countInvoiceablesToAdd(next: WorkInterval): number {
    debugger;
    invoiceableChecks[next.id] = !invoiceableChecks[next.id];
    let trues = 0;
    invoiceableChecks.forEach((checked: boolean) => {
      trues += checked ? 1 : 0;
    })
    invoiceablesToAdd = trues;
    return trues;
  }


</script>
<div class="new-invoice flex flex-col border-myroon-100 border p-3 mr-6 ml-3 rounded w-full text-myhigh_white"
     style="min-width: 226px; max-width: 375px; font-size: 10pt;" data-testid="edit_invoice"
>
  <div class="bg-mywood-900 rounded mb-5 w-full" data-testid="edit_invoice_header" id="edit_invoice_header">edit invoice</div>
  <div class="client-form-fields text-mywood-900" data-testid="edit_invoice_form">
    <div><div class="" data-testid="edit_invoice_name">ymd issue:</div></div>
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
    <div><div class="" data-testid="edit_invoice_name">ymd create:</div></div>
    <div>{invoice.created.substring(0, invoice.created.indexOf(' '))}</div>
  </div>
  <div class="edit-invoice-menu flex flex-row ml-3 mb-3 mt-4">
    {#if mode!=='invoiced-items'}
      <div on:click={() => {setMode('invoiced-items')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6"
           style="width:150px;"
      >
        invoiced-items
      </div>
    {/if}
    {#if mode!=='invoiceables'}
      <div on:click={() => {setMode('invoiceables')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        invoiceables
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
  {#if mode==='invoiceables'}
    <div class="bg-mywood-100 rounded mb-5 w-full"
         data-testid="edit_invoice_header"
         id="invoiceables_header">invoiceables</div>
    {#if invoiceableWorkIntervals}
    <div class="invoiceable-work-intervals">
      {#each invoiceableWorkIntervals as invoiceable}
        <div><input type="checkbox"
          on:click={() => countInvoiceablesToAdd(invoiceable)}
        ></div>
        <div class="hover:bg-myblue-100 cursor-pointer">{invoiceable.start.substring(0, invoiceable.start.indexOf('T'))}</div>
        <div class="hover:bg-myblue-100 cursor-pointer">{invoiceable.hhmm}</div>
        <div class="hover:bg-myblue-100 cursor-pointer">{invoiceable.description}</div>
      {/each}
    </div>
    {/if}
    {#if invoiceablesToAdd > 0}
    <div class="mt-6 text-myhigh_white hover:drop-shadow w-full">
      <button on:click={addInvoiceables}
              type="button"
              value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
              style="margin: auto; width: 220px;"
              data-testid="create_client_button"
      >
        add {invoiceablesToAdd} invoiceable{invoiceablesToAdd && invoiceablesToAdd === 1 ? '' : 's'} to invoice
      </button>
    </div>
    {/if}
  {/if}
</div>

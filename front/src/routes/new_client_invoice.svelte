<style>
  .client-form-fields {
    margin-left: 4px;
    display: grid;
    grid-template-columns: 1fr;
    width: 180px;
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

</style>
<script lang="ts">

  import {type ClientCrud, ClientStore, crud, InvoiceStore} from "../stores";


  import { DatePicker } from "@svelte-plugins/datepicker";
  import { format } from 'date-fns';
  import {type Client} from "../models/client";
  import {onDestroy} from "svelte";
  import InvoiceService from "../services/invoice.service";

  let startDate = new Date();
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
      client = ccrud.payload as Client
    }
  });
  onDestroy(unsubClient)

  $: formattedYmdIssue = formatDate(startDate);
  function createInvoice(): void {
    InvoiceService.create({
      client: client.id
    }).then((response: any) => {
      const created = response.data;
      InvoiceStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }

</script>
<div class="new-invoice flex flex-col border-myroon-100 border p-3 mr-6 ml-3 rounded w-full text-myhigh_white"
     style="min-width: 226px; max-width: 375px; font-size: 10pt;" data-testid="new_invoice"
>
  <div class="bg-mywood-900 rounded mb-5 w-full" data-testid="new_invoice_header" id="new_invoice_header">new invoice</div>
  <div class="client-form-fields text-mywood-900" data-testid="new_invoice_form">
    <label class="field-label" data-testid="new_invoice_name">ymd issue
      <DatePicker bind:isOpen bind:startDate enableFutureDates={true}>
        <input type="text"
               placeholder="Select ymd issue"
               bind:value={formattedYmdIssue}
               on:click={toggleDatePicker}
               style="width: 150px; font-size: 9pt; height: 18px; text-align: center;"
        />
      </DatePicker>
    </label>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow">
    <button on:click={createInvoice}
            type="button"
            value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
            style="margin: auto;"
            data-testid="create_client_button"
    >
      create
    </button>
  </div>
</div>

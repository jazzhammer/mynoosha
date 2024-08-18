<style>

  .search-text {
    font-size: 9pt;
    height: 18px;
    width: 80px;
    text-align: center;
  }

  .search-agreement {
    display: flex;
    flex-direction: row;
  }
</style>
<script lang="ts">
  import {type Agreement} from '../models/agreement';
  import AgreementService from "../services/agreement.service";
  import type {Client} from "../models/client";
  import Ymd from "./ymd.svelte";
  import {MessageStore} from "../stores";
  let searchTerm = '';
  $: searchTerm

  export let client: Client | null;
  $: client

  export let foundAgreements = (agreements: Agreement[]): void => {
    MessageStore.set({
      type: '',
      message: `found agreements:${agreements ? agreements.length: 'none'}`
    });

  }

  let initialYmdFrom = new Date();
  initialYmdFrom.setMonth(initialYmdFrom.getMonth() - 1);
  initialYmdFrom.setDate(1);

  let initialYmdThrough = new Date();
  initialYmdThrough.setMonth(initialYmdThrough.getMonth() + 1);
  initialYmdThrough.setDate(0);

  let ymdFrom: string = initialYmdFrom.toISOString().split('T')[0];
  const selectYmdFrom = (next: string): void => {
    ymdFrom = next;
    executeSearch();
  }

  let ymdThrough: string = initialYmdThrough.toISOString().split('T')[0];
  const selectYmdThrough = (next: string): void => {
    ymdThrough = next;
    executeSearch();
  }

  let timeoutSearchAgreement: any;
  const executeSearch = (): void => {
    AgreementService.find({
      search: searchTerm.trim(),
      client: client.id,
      created_from: ymdFrom,
      created_through: ymdThrough
    }).then((response: any) => {
      const agreements = response.data;
      foundAgreements(agreements);
    })
  }

  const searchAgreement = (): void => {
    if (timeoutSearchAgreement) {
      clearTimeout(timeoutSearchAgreement);
    }
    if (client) {
      MessageStore.set({
        type: '',
        message: 'searching agreements...'
      });
      timeoutSearchAgreement = setTimeout(() => {
        executeSearch();
      }, 300);
    } else {
      MessageStore.set({
        type: '',
        message: 'require a client to search for agreements'
      });
    }
  }
</script>
<div class="search-agreement">
  <div><input bind:value={searchTerm}
              on:keyup={searchAgreement}
              type="text" placeholder="search"
              class="search-text" on:focus={(e) => e?.target?.select()}>
  </div>
  <div style="margin-left: 4px; margin-right: 4px;">created from</div>
  <Ymd initialYmd={initialYmdFrom} selectYmd={selectYmdFrom}></Ymd>
  <div style="margin-left: 4px; margin-right: 4px;">through</div>
  <Ymd initialYmd={initialYmdThrough} selectYmd={selectYmdThrough}></Ymd>
</div>
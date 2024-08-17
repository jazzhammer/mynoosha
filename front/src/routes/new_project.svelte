<style>
  .new-project {
    width: calc(100% - 5px);
    height: 80lvh;
    margin: 3px;
  }
  .project-form {
    display: grid;
    grid-template-columns: 1fr 4fr;
  }
  .project-form > * {
    margin-top: 4px;
    font-size: 9pt;
  }
  .agreement-search {

  }
  .agreement-search > * {
    margin-right: 5px;
  }
</style>
<script lang="ts">
  import SearchAgreement from './search-agreement.svelte';
  import Ymd from './ymd.svelte';
  import type {Client} from "../models/client";
  import type {Agreement} from "../models/agreement";
  import AgreementService from "../services/agreement.service";
  export let client: Client;
  $: client

  let agreements: Agreement[];
  $: agreements

  const foundAgreements = (next: Agreement[]): void => {
    agreements = next;
  }
  let count_agreements = 0;
  $: count_agreements
  if (client) {
    AgreementService.count({
      client: client.id
    }).then((response: any) => {
      count_agreements = response.data;
    });
  }
</script>
<div class="new-project rounded-xl">
  <div class="w-full bg-myroon-100 text-myhigh_white text-left pl-4">new project</div>
  <div class="flex flex-row text-mywood-900 justify-start">
    <div class="flex flex-col text-left project-form">
      <div><label for="name">name</label></div>
      <div><input id="name" type="text" style="width: 100%; font-size: 9pt; height: 20px;"/></div>
      <div><label for="description">description</label></div>
      <div><textarea id="description" style="width: 100%; height: 100px; font-size: 9pt;"></textarea></div>
      <div class="flex flex-col">
        <div><label for="agreement_id">agreement (total {count_agreements})</label></div>
        {#if !count_agreements}
          <div on:click={} class="rounded-md bg-mywood-100 w-9/12 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer">
            new agreement
          </div>
        {/if}
      </div>
      <div id="agreement_id" class="flex flex-row agreement-search">
        <SearchAgreement client={client} foundAgreements={foundAgreements}></SearchAgreement>
      </div>
    </div>
  </div>

</div>
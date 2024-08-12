<style>
  .agreement-list {
    display: grid;
    grid-template-columns: 1fr;
    font-size: 9pt;
  }
  .agreement-list-header {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 9pt;
  }
  .agreement-field {
    text-align: center;
  }
</style>

<script lang="ts">
  import {type Agreement} from '../models/agreement';
  export let agreements: Agreement[] = [];

  export let selectAgreement: (agreement: Agreement) => void;



</script>
<div class="agreement-list w-full border border-myblue-50">
  <div class="agreement-list-header bg-mylow_white">ymdIssue</div>
  {#each agreements as agreement}
    <div class="agreement-field text-black cursor-pointer hover:bg-myblue-100" on:click={() => {selectAgreement(agreement)}}>
      {agreement.name}
    </div>
  {/each}
</div>

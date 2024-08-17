<style>
  .agreement-list {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
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
  <div class="agreement-list-header bg-mymid_white">id</div>
  <div class="agreement-list-header bg-mymid_white">name</div>
  <div class="agreement-list-header bg-mymid_white">created</div>
  {#each agreements as agreement}
    <div  on:click={() => {selectAgreement(agreement)}}
          class="agreement-field text-black text-left cursor-pointer hover:bg-myblue-100"
    >
      {agreement.id}
    </div>
    <div  on:click={() => {selectAgreement(agreement)}}
          class="agreement-field text-black text-left cursor-pointer hover:bg-myblue-100"
    >
      {agreement.name}
    </div>
    <div  on:click={() => {selectAgreement(agreement)}}
          class="agreement-field text-black text-left cursor-pointer hover:bg-myblue-100"
    >
      {agreement.created}
    </div>
  {/each}
</div>

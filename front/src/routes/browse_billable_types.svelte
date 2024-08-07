<style>
</style>
<script lang="ts">
  import {type BillableTypeCrud, BillableTypeStore, crud} from "../stores";
  import type {BillableType} from "../models/billable_type";
  import {onDestroy} from "svelte";

  let billable_type: BillableType;
  $: billable_type
  const unsubBillableType = BillableTypeStore.subscribe((ccrud: BillableTypeCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      billable_type = ccrud.payload as BillableType
    }
  });
  onDestroy(unsubBillableType);

</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="browse_billable_types">
  browse
</div>

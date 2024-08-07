<style>
</style>
<script lang="ts">
  import {type WorkerCrud, WorkerStore, crud} from "../stores";
  import type {Worker} from "../models/worker";
  import {onDestroy} from "svelte";

  let worker: Worker;
  $: worker
  const unsubWorker = WorkerStore.subscribe((ccrud: WorkerCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      worker = ccrud.payload as Worker
    }
  });
  onDestroy(unsubWorker);

</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="browse_workers">
  browse
</div>

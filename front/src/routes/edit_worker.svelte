<style>
  .worker-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 200px;
  }
  .worker-form-fields > * {
    margin-bottom: 2px;
  }
  .worker-form-header {
    width: 265px;
  }
  .field-label {
    text-align: left;
  }
  .field-input {
    text-align: left;
    width: 200px;
    margin-left: 3px;
  }
</style>
<script lang="ts">
  import WorkerService from '../services/worker.service';
  import {type WorkerCrud, WorkerStore, crud} from "../stores";
  import type {Worker} from "../models/worker";
  import {onDestroy} from "svelte";
  // ------------------------------------------------------------
  let last_name ='';
  $: last_name
  let first_name ='';
  $: first_name
  // ------------------------------------------------------------
  let worker: Worker;
  $: worker
  const unsubWorker = WorkerStore.subscribe((ccrud: WorkerCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      worker = ccrud.payload as Worker
      last_name = worker.last_name as string;
      first_name = worker.first_name as string;
    }
  });
  onDestroy(unsubWorker);

  function updateWorker(): void {
    WorkerService.update({
      id: worker.id,
      last_name,
      first_name,
    }).then((response: any) => {
      const updated = response.data;
      worker = updated;
      WorkerStore.set({
        type: crud.UPDATE,
        payload: updated
      });
    })
  }

  function keyupName(event: any) {
    if (event.key === 'Enter') {
      updateWorker();
    }
    console.log(name)
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="new_worker">
  <div class="worker-form-header bg-mywood-900 rounded mb-5" data-testid="new_worker_header" id="new_worker_header">edit worker</div>
  <div class="worker-form-fields w-3/12 text-mywood-900" data-testid="new_worker_form">
    <label class="field-label" data-testid="new_worker_name">last_name
      <input type="text"
             bind:value={last_name}
             on:keyup={keyupName}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             id="new_worker_last_name"
             data-testid="new_worker_last_name_input"/>
    </label>
    <label class="field-label" data-testid="new_worker_name">first_name
      <input type="text"
             bind:value={first_name}
             on:keyup={keyupName}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             id="new_worker_first_name"
             data-testid="new_worker_first_name_input"/>
    </label>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow">
    <button on:click={updateWorker}
            type="button"
            value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
            style="margin: auto;"
            data-testid="create_worker_button"
    >
      update
    </button>
  </div>
</div>

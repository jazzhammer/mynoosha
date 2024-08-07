<style>
  .worker-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 180px;
  }

  .worker-form-fields > * {
    margin-bottom: 2px;
  }

  .field-label {
    text-align: left;
    width: 110px;
  }

  .worker-form-header {
    width: 262px;
  }
</style>
<script lang="ts">
  import WorkerService from '../services/worker.service';
  import {WorkerStore, crud} from "../stores";

  let last_name ='';
  $: last_name
  let first_name ='';
  $: first_name

  function createWorker(): void {
    WorkerService.create({
      last_name,
      first_name,
    }).then((response: any) => {
      const created = response.data;
      WorkerStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }
  function keyupName(event: any) {
    if (event.key === 'Enter') {
      createWorker();
    }
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="new_worker"
>
  <div class="worker-form-header bg-mywood-900 rounded mb-5" data-testid="new_worker_header" id="new_worker_header">new worker</div>
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
    <div class="mt-6 text-myhigh_white hover:drop-shadow">
      <button on:click={createWorker}
              type="button"
              value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
              style="margin: auto;"
              data-testid="create_worker_button"
      >
        create
      </button>
    </div>
  </div>
</div>
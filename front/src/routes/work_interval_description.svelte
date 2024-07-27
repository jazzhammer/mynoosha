<style>
.editor {
  resize: none;
  outline: none;
  width: 100%;
  padding: 10px;
  border: none;
  height: 100%;
}
</style>
<script lang="ts">
  import type {WorkInterval} from "../models/work_interval";
  import WorkIntervalService from "../services/work_interval.service";
  import markdownify from "../utils/markdown";
  import type {WorkIntervalCrud} from "../stores";
  import {crud, WorkIntervalStore} from "../stores";
  import {onDestroy} from "svelte";
  let workInterval: WorkInterval | null = null;
  const unsubWorkIntervalStore = WorkIntervalStore.subscribe((wicrud: WorkIntervalCrud) => {
    if (wicrud && wicrud.type === crud.READ) {
      if (!Array.isArray(wicrud)) {
        workInterval = wicrud.payload as WorkInterval;
        nextWorkIntervalDescription = workInterval.description;
      }
    }
  });
  onDestroy(unsubWorkIntervalStore);

  let nextWorkIntervalDescription = workInterval?.description;

  $: workInterval
  $: nextWorkIntervalDescription


  let debounceWorkIntervalDescription: any;
  function updateWorkIntervalDescription(): void {
    if (debounceWorkIntervalDescription) {
      clearTimeout(debounceWorkIntervalDescription);
    }
    debounceWorkIntervalDescription = setTimeout(
      () => {
        if (workInterval) {
          workInterval.description = nextWorkIntervalDescription;
          WorkIntervalService.update({
            id: workInterval.id,
            description: workInterval.description
          }).then((response: any) => {
            nextWorkIntervalDescription = workInterval?.description;
            WorkIntervalStore.set({
              type: crud.UPDATE,
              payload: workInterval as WorkInterval
            });
          });
        }
      }, 300
    );
  }
</script>
<div class="flex flex-row h-full" style="font-size:8pt;">
  {#if workInterval}
    <div style="width: 100%; height: 100%">
      <textarea style="font-size:8pt; line-height: 100%"
                class="editor"
          bind:value={nextWorkIntervalDescription}
          on:keyup={updateWorkIntervalDescription}></textarea>
    </div>
  {/if}
</div>
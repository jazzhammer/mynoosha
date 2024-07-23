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

  export let workInterval: WorkInterval;
  let nextWorkIntervalDescription = workInterval?.description;
  let nextMD = workInterval?.description;

  $: workInterval
  $: nextWorkIntervalDescription
  $: nextMD


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
            nextWorkIntervalDescription = workInterval.description;
            nextMD = markdownify(workInterval.description);
          });
        }
      }, 300
    );
  }
</script>
<div class="flex flex-row w-full h-full" style="font-size:8pt;">
  {#if workInterval}
    <div style="width: 50%; height: 100%">
      <textarea style="font-size:8pt; line-height: 100%"
                class="editor"
          bind:value={nextWorkIntervalDescription}
          on:keyup={updateWorkIntervalDescription}></textarea>
    </div>
    <div style="width: 50%; height: 100%" class="p-2">{@html nextMD}</div>
  {/if}
</div>
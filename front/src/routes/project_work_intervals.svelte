<style>
  .project-work-intervals {

  }
</style>
<script lang="ts">
  import type {Project} from "../models/project";
  // import TimeRecorder from './time_recorder.svelte';
  import WorkIntervalList from './work_interval_list.svelte';
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkInterval} from "../models/work_interval";
  import {type WorkIntervalCrud, WorkIntervalStore} from "../stores";
  import {onDestroy} from "svelte";

  export let project: Project;
  $: project

  let workIntervals: WorkInterval[];
  $: workIntervals

  const getWorkIntervals = (): void => {
    if (project) {
      WorkIntervalService.find({project: project.id}).then((response: any) => {
        workIntervals = response.data;

      });
    }
  }
  getWorkIntervals();
  const unsubWorkInterval = WorkIntervalStore.subscribe((wicrud: WorkIntervalCrud) => {
    if (!Array.isArray(wicrud)) {
      getWorkIntervals();
    }
  })
  onDestroy(unsubWorkInterval);
  const selectWorkInterval = (next: WorkInterval): void => {
    console.log(`project work intervals: selectedWorkInterval: ${next.id}`);
  }
</script>
<div class="project-work-intervals">
  <WorkIntervalList workIntervals={workIntervals} selectWorkInterval={selectWorkInterval}></WorkIntervalList>
</div>
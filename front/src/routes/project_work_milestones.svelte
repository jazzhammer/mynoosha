<style>
  .project-work-milestones {

  }
</style>
<script lang="ts">
  import type {Project} from "../models/project";
  // import TimeRecorder from './time_recorder.svelte';
  import WorkMilestoneList from './work_milestone_list.svelte';
  import WorkMilestoneService from "../services/work_milestone.service";
  import type {WorkMilestone} from "../models/work_milestone";
  import {type WorkMilestoneCrud, WorkMilestoneStore} from "../stores";
  import {onDestroy} from "svelte";

  export let project: Project;
  $: project

  let workMilestones: WorkMilestone[];
  $: workMilestones

  const getWorkMilestones = (): void => {
    if (project) {
      WorkMilestoneService.find({project: project.id}).then((response: any) => {
        workMilestones = response.data;

      });
    }
  }
  getWorkMilestones();
  const unsubWorkMilestone = WorkMilestoneStore.subscribe((wicrud: WorkMilestoneCrud) => {
    if (!Array.isArray(wicrud)) {
      getWorkMilestones();
    }
  })
  onDestroy(unsubWorkMilestone);
  const selectWorkMilestone = (next: WorkMilestone): void => {
    console.log(`project work milestones: selectedWorkMilestone: ${next.id}`);
  }
</script>
<div class="project-work-milestones">
  <WorkMilestoneList workMilestones={workMilestones} selectWorkMilestone={selectWorkMilestone}></WorkMilestoneList>
</div>
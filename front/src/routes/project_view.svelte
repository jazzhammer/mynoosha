<style>
  .project-view {
    display: flex;
    flex-direction: column;
  }

  .project-demogs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    max-width: 350px;
  }
  .work-intervals {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .work-intervals-assigned {
    border: 1px solid #ddddff;
  }

  .work-intervals-other {
    border: 1px solid #ddddff;
  }

</style>
<script lang="ts">
  import WorkIntervalList from './work_interval_list.svelte';
  import SearchWorkInterval from './search_work_interval.svelte';
  import {crud, MessageStore, type ProjectCrud, ProjectStore, type WorkIntervalCrud, WorkIntervalStore} from "../stores";
  import type {Project} from "../models/project";
  import {onDestroy} from "svelte";
  import ProjectWorkIntervals from './project_work_intervals.svelte';
  import type {WorkInterval} from "../models/work_interval";
  import WorkIntervalService from "../services/work_interval.service";
  let project: Project;
  $: project
  let unsubProject = ProjectStore.subscribe((pcrud: ProjectCrud) => {
    if (pcrud && (pcrud.type===crud.READ || pcrud.type===crud.CREATE)) {
      if (!Array.isArray(pcrud.payload) ) {
        project = pcrud.payload;
      }
    }
  });
  onDestroy(unsubProject);

  let otherWorkIntervals: WorkInterval[];
  $: otherWorkIntervals

  let unsubWorkInterval = WorkIntervalStore.subscribe((wicrud: WorkIntervalCrud) => {
    if (wicrud && (wicrud.type === crud.READ || wicrud.type === crud.CREATE || wicrud.type === crud.UPDATE)) {
      if (!Array.isArray(wicrud.payload) ) {
        const nextWorkInterval = wicrud.payload;
        if (otherWorkIntervals) {
          const i = otherWorkIntervals.findIndex((wi: WorkInterval) => {
            return wi.id === nextWorkInterval.id;
          })
          if (i >= 0) {
            const nextOtherWorkIntervals = structuredClone(otherWorkIntervals);
            nextOtherWorkIntervals[i] = nextWorkInterval;
            otherWorkIntervals = nextOtherWorkIntervals;
          }
        }
      }
    }
  });
  onDestroy(unsubWorkInterval);

  const foundWorkIntervals = (founds: WorkInterval[]): void => {
    otherWorkIntervals = founds;
    MessageStore.set({
      type: '',
      message: `found work intervals: ${otherWorkIntervals ? otherWorkIntervals.length : 'none'}`
    });
  }
  const selectWorkInterval = (next: WorkInterval): void => {
    MessageStore.set({
      type: '',
      message: `selected workInterval: ${next.id}`
    });
    if (project) {
      next.project = project.id;
      WorkIntervalService.update(next).then((response: any) => {
        const updated = response.data;
        WorkIntervalStore.set({
          type: crud.UPDATE,
          payload: updated
        })
      });
    }
  }
</script>
{#if project}
<div class="project-view">
  <div class="bg-mymid_white flex flex-row pl-2">
    <div class="mr-5">project: {project?.name} [{project?.id}]</div>
    <div class="mr-5">client: {project?.client ? project?.client : 'none'}</div>
    <div class="mr-5">agreement: {project?.agreement ? project?.agreement : 'none'}</div>
  </div>
  <div class="project-demogs text-left ml-2">
    <div>id</div><div>{project?.id}</div>
    <div>name</div><div>{project?.name}</div>
    <div>description</div><div>{project?.description}</div>
    <div>agreement_id</div><div>{project?.agreement}</div>
<!--    <div>client_id</div><div>{project?.client}</div>-->
    <div>created</div><div>{project?.created?.split("T")[0]}</div>
  </div>
  <div class="bg-mymid_white">work intervals</div>
  <div class="work-intervals">
    <div class="flex flex-col m-2 work-intervals-assigned">
      <div class="text-mywood-900">assigned to project</div>
      <ProjectWorkIntervals project={project}></ProjectWorkIntervals>
    </div>
    <div class="flex flex-col m-2 work-intervals-other">
      <div class="text-mywood-900">search other work intervals</div>
      <SearchWorkInterval foundWorkIntervals={foundWorkIntervals}></SearchWorkInterval>
      {#if otherWorkIntervals && otherWorkIntervals.length > 0}
      <div class="text-left pl-2 w-full text-mywood-900">select to assign to project:</div>
      <WorkIntervalList selectWorkInterval={selectWorkInterval}
                        workIntervals={otherWorkIntervals}>
      </WorkIntervalList>
      {/if}
    </div>
  </div>
</div>
{/if}

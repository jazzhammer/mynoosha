<style>
  .work-interval-project {
    width: 100%;
    height: 85lvh;
  }
</style>
<script lang="ts">
  import SearchProject from './search_project.svelte';
  import {type WorkInterval} from '../models/work_interval';
  import type {Project} from "../models/project";

  export let workInterval: WorkInterval;
  $: workInterval

  let projects: Project[] = [];
  $: projects

  export let updatedWorkInterval = (updated: WorkInterval) => {
    console.log(`updated workInterval: ${JSON.stringify(updated)}`);
  }

  const canUpdate = (): boolean => {
    return true;
  }

  const updateWorkInterval = (): void => {
    console.log(`override this function workIntervalProject.updateWorkInterval = (): void => {}`)
    updatedWorkInterval(workInterval);
  }

  const foundProjects = (founds: Project[]): void => {
    projects = founds;
  }
</script>
<div class="work-interval-project flex flex-col">
  <div class="work-interval-project-header">work interval project</div>
  <div>
    <SearchProject foundProjects={foundProjects}></SearchProject>
  </div>
  {#if canUpdate()}
    <div on:click={updateWorkInterval}>update work interval</div>
  {/if}
</div>
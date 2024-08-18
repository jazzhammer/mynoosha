<style>
  .project-list {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
    font-size: 9pt;
  }
  .project-list-header {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 9pt;
  }
  .project-field {
    text-align: center;
  }
</style>

<script lang="ts">
  import {type Project} from '../models/project';
  import ProjectView from './project_view.svelte';
  import type {ProjectType} from "../models/project_type";
  export let projectTypes: ProjectType[] = [];

  export let selectProject: (project: Project) => void;



</script>
<div class="flex flex-col">
  <div class="project-list w-full border border-myblue-50">
    <div class="project-list-header bg-mylow_white">id</div>
    <div class="project-list-header bg-mylow_white">name</div>
    {#each projectTypes as project}
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.id}
      </div>
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.name}
      </div>
    {/each}
  </div>
  <div>
    <ProjectView></ProjectView>
  </div>
</div>

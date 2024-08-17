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
  export let projects: Project[] = [];

  export let selectProject: (project: Project) => void;



</script>
<div class="flex flex-col">
  <div class="project-list w-full border border-myblue-50">
    <div class="project-list-header bg-mylow_white">id</div>
    <div class="project-list-header bg-mylow_white">name</div>
    <div class="project-list-header bg-mylow_white">description</div>
    <div class="project-list-header bg-mylow_white">agreement</div>
    <div class="project-list-header bg-mylow_white">client</div>
    <div class="project-list-header bg-mylow_white">created</div>
    {#each projects as project}
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.id}
      </div>
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.name}
      </div>
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.description}
      </div>
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.agreement}
      </div>
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.client}
      </div>
      <div on:click={() => {selectProject(project)}} class="project-field text-black cursor-pointer hover:bg-myblue-100">
        {project.created?.split('T')[0]}
      </div>
    {/each}
  </div>
  <div>
    <ProjectView></ProjectView>
  </div>
</div>

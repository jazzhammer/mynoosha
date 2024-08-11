<style>
  .project-list {
    display: grid;
    grid-template-columns: 1fr;
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
  export let projects: Project[] = [];

  export let selectProject: (project: Project) => void;



</script>
<div class="project-list w-full border border-myblue-50">
  <div class="project-list-header bg-mylow_white">ymdIssue</div>
  {#each projects as project}
    <div class="project-field text-black cursor-pointer hover:bg-myblue-100" on:click={() => {selectProject(project)}}>
      {project.name}
    </div>
  {/each}
</div>

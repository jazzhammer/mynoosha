<style>
  .project-type-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    font-size: 9pt;
  }
  .project-type-list-header {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 9pt;
  }
  .project-type-field {
    text-align: center;
  }
</style>

<script lang="ts">
  import {type ProjectType} from '../models/project_type';
  import ProjectTypeView from './project_type_view.svelte';
  export let projectTypes: ProjectType[] = [];

  export let selectProjectType: (project: ProjectType) => void;



</script>
<div class="flex flex-col">
  <div class="project-type-list w-full border border-myblue-50">
    <div class="project-type-list-header bg-mylow_white">id</div>
    <div class="project-type-list-header bg-mylow_white">name</div>
<!--    <div class="project-type-list-header bg-mylow_white">description</div>-->
<!--    <div class="project-type-list-header bg-mylow_white">agreement</div>-->
<!--    <div class="project-type-list-header bg-mylow_white">client</div>-->
<!--    <div class="project-type-list-header bg-mylow_white">created</div>-->
    {#each projectTypes as projectType}
      <div on:click={() => {selectProjectType(projectType)}} class="project-type-field text-black cursor-pointer hover:bg-myblue-100">
        {projectType.id}
      </div>
      <div on:click={() => {selectProjectType(projectType)}} class="project-type-field text-black cursor-pointer hover:bg-myblue-100">
        {projectType.name}
      </div>
<!--      <div on:click={() => {selectProjectType(projectType)}} class="project-type-field text-black cursor-pointer hover:bg-myblue-100">-->
<!--        {projectType.description}-->
<!--      </div>-->
<!--      <div on:click={() => {selectProjectType(projectType)}} class="project-type-field text-black cursor-pointer hover:bg-myblue-100">-->
<!--        {projectType.agreement}-->
<!--      </div>-->
<!--      <div on:click={() => {selectProjectType(projectType)}} class="project-type-field text-black cursor-pointer hover:bg-myblue-100">-->
<!--        {projectType.client}-->
<!--      </div>-->
<!--      <div on:click={() => {selectProjectType(projectType)}} class="project-type-field text-black cursor-pointer hover:bg-myblue-100">-->
<!--        {projectType.created?.split('T')[0]}-->
<!--      </div>-->
    {/each}
  </div>
  <div>
    <ProjectTypeView></ProjectTypeView>
  </div>
</div>

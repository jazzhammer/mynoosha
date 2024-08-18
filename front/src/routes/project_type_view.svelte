<style>
  .project-type-view {
    display: flex;
    flex-direction: column;
    max-width: 250px;
  }

  .project-type-demogs {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
</style>
<script lang="ts">

  import {crud, type ProjectTypeCrud, ProjectTypeStore} from "../stores";
  import type {ProjectType} from "../models/project_type";
  import {onDestroy} from "svelte";

  let projectType: ProjectType;
  $: projectType
  let unsubProjectType = ProjectTypeStore.subscribe((pcrud: ProjectTypeCrud) => {
    if (pcrud && (pcrud.type === crud.READ || pcrud.type === crud.CREATE)) {
      if (!Array.isArray(pcrud.payload) ) {
        projectType = pcrud.payload;
      }
    }
  });
  onDestroy(unsubProjectType);
</script>
{#if projectType}
<div class="project-type-view">
  <div class="bg-mymid_white">project type: {projectType?.name} [{projectType?.id}]</div>
  <div class="project-type-demogs text-left ml-2">
    <div>id</div><div>{projectType?.id}</div>
    <div>name</div><div>{projectType?.name}</div>
<!--    <div>description</div><div>{projectType?.description}</div>-->
<!--    <div>agreement_id</div><div>{projectType?.agreement}</div>-->
<!--    <div>client_id</div><div>{projectType?.client}</div>-->
<!--    <div>created</div><div>{projectType?.created}</div>-->
  </div>
</div>
{/if}

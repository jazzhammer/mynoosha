<style>
  .project-view {
    display: flex;
    flex-direction: column;
    max-width: 350px;
  }

  .project-demogs {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
</style>
<script lang="ts">

  import {crud, type ProjectCrud, ProjectStore} from "../stores";
  import type {Project} from "../models/project";
  import {onDestroy} from "svelte";

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
</script>
{#if project}
<div class="project-view">
  <div class="bg-mymid_white">project: {project?.name} [{project?.id}]</div>
  <div class="project-demogs text-left ml-2">
    <div>id</div><div>{project?.id}</div>
    <div>name</div><div>{project?.name}</div>
    <div>description</div><div>{project?.description}</div>
    <div>agreement_id</div><div>{project?.agreement}</div>
    <div>client_id</div><div>{project?.client}</div>
    <div>created</div><div>{project?.created?.split("T")[0]}</div>
  </div>
</div>
{/if}

<style>
  .project-view {
    display: flex;
    flex-direction: column;
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
    if (pcrud && pcrud.type===crud.READ) {
      if (!Array.isArray(pcrud.payload) ) {
        project = pcrud.payload;
      }
    }
  });
  onDestroy(unsubProject);
</script>

<div class="project-view">
  <div class="project-demogs">
    <div>id</div><div>{project.id}</div>
    <div>name</div><div>{project.name}</div>
    <div>description</div><div>{project.description}</div>
    <div>agreement_id</div><div>{project.agreement_id}</div>
    <div>created</div><div>{project.created}</div>
  </div>

</div>
<style>
  .new-project-type {
    width: calc(100% - 5px);
    height: 80lvh;
    margin: 3px;
    display: flex;
    flex-direction: column;
  }
  .project-type-form {
    display: grid;
    grid-template-columns: 1fr 3fr;
  }
  .project-type-form > * {
    margin-top: 4px;
    font-size: 9pt;
  }
  .agreement-search {

  }
  .agreement-search > * {
    margin-right: 5px;
  }
</style>
<script lang="ts">
  import ProjectTypeService from "../services/project_type.service";
  import {crud, MessageStore, ProjectTypeStore} from "../stores";
  import type {ProjectType} from "../models/project_type";

  export let createdProjectType = (created: ProjectType) => {
    console.log(`created project type: ${JSON.stringify(created)}`);
  }

  let new_name = '';
  $: new_name

  const createProjectType = (): void => {
    ProjectTypeService.create({
        name: new_name,
    }).then((response: any) => {
      const created = response.data;
      ProjectTypeStore.set({
        type: crud.CREATE,
        payload: created
      });
      createdProjectType(created);
    });
  }
</script>
<div class="new-project-type rounded-xl">
  <div class="w-full bg-myroon-100 text-myhigh_white text-left pl-4">new project</div>
  <div class="flex flex-row text-mywood-900 justify-start">
    <div class="flex flex-col text-left project-type-form w-7/12">
      <div><label for="name">name</label></div>
      <div><input id="name" bind:value={new_name} type="text" style="width: 100%; font-size: 9pt; height: 20px;"/></div>


    </div>
  </div>
  {#if new_name && new_name.trim().length > 0}
    <div on:click={createProjectType}
         class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
         style="width: 150px;"
    >
      create project type
    </div>
  {/if}
</div>
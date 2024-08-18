<style>
  .project_types {
    width: 100%;
  }

  .project_types-header {
    width: 100%;

  }

  .search-row {
    display: flex;
    flex-direction: row;
    width: 100%;
  }

  .search-row > * {
    margin-left: 4px;
  }

  .menu-item {
    padding-left: 4px;
    padding-right: 4px;
    min-width: 80px;
    text-align: center;
    background-color: antiquewhite;
    cursor: pointer;
    border-radius: 2px;
    color: #3b1000;
    margin: 3px;
    font-size: 11pt;
  }
  .menu-item:hover {
    background-color: #2aabd2;
    color: #efefef;
  }
</style>
<script lang="ts">
  import SearchClient from './search-client.svelte';
  import Ymd from './ymd.svelte';
  import type {Client} from "../models/client";
  import {type ClientCrud, ClientStore, crud, MessageStore, ProjectTypeStore} from "../stores";
  import ClientList from './client_list.svelte';
  import {onDestroy} from "svelte";
  import ProjectTypeService from "../services/project_type.service";
  import type {ProjectType} from "../models/project_type";
  import ProjectTypeList from './project_type_list.svelte';
  import ProjectTypeView from './project_type_view.svelte';
  import NewProjectType from './new_project_type.svelte';
  let initialYmdFrom = new Date();
  initialYmdFrom.setMonth(initialYmdFrom.getMonth() - 1)
  initialYmdFrom.setDate(1)

  let initialYmdThrough = new Date();
  initialYmdThrough.setFullYear(initialYmdThrough.getFullYear(), initialYmdThrough.getMonth() + 1, 0);

  let ymdFrom = initialYmdFrom.toISOString().split('T')[0];
  const selectYmdFrom = (next: string): void => {
    ymdFrom = next;
    searchProjectTypes();
  }
  let ymdThrough = initialYmdThrough.toISOString().split('T')[0];
  const selectYmdThrough = (next: string): void => {
    ymdThrough = next;
    searchProjectTypes();
  }

  let clients: Client[];
  $: clients
  let unsubClients = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      if (Array.isArray(ccrud.payload)) {
        clients = ccrud.payload
      }
    }
  });
  onDestroy(unsubClients);

  const foundClients = (founds: Client[]): void => {
    ClientStore.set({
      type: crud.READ,
      payload: founds
    });
  }

  let client: Client;
  $: client

  const selectClient = (next: Client): void => {
    client = next;
    clients = [];
    searchProjectTypes();
  }

  let projectTypes: ProjectType[] = [];
  $: projectTypes
  let projectType: ProjectType;
  $: projectType

  const searchProjectTypes = (): void => {
    ProjectTypeService.find({

    }).then((response: any) => {
      const founds = response.data;
      projectTypes = founds;
      MessageStore.set({
        type: '',
        message: `found project_types: ${founds ? founds.length: 'none'}`
      });
      ProjectTypeStore.set({
        type: crud.READ,
        payload: founds
      });
    });
  }

  const selectProjectType = (next: ProjectType): void => {
    projectType = next;
    projectTypes = [];
    ProjectTypeStore.set({
      type: crud.READ,
      payload: projectType
    });
  }
  let mode = 'browse';
  $: mode
  const setMode = (next: string): void => {
    mode = next;
  }

  const createdProjectType = (next: ProjectType): void => {
      project_type = next;
      mode = 'browse';
  }
</script>
<div class="project_types flex flex-col">
  <div class="project_types-header bg-mywood-100 text-myhigh_white text-xl flex flex-row">
    <div style="margin-left: 10px;">project_types {client ? `for client: ${client.name}` : ''}</div>
    {#if mode!=='new'}
      <div class="menu-item" on:click={() => setMode('new')}>new</div>
    {/if}
    {#if mode!=='browse'}
      <div class="menu-item" on:click={() => setMode('browse')}>browse</div>
    {/if}
  </div>
  {#if projectTypes && projectTypes.length > 0}
    <div class="flex flex-col">
      <div class="ml-3 text-left bg-myhigh_white text-mywood-900">select project type:</div>
      <div>
        <ProjectTypeList projectTypes={projectTypes} selectProjectType={selectProjectType}></ProjectTypeList>
      </div>
    </div>
  {/if}
  {#if projectType}
    <div>
      <div>
        <ProjectTypeView></ProjectTypeView>
      </div>
    </div>
  {/if}
  {#if mode==='new'}
    <div>
      <div>
        <NewProjectType client={client} createdProjectType={createdProjectType}></NewProjectType>
      </div>
    </div>
  {/if}
</div>
<style>
  .projects {
    width: 100%;
  }

  .projects-header {
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
  import {type ClientCrud, ClientStore, crud, MessageStore, ProjectStore} from "../stores";
  import ClientList from './client_list.svelte';
  import {onDestroy} from "svelte";
  import ProjectService, {type ProjectSearchDto} from "../services/project.service";
  import type {Project} from "../models/project";
  import ProjectList from './project_list.svelte';
  import ProjectView from './project_view.svelte';
  import NewProject from './new_project.svelte';
  let initialYmdFrom = new Date();
  initialYmdFrom.setMonth(initialYmdFrom.getMonth() - 1)
  initialYmdFrom.setDate(1)

  let initialYmdThrough = new Date();
  initialYmdThrough.setFullYear(initialYmdThrough.getFullYear(), initialYmdThrough.getMonth() + 1, 0);

  let ymdFrom = initialYmdFrom.toISOString().split('T')[0];
  const selectYmdFrom = (next: string): void => {
    ymdFrom = next;
    searchProjects();
  }
  let ymdThrough = initialYmdThrough.toISOString().split('T')[0];
  const selectYmdThrough = (next: string): void => {
    ymdThrough = next;
    searchProjects();
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

  let client: Client | null;
  $: client

  const selectClient = (next: Client): void => {
    client = next;
    clients = [];
    searchProjects();
  }

  let projects: Project[] = [];
  $: projects

  let project: Project | null;
  $: project

  const getAllProjects = (): void => {
    ProjectService.find({}).then((response: any) => {
      const founds = response.data;
      projects = founds;
      MessageStore.set({
        type: '',
        message: `found projects: ${founds ? founds.length: 'none'}`
      });
      ProjectStore.set({
        type: crud.READ,
        payload: founds
      });
    });
  }

  getAllProjects();

  const searchProjects = (): void => {
    const forSearch: ProjectSearchDto = {
      pre_created_from: ymdFrom,
      post_created_from: ymdThrough
    }
    if (client) {
      forSearch.client = client.id;
    }
    ProjectService.find(forSearch).then((response: any) => {
      const founds = response.data;
      projects = founds;
      MessageStore.set({
        type: '',
        message: `found projects: ${founds ? founds.length: 'none'}`
      });
      ProjectStore.set({
        type: crud.READ,
        payload: founds
      });
    });
  }

  const selectProject = (next: Project): void => {
    project = next;
    projects = [];
    ProjectStore.set({
      type: crud.READ,
      payload: project
    });
    mode = 'edit';
  }
  let mode = 'browse';
  $: mode

  const setMode = (next: string): void => {
    mode = next;
    if (mode === 'browse' || mode === 'new') {
      project = null;
      client = null;
    }
  }

  const createdProject = (next: Project): void => {
      project = next;
      mode = 'edit';
      ProjectStore.set({
        type: crud.CREATE,
        payload: project
      });
  }
</script>
<div class="projects flex flex-col">
  <div class="projects-header bg-mywood-100 text-myhigh_white text-xl flex flex-row">
    <div style="margin-left: 10px;">projects {client ? `for client: ${client.name}` : ''}</div>
    {#if mode!=='new'}
      <div class="menu-item" on:click={() => setMode('new')}>new</div>
    {/if}
    {#if mode!=='browse'}
      <div class="menu-item" on:click={() => setMode('browse')}>browse</div>
    {/if}
  </div>
  {#if mode==='browse'}
    {#if !projects || projects.length === 0}
    <div class="search-row">
      <div style="margin-left: 10px;">
        <SearchClient foundClients={foundClients}></SearchClient>
      </div>
      <div>project created from:</div>
      <div style="margin-left: 10px;">
        <Ymd initialYmd="{initialYmdFrom}" selectYmd={selectYmdFrom}></Ymd>
      </div>
      <div>through:</div>
      <div style="margin-left: 10px;">
        <Ymd initialYmd="{initialYmdThrough}" selectYmd={selectYmdThrough}></Ymd>
      </div>
    </div>
    {/if}
    {#if clients && clients.length > 0 && (!projects || projects.length === 0) }
      <div class="flex flex-col">
        <div class="ml-3 text-left bg-myhigh_white text-mywood-900">select client:</div>
        <div>
          <ClientList clients={clients} selectClient={selectClient}></ClientList>
        </div>
      </div>
    {/if}
  {/if}

  {#if projects && projects.length > 0}
    <div class="flex flex-col">
      <div class="ml-3 text-left bg-myhigh_white text-mywood-900">select project:</div>
      <div>
        <ProjectList projects={projects} selectProject={selectProject}></ProjectList>
      </div>
    </div>
  {/if}
  {#if project}
    <div>
      <div>
        <ProjectView></ProjectView>
      </div>
    </div>
  {/if}
  {#if mode==='new'}
    <div>
      <div>
        <NewProject client={client} createdProject={createdProject}></NewProject>
      </div>
    </div>
  {/if}
</div>
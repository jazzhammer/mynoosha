<style>
  .new-work-milestone {
    width: calc(100% - 5px);
    height: 80lvh;
    margin: 3px;
    display: flex;
    flex-direction: column;
  }
  .work-milestone-form {
    display: grid;
    grid-template-columns: 1fr 3fr;
  }
  .work-milestone-form > * {
    margin-top: 4px;
    font-size: 9pt;
  }
</style>
<script lang="ts">
  import type {Client} from "../models/client";
  import type {Project} from "../models/project";
  import WorkMilestoneService, {type WorkMilestoneDto} from "../services/work_milestone.service";
  import {crud, MessageStore, WorkMilestoneStore} from "../stores";
  import type {WorkMilestone} from "../models/work_milestone";
  import NewClient from './new_client.svelte';
  import NewProject from './new_project.svelte';
  import ClientService from "../services/client.service";
  import SearchClient from './search-client.svelte';
  import SearchProject from './search_project.svelte';
  import ClientList from './client_list.svelte';
  import ProjectList from './project_list.svelte';
  import ProjectService from "../services/project.service";

  export let createdWorkMilestone = (created: WorkMilestone) => {
    console.log(`created milestone: ${JSON.stringify(created)}`);
  }

  let new_description = '';
  $: new_description

  let new_name = '';
  $: new_name

  export let client: Client | null;
  $: client

  export let project: Project | null;
  $: project

  let clients: Client[];
  $: clients

  let projects: Project[];
  $: projects

  const foundClients = (next: Client[]): void => {
    clients = next;
  }

  const foundProjects = (next: Project[]): void => {
    projects = next;
  }

  const countClients = async () => {
    ClientService.count({
    }).then((response: any) => {
      count_clients = response.data;
      if (count_clients < 10) {
        findAllClients();
      }
    });
  }

  const countProjects = async () => {
    ProjectService.count({
    }).then((response: any) => {
      count_clients = response.data;
      if (count_clients < 10) {
        findAllProjects();
      }
    });
  }

  const findAllClients = (): void => {
    ClientService.find({}).then((response: any) => {
      clients = response.data;
      if (clients.length === 1) {
        client = clients[0];
      }
    });
  }

  const findAllProjects = (): void => {
    ProjectService.find({}).then((response: any) => {
      projects = response.data;
      if (projects.length === 1) {
        project = projects[0];
      }
    });
  }

  let count_clients = 0;
  $: count_clients
  countClients();

  let count_projects = 0;
  $: count_projects
  countProjects();


  let client_mode = ''
  $: client_mode

  let project_mode = ''
  $: project_mode

  let agreement_mode = ''
  $: agreement_mode

  const createdProject = (next: Project): void => {
    if (!projects) {
      projects = [];
    }
    projects.push(next);
    project = next;
    project_mode = 'search';
  }

  const createdClient = (next: Client): void => {
    if (!clients) {
      clients = [];
    }
    clients.push(next);
    client = next;
    client_mode = 'search';
    // countClientClients();
  }

  const setProjectMode = (next: string): void => {
    project_mode = next;
    if (project_mode === 'search') {
      // findAllProjects();
    } else if (project_mode === 'new') {
      project = null;
    }
  }

  const setClientMode = (next: string): void => {
    client_mode = next;
    if (client_mode === 'search') {
      findAllClients();
    } else if (client_mode === 'new') {
      client = null;
    }
  }

  const selectProject = (next: Project): void => {
    project = next;
    projects = [];
    project_mode = '';
    MessageStore.set({
      type: '',
      message: `selected project ${project?.name}`
    });
  }

  const selectClient = (next: Client): void => {
    client = next;
    clients = [];
    client_mode = '';
    MessageStore.set({
      type: '',
      message: `selected client ${client?.name}`
    });
  }

  const createWorkMilestone = (): void => {
    const toCreate: WorkMilestoneDto = {
      name: new_name,
      description: new_description
    };
    if (client) {
      toCreate['client'] = client.id;
    }
    WorkMilestoneService.create(toCreate).then((response: any) => {
      const created = response.data;
      WorkMilestoneStore.set({
        type: crud.CREATE,
        payload: created
      });
      createdWorkMilestone(created);
    });
  }
</script>
<div class="new-work-milestone rounded-xl">
  <div class="w-full bg-myroon-100 text-myhigh_white text-left pl-4">new milestone</div>
  <div class="flex flex-row text-mywood-900 justify-start">
    <div class="flex flex-col text-left work-milestone-form w-7/12">
      <div><label for="name">name</label></div>
      <div><input id="name" bind:value={new_name} type="text" style="width: 100%; font-size: 9pt; height: 20px;"/></div>

      <div><label for="description">description</label></div>
      <div><textarea id="description" bind:value={new_description} style="width: 100%; height: 100px; font-size: 9pt;"></textarea></div>

      <div class="flex flex-col">
        <div><label for="agreement_id">client (total {count_clients})</label></div>
      </div>
      <div>
        <div class="flex flex-col">
          {#if client_mode === 'new'}
            <div></div>
            <NewClient createdClient={createdClient}></NewClient>
          {/if}
          {#if count_clients === 1 || client}
            <div class="flex flex-row">
              <div class="mr-2">{client? client.id : ''}</div>
              <div class="mr-2">{client? client.name : ''}</div>
            </div>
          {/if}
          {#if client_mode === 'search'}
            <div id="client_id" class="flex flex-col client-search">
              <SearchClient foundClients={foundClients}></SearchClient>
            </div>
          {/if}
          {#if (clients && clients.length < 10) || (client_mode === 'search' && (clients && clients.length > 0))}
            <div class="flex flex-col">
              {#if clients && clients.length > 0 && client_mode === 'search'}
                <div>select client:</div>
                <ClientList clients={clients} selectClient={selectClient}></ClientList>
              {/if}
            </div>
          {/if}
          <div class="flex flex-row">
            {#if (!count_clients || count_clients < 10 ) && client_mode !== 'new'}
              <div on:click={() => setClientMode('new')}
                   class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
                   style="width: 150px;"
              >
                new client
              </div>
            {/if}
            {#if client_mode !== 'search'}
              <div on:click={() => setClientMode('search')}
                   class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
                   style="width: 150px; margin-left: 5px;"
              >
                search clients
              </div>
            {/if}
          </div>
        </div>
      </div>

      <div class="flex flex-col">
        <div><label for="agreement_id">project (total {count_projects})</label></div>
      </div>
      <div>
        <div class="flex flex-col">
          {#if project_mode === 'new'}
            <div></div>
            <NewProject client={client} createdProject={createdProject}></NewProject>
          {/if}
          {#if count_projects === 1 || project}
            <div class="flex flex-row">
              <div class="mr-2">{project? project.id : ''}</div>
              <div class="mr-2">{project? project.name : ''}</div>
            </div>
          {/if}
          {#if project_mode === 'search'}
            <div id="project_id" class="flex flex-col project-search">
              <SearchProject foundProjects={foundProjects}></SearchProject>
            </div>
          {/if}
          {#if (projects && projects.length < 10) || (project_mode === 'search' && (projects && projects.length > 0))}
            <div class="flex flex-col">
              {#if projects && projects.length > 0 && project_mode === 'search'}
                <div>select project:</div>
<!--                <ProjectList projects={projects} selectProject={selectProject}></ProjectList>-->
              {/if}
            </div>
          {/if}
          <div class="flex flex-row">
            {#if (!count_projects || count_projects < 10 ) && project_mode !== 'new'}
              <div on:click={() => setProjectMode('new')}
                   class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
                   style="width: 150px;"
              >
                new project
              </div>
            {/if}
            {#if project_mode !== 'search'}
              <div on:click={() => setProjectMode('search')}
                   class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
                   style="width: 150px; margin-left: 5px;"
              >
                search projects
              </div>
            {/if}
          </div>
        </div>
      </div>

    </div>
  </div>
  {#if new_name && new_name.trim().length > 0 && new_description && new_description.trim().length > 0 }
    <div on:click={createWorkMilestone}
         class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
         style="width: 150px;"
    >
      create
    </div>
  {/if}
</div>
<style>
  .new-project {
    width: calc(100% - 5px);
    height: 80lvh;
    margin: 3px;
    display: flex;
    flex-direction: column;
  }
  .project-form {
    display: grid;
    grid-template-columns: 1fr 3fr;
  }
  .project-form > * {
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
  import SearchAgreement from './search-agreement.svelte';
  import type {Client} from "../models/client";
  import type {Agreement} from "../models/agreement";
  import AgreementService from "../services/agreement.service";
  import NewAgreement from './new_agreement.svelte';
  import AgreementList from './agreement_list.svelte';
  import ProjectService from "../services/project.service";
  import {crud, MessageStore, ProjectStore} from "../stores";
  import type {Project} from "../models/project";
  import NewClient from './new_client.svelte';
  import ClientService from "../services/client.service";
  import SearchClient from './search-client.svelte';
  import ClientList from './client_list.svelte';

  export let createdProject = (created: Project) => {
    console.log(`created project: ${JSON.stringify(created)}`);
  }

  let new_description = '';
  $: new_description

  let new_name = '';
  $: new_name

  export let client: Client | null;
  $: client

  let clients: Client[];
  $: clients

  let agreements: Agreement[];
  $: agreements

  let agreement: Agreement;
  $: agreement

  const foundClients = (next: Client[]): void => {
    clients = next;
  }

  const foundAgreements = (next: Agreement[]): void => {
    agreements = next;
  }
  const countClientAgreements = async () => {
    AgreementService.count({
      client: client.id
    }).then((response: any) => {
      count_agreements = response.data;
      if (count_agreements < 10) {
        AgreementService.find({client: client.id}).then((response: any) => {
          agreements = response.data;
          agreement = agreements[0];
        });

      }
    });
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

  const findAllClients = (): void => {
    ClientService.find({}).then((response: any) => {
      clients = response.data;
      if (clients.length === 1) {
        client = clients[0];
      }
    });
  }

  let count_clients = 0;
  $: count_clients
  countClients();


  let count_agreements = 0;
  $: count_agreements
  if (client) {
    countClientAgreements();
  }

  let client_mode = ''
  $: client_mode

  let agreement_mode = ''
  $: agreement_mode

  const createdClient = (next: Client): void => {
    if (!clients) {
      clients = [];
    }
    clients.push(next);
    client = next;
    client_mode = 'search';
    // countClientClients();
  }

  const createdAgreement = (next: Agreement): void => {
    if (!agreements) {
      agreements = [];
    }
    agreements.push(next);
    agreement = next;
    agreement_mode = 'search';
    countClientAgreements();
  }

  const setClientMode = (next: string): void => {
    client_mode = next;
    if (client_mode === 'search') {
      findAllClients();
    } else if (client_mode === 'new') {
      client = null;
    }
  }

  const setAgreementMode = (next: string): void => {
    agreement_mode = next;
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

  const selectAgreement = (next: Agreement): void => {
    agreement = next;
    agreements = [];
    agreement_mode = '';
  }

  const createProject = (): void => {
    if (client) {
      ProjectService.create({
          name: new_name,
          description: new_description,
          client: client.id,
          agreement: agreement.id
      }).then((response: any) => {
        const created = response.data;
        ProjectStore.set({
          type: crud.CREATE,
          payload: created
        });
        createdProject(created);
      });
    }
  }
</script>
<div class="new-project rounded-xl">
  <div class="w-full bg-myroon-100 text-myhigh_white text-left pl-4">new project</div>
  <div class="flex flex-row text-mywood-900 justify-start">
    <div class="flex flex-col text-left project-form w-7/12">
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
        <div><label for="agreement_id">agreement (total {count_agreements})</label></div>
      </div>
      <div>
        <div class="flex flex-col">
          {#if agreement_mode === 'new' && client}
            <div></div>
            <NewAgreement client={client} createdAgreement={createdAgreement}></NewAgreement>
          {/if}
          {#if count_agreements === 1 || agreement}
            <div class="flex flex-row">
              <div class="mr-2">{agreement?.id}</div>
              <div class="mr-2">{agreement?.name}</div>
              <div class="mr-2">{agreement?.created? `${agreement.created}` : ''}</div>
            </div>
          {/if}
          {#if agreement_mode === 'search'}
            <div id="agreement_id" class="flex flex-col agreement-search">
              <SearchAgreement client={client} foundAgreements={foundAgreements}></SearchAgreement>
            </div>
          {/if}
          {#if (agreements && agreements.length < 10) || (agreement_mode === 'search' && (agreements && agreements.length > 0))}
            <div class="flex flex-col">
              {#if agreements && agreements.length > 0}
                <div>select agreement:</div>
                <AgreementList agreements={agreements} selectAgreement={selectAgreement}></AgreementList>
              {/if}
            </div>
          {/if}
          <div class="flex flex-row" style="margin-right: 5px;">
            {#if agreement_mode !== 'new'}
              <div on:click={() => setAgreementMode('new')}
                   class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
                   style="width: 150px;"
              >
                new agreement
              </div>
            {/if}
            {#if agreement_mode !== 'search'}
              <div on:click={() => setAgreementMode('search')}
                   class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
                   style="width: 150px; margin-left: 5px;"
              >
                search agreements
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
  {#if new_name && new_name.trim().length > 0 && new_description && new_description.trim().length > 0 && agreement}
    <div on:click={createProject}
         class="rounded-md mb-3 mt-3 bg-mywood-100 text-center text-myhigh_white hover:bg-myblue-100 hover:text-myhigh_white cursor-pointer"
         style="width: 150px;"
    >
      create
    </div>
  {/if}
</div>
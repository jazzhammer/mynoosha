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
  import type {Client} from "../models/client";
  import type {Agreement} from "../models/agreement";
  import AgreementService from "../services/agreement.service";
  import ProjectTypeService from "../services/project.service";
  import {crud, MessageStore, ProjectTypeStore} from "../stores";
  import type {ProjectType} from "../models/project_type";
  import ClientService from "../services/client.service";

  export let createdProjectType = (created: ProjectType) => {
    console.log(`created project type: ${JSON.stringify(created)}`);
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

  const createProjectType = (): void => {
    if (client) {
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
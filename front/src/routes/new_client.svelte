<style>
  .client-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 180px;
  }

  .client-form-fields > * {
    margin-bottom: 2px;
  }

  .field-label {
    text-align: left;
    width: 110px;
  }

  .client-form-header {
    width: 262px;
  }
</style>
<script lang="ts">
  import ClientService from '../services/client.service';
  import {ClientStore, crud} from "../stores";
  import type {Client} from "../models/client";

  let canCreate = false;
  $: canCreate

  let name = '';
  $: name

  let address_street = '';
  $: address_street

  let address_city = '';
  $: address_city

  let address_province_state = '';
  $: address_province_state

  let address_postal_zip_code = '';
  $: address_postal_zip_code

  export let createdClient =  (created: Client) => {
    console.log(`createdClient: ${JSON.stringify(created)}`);
  }

  function createClient(): void {
    ClientService.create({
      name,
      address_street,
      address_city,
      address_province_state,
      address_postal_zip_code,
    }).then((response: any) => {
      const created = response.data;
      ClientStore.set({
        type: crud.CREATE,
        payload: created
      });
      createdClient(created);
    })
  }
  function keyupName(event: any) {
    canCreate = name.trim().length > 0;

    if (event.key === 'Enter' && canCreate) {
      createClient();
    }
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded text-myhigh_white"
     style="min-width: 226px; max-width: 288px; font-size: 10pt;"
     data-testid="new_client"
>
  <div class="client-form-header bg-mywood-900 rounded mb-5 text-center"
       data-testid="new_client_header"
       id="new_client_header">
    new client
  </div>
  <div class="client-form-fields w-3/12 text-mywood-900" data-testid="new_client_form">
    <label class="field-label" data-testid="new_client_name">name
      <input type="text"
             bind:value={name}
             on:keyup={keyupName}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             id="new_client_name"
             data-testid="new_client_name_input"/>
    </label>
    <label class="field-label" data-testid="new_client_name">street
      <input type="text"
             bind:value={address_street}
             on:keyup={() => {}}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             id="new_client_street_input"
             data-testid="new_client_street_input"
      />
    </label>
    <label class="field-label" data-testid="new_client_name">city
      <input type="text"
             bind:value={address_city}
             on:keyup={() => {}}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             data-testid="new_client_city_input"/>
    </label>
    <label class="field-label" data-testid="new_client_name">province/state
      <input type="text"
             bind:value={address_province_state}
             on:keyup={() => {}}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             data-testid="new_client_province_state_input"/>
    </label>
    <label class="field-label" data-testid="new_client_name">zip/postal
      <input type="text"
             bind:value={address_postal_zip_code}
             on:keyup={() => {}}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             data-testid="new_client_postal_zip_code_input"/>
    </label>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow h-5 text-mywood-900">
    {#if canCreate}
    <button on:click={createClient}
            type="button"
            value="create"
            class="bg-myroon-100mt-3 rounded hover:border"
            style="margin: auto; min-width: 80px; background-color: #d78058"
            data-testid="create_client_button"
    >
      create
    </button>
    {/if}
  </div>
</div>

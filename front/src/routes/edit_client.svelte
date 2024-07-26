<style>
  .client-form-fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    width: 200px;
  }
  .client-form-fields > * {
    margin-bottom: 2px;
  }
  .client-form-header {
    width: 265px;
  }
  .field-label {
    text-align: left;
  }
  .field-input {
    text-align: left;
    width: 200px;
    margin-left: 3px;
  }
</style>
<script lang="ts">
  import ClientService from '../services/client.service';
  import {type ClientCrud, ClientStore, crud} from "../stores";
  import type {Client} from "../models/client";
  import {onDestroy} from "svelte";

  let name ='';
  $: name
  let address_street ='';
  $: address_street
  let address_city ='';
  $: address_city
  let address_province_state ='';
  $: address_province_state
  let address_postal_zip_code ='';
  $: address_postal_zip_code

  let client: Client;
  $: client

  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      client = ccrud.payload as Client
      name = client.name as string;
      address_street = client.address_street as string;
      address_city = client.address_city as string;
      address_province_state = client.address_province_state as string;
      address_postal_zip_code = client.address_postal_zip_code as string;
    }
  });
  onDestroy(unsubClient);

  function updateClient(): void {
    ClientService.update({
      id: client.id,
      name,
      address_street,
      address_city,
      address_province_state,
      address_postal_zip_code
    }).then((response: any) => {
      const updated = response.data;
      client = updated;
      ClientStore.set({
        type: crud.UPDATE,
        payload: updated
      });
    })
  }

  function keyupName(event: any) {
    if (event.key === 'Enter') {
      updateClient();
    }
    console.log(name)
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="new_client">
  <div class="client-form-header bg-mywood-900 rounded mb-5" data-testid="new_client_header" id="new_client_header">edit client</div>
  <div class="client-form-fields w-3/12 text-mywood-900" data-testid="new_client_form">
    <label class="field-label" data-testid="new_client_name">name</label>
    <input type="text"
           bind:value={name}
           on:keyup={keyupName}
           class="field-input"
           style="width: 173px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
           data-testid="new_client_name_input"/>
    <label class="field-label" data-testid="new_client_name">street</label>
    <input type="text"
           bind:value={address_street}
           on:keyup={() => {}}
           class="field-input"
           style="width: 173px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
           data-testid="new_client_street_input"/>
    <label class="field-label" data-testid="new_client_name">city</label>
    <input type="text"
           bind:value={address_city}
           on:keyup={() => {}}
           class="field-input"
           style="width: 173px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
           data-testid="new_client_city_input"/>
    <label class="field-label" data-testid="new_client_name">province/state</label>
    <input type="text"
           bind:value={address_province_state}
           on:keyup={() => {}}
           class="field-input"
           style="width: 173px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
           data-testid="new_client_province_state_input"/>
    <label class="field-label" data-testid="new_client_name">zip/postal</label>
    <input type="text"
           bind:value={address_postal_zip_code}
           on:keyup={() => {}}
           class="field-input"
           style="width: 173px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
           data-testid="new_client_postal_zip_code_input"/>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow">
    <button on:click={updateClient}
            type="button"
            value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
            style="margin: auto;"
            data-testid="create_client_button"
    >
      update
    </button>
  </div>
</div>

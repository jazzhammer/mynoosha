<style>
  .billable_type-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 200px;
  }
  .billable_type-form-fields > * {
    margin-bottom: 2px;
  }
  .billable_type-form-header {
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
  import BillableTypeService from '../services/billable_type.service';
  import {type BillableTypeCrud, BillableTypeStore, crud} from "../stores";
  import type {BillableType} from "../models/billable_type";
  import {onDestroy} from "svelte";
  // ------------------------------------------------------------
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
  // ------------------------------------------------------------
  let billable_type: BillableType;
  $: billable_type
  const unsubBillableType = BillableTypeStore.subscribe((ccrud: BillableTypeCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      billable_type = ccrud.payload as BillableType
      name = billable_type.name as string;
    }
  });
  onDestroy(unsubBillableType);

  function updateBillableType(): void {
    BillableTypeService.update({
      id: billable_type.id,
      name
    }).then((response: any) => {
      const updated = response.data;
      billable_type = updated;
      BillableTypeStore.set({
        type: crud.UPDATE,
        payload: updated
      });
    })
  }

  function keyupName(event: any) {
    if (event.key === 'Enter') {
      updateBillableType();
    }
    console.log(name)
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="new_billable_type">
  <div class="billable_type-form-header bg-mywood-900 rounded mb-5" data-testid="new_billable_type_header" id="new_billable_type_header">edit billable_type</div>
  <div class="billable_type-form-fields w-3/12 text-mywood-900" data-testid="new_billable_type_form">
    <label class="field-label" data-testid="new_billable_type_name">name
    <input type="text"
           bind:value={name}
           on:keyup={keyupName}
           class="field-input"
           style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
           id="new_billable_type_name"
           data-testid="new_billable_type_name_input"/>
    </label>
    <div class="mt-6 text-myhigh_white hover:drop-shadow">
      <button on:click={updateBillableType}
              type="button"
              value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
              style="margin: auto;"
              data-testid="create_billable_type_button"
      >
        update
      </button>
    </div>
  </div>
</div>

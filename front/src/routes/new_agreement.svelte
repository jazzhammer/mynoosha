<style>
  .agreement-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 180px;
  }

  .agreement-form-fields > * {
    margin-bottom: 2px;
  }

  .field-label {
    text-align: left;
    width: 110px;
  }

  .agreement-form-header {
    width: 262px;
  }
</style>
<script lang="ts">
  import AgreementService from '../services/agreement.service';
  import {AgreementStore, crud} from "../stores";

  let name ='';
  $: name

  function createAgreement(): void {
    AgreementService.create({
      name
    }).then((response: any) => {
      const created = response.data;
      AgreementStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }
  function keyupName(event: any) {
    if (event.key === 'Enter') {
      createAgreement();
    }
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-4/12 text-myhigh_white"
     style="min-width: 226px; max-width: 300px; font-size: 10pt;" data-testid="new_agreement"
>
  <div class="agreement-form-header bg-mywood-900 rounded mb-5" data-testid="new_agreement_header" id="new_agreement_header">new agreement</div>
  <div class="agreement-form-fields w-3/12 text-mywood-900" data-testid="new_agreement_form">
    <label class="field-label" data-testid="new_agreement_name">name
      <input type="text"
             bind:value={name}
             on:keyup={keyupName}
             class="field-input"
             style="width: 260px; height: 24px; font-size: 10pt; padding-left: 2px; padding-right: 2px;"
             id="new_agreement_name"
             data-testid="new_agreement_name_input"/>
    </label>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow">
    <button on:click={createAgreement}
            type="button"
            value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
            style="margin: auto;"
            data-testid="create_agreement_button"
    >
      create
    </button>
  </div>
</div>

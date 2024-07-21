<style>
  .client-form-fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    width: 200px;
  }
  .client-form-header {
    width: 200px;
  }
</style>
<script lang="ts">
  import ClientService from '../services/client.service';
  import {ClientStore, crud} from "../stores";

  let name ='';
  $: name
  function createClient(): void {
    ClientService.createClient({
      name
    }).then((response: any) => {
      const created = response.data;
      ClientStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }
  function keyupName(event: any) {
    if (event.key === 'Enter') {
      createClient();
    }
    console.log(name)
  }
</script>
<div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded w-2/12 text-myhigh_white" style="min-width: 226px;">
  <div class="client-form-header mb-2 bg-myroon-100">new client</div>
  <div class="client-form-fields w-2/12 text-mywood-900">
    <label>name</label>
    <input type="text" style="width: 80px;" bind:value={name} on:keyup={keyupName}/>
  </div>
  <div class="mt-6 text-myhigh_white hover:drop-shadow">
    <button type="button" on:click={createClient} value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border" style="margin: auto;">create</button>
  </div>
</div>

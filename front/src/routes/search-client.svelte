<style>

  .search-text {
    font-size: 9pt;
    height: 18px;
  }

</style>
<script lang="ts">
  import {type Client} from '../models/client';
  import ClientService from "../services/client.service";
  let searchTerm = '';
  $: searchTerm

  export let foundClients = (clients: Client[]): void => {
    console.log(`found clients:${clients ? clients.length: 'none'}`);
  }


  let timeoutSearchClient: any;
  const searchClient = (): void => {
    if (timeoutSearchClient) {
      clearTimeout(timeoutSearchClient);
    }
    if (searchTerm && searchTerm.length > 0) {
      timeoutSearchClient = setTimeout(() => {
        ClientService.find({search: searchTerm}).then((response: any) => {
          const clients = response.data;
          foundClients(clients);
        })
      }, 300);
    }
  }
</script>
<div>
  <input bind:value={searchTerm} on:keyup={searchClient}
         on:focus={(e) => e?.target?.select()}
         type="text" placeholder="search client"
         class="search-text"
  >
</div>
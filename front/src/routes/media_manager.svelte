<style>
  .media-manager {
    width: 100%;
    color: black;
  }

  .upload-button {
    border: 1px solid #b42f4c;
    width: 80px;
    border-radius: 2px;
    cursor: pointer;
    color: #3b1000;
  }
  .upload-button:hover {
    background-color: #e3cd9a;
    border: 2px solid #b42f4c;
  }
</style>
<script lang="ts">
  import MediumService from "../services/medium.service";
  import {crud, MediumStore} from "../stores";

  let files: FileList;
  $: files

  let b64: any;
  $: b64

  let latestImage: Image;
  $: latestImage

  function uploadFile(next: any): void {
    const file = files[0];
    debugger;
    MediumService.create({
      file: file
    }).then((response: any) => {
      const created = response.data
      const b64source = created.base64;
      b64 = `data:image/png;base64,${b64source}`
      latestImage = new Image();
      latestImage.src = b64;
      latestImage.width = created.width;
      latestImage.height = created.height;
      debugger;
      MediumStore.set({
        type: crud.CREATE,
        payload: created
      })
    });
  }

</script>
<div class="media-manager">
  <div class="flex flex-col border-myroon-100 border p-3 ml-3 rounded text-myhigh_white text-myblue-900"
       style="min-width: 226px; width: calc(100% - 23px); height: 90lvh; font-size: 10pt;"
       data-testid="media-manager"
  >
    <div class="billable_type-form-header bg-mywood-900 rounded mb-5 text-myhigh_white"
         data-testid="media-manager_header" id="media-manager_header"
    >media manager</div>

    <label for="avatar" class="upload-button">
      upload file
    </label>
    <input accept="image/png, image/jpeg"
           bind:files
           id="avatar"
           name="avatar"
           type="file"
           style="display: none"
           on:change={uploadFile}
    />
<!--    <input bind:files id="many" multiple type="file" />-->

    {#if files}
      <h2>Selected files:</h2>
      {#each Array.from(files) as file}
        <p>{file.name} ({file.size} bytes)</p>
      {/each}
    {/if}

    <img style='' id='base64image' width={latestImage?.width/2} height={latestImage?.height/2} src={b64} />
  </div>
</div>
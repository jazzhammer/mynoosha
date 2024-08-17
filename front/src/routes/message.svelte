<style>
  .message {
    font-style: italic;
    padding-left: 10px;
    width: 100%;
    display: flex;
    flex-direction: row;
    height: 100%;
    color: black;
  }

</style>
<script lang="ts">
  import {MessageStore} from "../stores";
  import {onDestroy} from "svelte";

  let message = '';
  $: message
  let unsubMessage = MessageStore.subscribe((me: any) => {
    if (me) {
      message = me.message;
      setTimeout(() => {
        message = '';
      }, 3000);
    }
  });
  onDestroy(unsubMessage);
</script>
<div class="message">{message}</div>
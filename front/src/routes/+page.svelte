<script lang="ts">
  import Home from './home.svelte';
  let mode = 'splash';

  function go(next: string) {
    console.log(`next ${next}`)
    mode = next;
  }
</script>
<div class="p-1 h-full flex flex-col text-center" style="font-size: 10pt;">
  {#if mode === 'home'}
    <Home></Home>
  {/if}
  {#if mode === 'splash'}
    <img  src="logo_mynoosha_l.jpg" alt="main logo" class="rounded-xl"
          style="height: 40%; width: 40%; margin: auto; margin-top: 100px; z-index: 100"
          data-testid="splash-logo"
    >
    <section style="z-index: 200; position: relative">
      <div role="button" class="" style="position: absolute; top: -120px; width: 100%; text-align: center" >
        <button on:click={() => go('home')}
                on:keyup={() => {}}
                class="bg-mymid_white p-2 w-2/12 rounded-xl drop-shadow-2xl shadow-mywood-900 cursor-pointer hover:border-2"
                style="margin: auto;"
                role="button"
                tabindex="0"
                data-testid="start-button"
        >
          start posting time
        </button>
      </div>
    </section>
  {/if}
</div>
<script lang="ts">
  import { showSidebar, user } from '$lib/stores';
  import Gallery from '$lib/components/gallery/Gallery.svelte';
  import MenuLines from '$lib/components/icons/MenuLines.svelte';
  import UserMenu from '$lib/components/layout/Sidebar/UserMenu.svelte';
  import { getContext } from 'svelte';
  const i18n = getContext('i18n');
</script>

<div class="flex flex-col w-full h-screen max-h-[100dvh] transition-width duration-200 ease-in-out {$showSidebar ? 'md:max-w-[calc(100%-260px)]' : ''} max-w-full">
  <nav class="px-2 pt-1 backdrop-blur-xl w-full drag-region">
    <div class="flex items-center">
      <div class="{$showSidebar ? 'md:hidden' : ''} flex flex-none items-center">
        <button id="sidebar-toggle-button" class="cursor-pointer p-1.5 flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-850 transition" on:click={() => { showSidebar.set(!$showSidebar); }} aria-label="Toggle Sidebar">
          <div class="m-auto self-center"><MenuLines /></div>
        </button>
      </div>
      <div class="ml-2 py-0.5 self-center flex items-center justify-between w-full">
        <div class="">
          <div class="flex gap-1 scrollbar-none overflow-x-auto w-fit text-center text-sm font-medium bg-transparent py-1 touch-auto pointer-events-auto">
            <a class="min-w-fit transition" href="/gallery">{$i18n.t('Gallery')}</a>
          </div>
        </div>
        <div class="self-center flex items-center gap-1">
          {#if $user !== undefined && $user !== null}
            <UserMenu className="max-w-[240px]" role={$user?.role} help={true} />
          {/if}
        </div>
      </div>
    </div>
  </nav>
  <div class="pb-1 flex-1 max-h-full overflow-y-auto @container">
    <Gallery />
  </div>
</div>

<script lang="ts">
  import { onMount, getContext } from 'svelte';
  import { WEBUI_NAME, showSidebar, config, user } from '$lib/stores';
  import { goto } from '$app/navigation';

  const i18n = getContext('i18n');
  let loaded = false;
  onMount(async () => {
    if (!($config?.features?.enable_gallery ?? false) || !['admin','user'].includes($user?.role)) {
      goto('/');
      return;
    }
    loaded = true;
  });
</script>

<svelte:head>
  <title>{$i18n.t('Gallery')} • {$WEBUI_NAME}</title>
</svelte:head>

{#if loaded}
  <slot />
{/if}

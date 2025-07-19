<script lang="ts">
import { onMount, getContext } from 'svelte';
import { getFiles } from '$lib/apis/files';
import { user } from '$lib/stores';

let images: any[] = [];
const i18n = getContext('i18n');

onMount(async () => {
    const token = $user?.token ?? '';
    try {
        const files = await getFiles(token);
        images = files.filter((f: any) => f.meta?.content_type?.startsWith('image/'));
    } catch (e) {
        console.error('failed to load gallery', e);
    }
});
</script>

<div class="p-4 grid grid-cols-2 md:grid-cols-3 gap-2">
    {#each images as img}
        <img class="w-full rounded" src={`/api/files/${img.id}/content`} alt={img.filename} />
    {/each}
</div>

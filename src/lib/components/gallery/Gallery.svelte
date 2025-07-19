<script lang="ts">
import { onMount, getContext } from 'svelte';
import { getFiles } from '$lib/apis/files';
import { WEBUI_API_BASE_URL } from '$lib/constants';
import { user } from '$lib/stores';
import Image from '$lib/components/common/Image.svelte';
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

<div class="p-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
    {#each images as img}
        <div class="bg-gray-50 dark:bg-gray-850 rounded-xl p-2 flex justify-center">
            <Image
                className="w-40 h-40"
                imageClassName="object-cover w-full h-full rounded-lg"
                src={`${WEBUI_API_BASE_URL}/files/${img.id}/content`}
                alt={img.filename}
            />
        </div>
    {/each}
</div>
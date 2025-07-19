<script lang="ts">
import { onMount, getContext } from 'svelte';
import { getFiles } from '$lib/apis/files';
import { generateImageCaption } from '$lib/apis';
import { WEBUI_API_BASE_URL } from '$lib/constants';
import { user, models, settings } from '$lib/stores';
import Image from '$lib/components/common/Image.svelte';
import Spinner from '$lib/components/common/Spinner.svelte';
import { toast } from 'svelte-sonner';
let images: any[] = [];
let captions: Record<string, any> = {};
let selectedModels: Record<string, string> = {};
let loading: Record<string, boolean> = {};
const i18n = getContext('i18n');
onMount(async () => {
    const token = $user?.token ?? '';
    try {
        const files = await getFiles(token);
        images = files.filter((f: any) => f.meta?.content_type?.startsWith('image/'));
        images.forEach((img) => {
            if (img.meta?.caption || img.meta?.description) {
                captions[img.id] = { caption: img.meta.caption, description: img.meta.description };
            }
            selectedModels[img.id] = $settings?.imageCaptionModel ?? $models.find((m) => m.owned_by === 'ollama')?.id;
        });
    } catch (e) {
        console.error('failed to load gallery', e);
    }
});

const captionImage = async (id: string) => {
    const token = $user?.token ?? '';
    const modelId = selectedModels[id] ?? $models.find((m) => m.owned_by === 'ollama')?.id;
    if (!modelId) {
        toast.error($i18n.t('No model available'));
        return;
    }
    loading[id] = true;
    const res = await generateImageCaption(token, modelId, id).catch((err) => {
        toast.error(`${err}`);
        return null;
    });
    if (res) {
        captions[id] = res;
        const img = images.find((f) => f.id === id);
        if (img) {
            img.meta = { ...img.meta, ...res };
        }
    }
    loading[id] = false;
};
</script>

<div class="p-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
    {#each images as img}
        <div class="bg-gray-50 dark:bg-gray-850 rounded-xl p-2 flex flex-col items-center space-y-2">
            <Image
                className="w-40 h-40"
                imageClassName="object-cover w-full h-full rounded-lg"
                src={`${WEBUI_API_BASE_URL}/files/${img.id}/content`}
                alt={img.filename}
            />
            <select class="text-sm rounded" bind:value={selectedModels[img.id]}>
                {#each $models.filter(m => m.owned_by === 'ollama') as m}
                    <option value={m.id}>{m.name}</option>
                {/each}
            </select>
            <button
                class="px-3 py-1 bg-emerald-700 hover:bg-emerald-800 text-gray-100 text-sm rounded"
                on:click={() => captionImage(img.id)}
                disabled={loading[img.id]}
            >
                {#if loading[img.id]}
                    <Spinner className="size-4" />
                {:else}
                    {$i18n.t('Generate')}
                {/if}
            </button>
            {#if captions[img.id]}
                <div class="text-xs text-center space-y-1">
                    <div><strong>{$i18n.t('Description')}:</strong> {captions[img.id].description}</div>
                    <div><em>{$i18n.t('Caption')}:</em> {captions[img.id].caption}</div>
                </div>
            {/if}
        </div>
    {/each}
</div>
<script lang="ts">
	import { createEventDispatcher, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';

import { updateMemoryById, updateMemoryTags } from '$lib/apis/memories';
import Tags from '$lib/components/common/Tags.svelte';

	import Spinner from '$lib/components/common/Spinner.svelte';
	import Modal from '$lib/components/common/Modal.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';

	const dispatch = createEventDispatcher();

	export let show;
	export let memory = {};

	const i18n = getContext('i18n');

let loading = false;
let content = '';
let tagsList: { name: string }[] = [];

	$: if (show) {
		setContent();
	}

        const setContent = () => {
                content = memory.content;
                tagsList = memory?.meta?.tags?.map((t) => ({ name: t })) ?? [];
        };

	const submitHandler = async () => {
		loading = true;

                const res = await updateMemoryById(localStorage.token, memory.id, content).catch((error) => {
                        toast.error(`${error}`);

                        return null;
                });

                if (res) {
                        await updateMemoryTags(localStorage.token, memory.id, tagsList.map(t => t.name)).catch(() => {});
                        console.log(res);
                        toast.success($i18n.t('Memory updated successfully'));
                        dispatch('save');
                        show = false;
                        tagsList = [];
                }

		loading = false;
	};
</script>

<Modal bind:show size="sm">
	<div>
		<div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-2">
			<div class=" text-lg font-medium self-center">
				{$i18n.t('Edit Memory')}
			</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<XMark className={'size-5'} />
			</button>
		</div>

		<div class="flex flex-col md:flex-row w-full px-5 pb-4 md:space-x-4 dark:text-gray-200">
			<div class=" flex flex-col w-full sm:flex-row sm:justify-center sm:space-x-6">
				<form
					class="flex flex-col w-full"
					on:submit|preventDefault={() => {
						submitHandler();
					}}
				>
					<div class="">
						<textarea
							bind:value={content}
							class=" bg-transparent w-full text-sm rounded-xl p-3 outline outline-1 outline-gray-100 dark:outline-gray-800"
							rows="6"
							style="resize: vertical;"
							placeholder={$i18n.t('Enter a detail about yourself for your LLMs to recall')}
						/>

                                                <div class="text-xs text-gray-500">
                                                        ⓘ {$i18n.t('Refer to yourself as "User" (e.g., "User is learning Spanish")')}
                                                </div>
                                        </div>

                                        <div class="mt-2">
                                                <Tags
                                                        tags={tagsList}
                                                        on:add={(e) => {
                                                                tagsList = [...tagsList, { name: e.detail }];
                                                        }}
                                                        on:delete={(e) => {
                                                                tagsList = tagsList.filter((t) => t.name !== e.detail);
                                                        }}
                                                />
                                        </div>

					<div class="flex justify-end pt-1 text-sm font-medium">
						<button
							class=" px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-3xl flex flex-row space-x-1 items-center {loading
								? ' cursor-not-allowed'
								: ''}"
							type="submit"
							disabled={loading}
						>
							{$i18n.t('Update')}

							{#if loading}
								<div class="ml-2 self-center">
									<Spinner />
								</div>
							{/if}
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</Modal>

<script lang="ts">
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import ChevronUp from '$lib/components/icons/ChevronUp.svelte';
	import Search from '$lib/components/icons/Search.svelte';
        import Collapsible from '$lib/components/common/Collapsible.svelte';
        import Image from '$lib/components/common/Image.svelte';

       export let status = { urls: [], images: [], snippets: [], query: '' };
	let state = false;
</script>

<Collapsible bind:open={state} className="w-full space-y-1">
	<div
		class="flex items-center gap-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition"
	>
		<slot />

		{#if state}
			<ChevronUp strokeWidth="3.5" className="size-3.5 " />
		{:else}
			<ChevronDown strokeWidth="3.5" className="size-3.5 " />
		{/if}
	</div>
	<div
		class="text-sm border border-gray-300/30 dark:border-gray-700/50 rounded-xl mb-1.5"
		slot="content"
	>
		{#if status?.query}
			<a
				href="https://www.google.com/search?q={status.query}"
				target="_blank"
				class="flex w-full items-center p-3 px-4 border-b border-gray-300/30 dark:border-gray-700/50 group/item justify-between font-normal text-gray-800 dark:text-gray-300 no-underline"
			>
				<div class="flex gap-2 items-center">
					<Search />

					<div class=" line-clamp-1">
						{status.query}
					</div>
				</div>

				<div
					class=" ml-1 text-white dark:text-gray-900 group-hover/item:text-gray-600 dark:group-hover/item:text-white transition"
				>
					<!--  -->
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 16 16"
						fill="currentColor"
						class="size-4"
					>
						<path
							fill-rule="evenodd"
							d="M4.22 11.78a.75.75 0 0 1 0-1.06L9.44 5.5H5.75a.75.75 0 0 1 0-1.5h5.5a.75.75 0 0 1 .75.75v5.5a.75.75 0 0 1-1.5 0V6.56l-5.22 5.22a.75.75 0 0 1-1.06 0Z"
							clip-rule="evenodd"
						/>
					</svg>
				</div>
			</a>
		{/if}

               {#each status.urls as url, urlIdx}
                       <div class="border-b border-gray-300/30 dark:border-gray-700/50 last:border-b-0">
                               <a
                                       href={url}
                                       target="_blank"
                                       class="flex w-full items-center p-3 px-4 group/item justify-between font-normal text-gray-800 dark:text-gray-300"
                               >
                                       <div class=" line-clamp-1">
                                               {url}
                                       </div>

                                       <div
                                               class=" ml-1 text-white dark:text-gray-900 group-hover/item:text-gray-600 dark:group-hover/item:text-white transition"
                                       >
                                               <svg
                                                       xmlns="http://www.w3.org/2000/svg"
                                                       viewBox="0 0 16 16"
                                                       fill="currentColor"
                                                       class="size-4"
                                               >
                                                       <path
                                                               fill-rule="evenodd"
                                                               d="M4.22 11.78a.75.75 0 0 1 0-1.06L9.44 5.5H5.75a.75.75 0 0 1 0-1.5h5.5a.75.75 0 0 1 .75.75v5.5a.75.75 0 0 1-1.5 0V6.56l-5.22 5.22a.75.75 0 0 1-1.06 0Z"
                                                               clip-rule="evenodd"
                                                       />
                                               </svg>
                                       </div>
                               </a>
                               {#if status.snippets && status.snippets[urlIdx]}
                                       <div class="px-4 pb-3 text-gray-600 dark:text-gray-400 text-wrap">
                                               {status.snippets[urlIdx]}
                                       </div>
                               {/if}
                       </div>
               {/each}
                {#if status.images && status.images.length > 0}
                        <div class="flex overflow-x-auto gap-2 p-3 px-4 border-t border-gray-300/30 dark:border-gray-700/50">
                                {#each status.images as img}
                                        <Image src={img} alt={status.query} className="w-28 h-28" imageClassName="rounded-lg object-cover w-full h-full" />
                                {/each}
                        </div>
                {/if}
        </div>
</Collapsible>

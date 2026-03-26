<script lang="ts">
    import { onMount } from "svelte";

    interface Dog {
        id: number;
        name: string;
        breed: string;
    }

    export let dogs: Dog[] = [];
    let loading = true;
    let error: string | null = null;

    const fetchDogs = async () => {
        loading = true;
        try {
            const response = await fetch('/api/dogs');
            if(response.ok) {
                dogs = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    onMount(() => {
        fetchDogs();
    });
</script>

<div>
    <h2 class="text-2xl font-semibold mb-6 text-gray-900 dark:text-gray-100 disco:text-cyan-300">Available Dogs</h2>
    
    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each Array(6) as _, i}
                <div class="bg-white dark:bg-[#161b22] disco:bg-gradient-to-br disco:from-pink-500 disco:to-purple-600 rounded-lg overflow-hidden border border-gray-300 dark:border-gray-700 disco:border-yellow-400 disco:shadow-2xl disco:shadow-pink-500/50">
                    <div class="p-5">
                        <div class="animate-pulse">
                            <div class="h-5 bg-gray-200 dark:bg-gray-700 disco:bg-yellow-300 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-gray-200 dark:bg-gray-700 disco:bg-yellow-300 rounded w-1/2 mb-4"></div>
                            <div class="h-8 bg-gray-200 dark:bg-gray-700 disco:bg-yellow-300 rounded mt-4"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-red-50 dark:bg-red-900/20 disco:bg-pink-600 rounded-lg border border-red-300 dark:border-red-800 disco:border-yellow-400">
            <p class="text-red-700 dark:text-red-400 disco:text-white font-medium">{error}</p>
        </div>
    {:else if dogs.length === 0}
        <!-- no dogs found -->
        <div class="text-center py-12 bg-blue-50 dark:bg-blue-900/20 disco:bg-cyan-500/20 rounded-lg border border-blue-300 dark:border-blue-800 disco:border-cyan-400">
            <p class="text-gray-600 dark:text-gray-300 disco:text-white">No dogs available at the moment. Check back soon!</p>
        </div>
    {:else}
        <!-- dog list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each dogs as dog (dog.id)}
                <a 
                    href={`/dog/${dog.id}`} 
                    class="group block bg-white dark:bg-[#161b22] disco:bg-gradient-to-br disco:from-pink-500 disco:to-purple-600 rounded-lg overflow-hidden border border-gray-300 dark:border-gray-700 disco:border-yellow-400 hover:border-gray-400 dark:hover:border-gray-600 disco:hover:border-cyan-300 hover:shadow-md disco:shadow-2xl disco:shadow-pink-500/50 transition-all duration-200"
                >
                    <div class="p-5">
                        <div class="flex items-start justify-between mb-3">
                            <div class="flex-1">
                                <h3 class="text-xl font-semibold text-[#0969da] dark:text-[#58a6ff] disco:text-yellow-300 disco:animate-pulse mb-1 group-hover:underline">{dog.name}</h3>
                                <p class="text-gray-600 dark:text-gray-300 disco:text-white text-sm">{dog.breed}</p>
                            </div>
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400 disco:text-cyan-300 group-hover:text-gray-700 dark:group-hover:text-gray-300 disco:group-hover:text-yellow-300 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                            </svg>
                        </div>
                        <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 disco:border-yellow-400">
                            <span class="text-sm text-gray-500 dark:text-gray-400 disco:text-cyan-300 font-medium">View details →</span>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>
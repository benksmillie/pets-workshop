<script lang="ts">
    import { onMount } from "svelte";
    
    interface Dog {
        id: number;
        name: string;
        breed: string;
        age: number;
        description: string;
        gender: string;
        status: 'AVAILABLE' | 'PENDING' | 'ADOPTED';
    };

    // Accept either a dog object or a dogId
    export let dog: Dog | undefined = undefined;
    export let dogId = 0;
    
    let loading = true;
    let error: string | null = null;
    let dogData: Dog | null = null;
    
    onMount(async () => {
        // If dog object is provided directly, use it
        if (dog) {
            dogData = dog;
            loading = false;
            return;
        }
        
        // Otherwise fetch data using dogId
        if (dogId) {
            try {
                const response = await fetch(`/api/dogs/${dogId}`);
                if (response.ok) {
                    dogData = await response.json();
                } else {
                    error = `Failed to fetch dog: ${response.status} ${response.statusText}`;
                }
            } catch (err) {
                error = `Error: ${err instanceof Error ? err.message : String(err)}`;
            } finally {
                loading = false;
            }
        } else {
            error = "No dog ID provided";
            loading = false;
        }
    });
</script>

{#if loading}
    <div class="animate-pulse bg-white dark:bg-[#161b22] disco:bg-gradient-to-br disco:from-pink-500 disco:to-purple-600 rounded-lg border border-gray-300 dark:border-gray-700 disco:border-yellow-400 disco:shadow-2xl disco:shadow-pink-500/50 p-8">
        <div class="h-8 bg-gray-200 dark:bg-gray-700 disco:bg-yellow-300 rounded w-1/2 mb-6"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 disco:bg-yellow-300 rounded w-3/4 mb-3"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 disco:bg-yellow-300 rounded w-1/2 mb-3"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 disco:bg-yellow-300 rounded w-full mb-3"></div>
    </div>
{:else if error}
    <div class="bg-red-50 dark:bg-red-900/20 disco:bg-pink-600 border border-red-400 dark:border-red-800 disco:border-yellow-400 text-red-800 dark:text-red-400 disco:text-white rounded-lg p-6">
        <p class="font-medium">{error}</p>
    </div>
{:else if dogData}
    <div class="bg-white dark:bg-[#161b22] disco:bg-gradient-to-br disco:from-pink-500 disco:to-purple-600 disco:shadow-2xl disco:shadow-pink-500/50 rounded-lg overflow-hidden border border-gray-300 dark:border-gray-700 disco:border-yellow-400">
        <div class="bg-gray-50 dark:bg-[#0d1117] disco:bg-purple-700 border-b border-gray-300 dark:border-gray-700 disco:border-yellow-400 p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
                <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-gray-100 disco:text-yellow-300 disco:animate-pulse">{dogData.name}</h1>
                {#if dogData.status === 'AVAILABLE'}
                    <span class="inline-flex items-center bg-[#1f883d] dark:bg-[#238636] disco:bg-cyan-400 text-white disco:text-gray-900 text-sm font-medium px-3 py-1 rounded-full self-start">Available</span>
                {:else if dogData.status === 'PENDING'}
                    <span class="inline-flex items-center bg-[#bf8700] dark:bg-[#9e6a03] disco:bg-yellow-400 text-white disco:text-gray-900 text-sm font-medium px-3 py-1 rounded-full self-start">Pending Adoption</span>
                {:else}
                    <span class="inline-flex items-center bg-gray-500 dark:bg-gray-600 disco:bg-gray-400 text-white disco:text-gray-900 text-sm font-medium px-3 py-1 rounded-full self-start">Adopted</span>
                {/if}
            </div>
        </div>
        
        <div class="p-6 sm:p-8">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8 pb-8 border-b border-gray-200 dark:border-gray-700 disco:border-yellow-400">
                <div>
                    <p class="text-sm text-gray-500 dark:text-gray-400 disco:text-cyan-300 font-medium mb-1">Breed</p>
                    <p class="text-base text-gray-900 dark:text-gray-100 disco:text-white font-semibold">{dogData.breed}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500 dark:text-gray-400 disco:text-cyan-300 font-medium mb-1">Age</p>
                    <p class="text-base text-gray-900 dark:text-gray-100 disco:text-white font-semibold">{dogData.age} {dogData.age === 1 ? 'year' : 'years'}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500 dark:text-gray-400 disco:text-cyan-300 font-medium mb-1">Gender</p>
                    <p class="text-base text-gray-900 dark:text-gray-100 disco:text-white font-semibold">{dogData.gender}</p>
                </div>
            </div>
            
            <div class="mb-8">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 disco:text-yellow-300 mb-3">About {dogData.name}</h2>
                <p class="text-gray-600 dark:text-gray-300 disco:text-white text-base leading-relaxed">{dogData.description}</p>
            </div>
            
            {#if dogData.status === 'AVAILABLE'}
                <div class="bg-blue-50 dark:bg-blue-900/20 disco:bg-cyan-500/20 border border-blue-400 dark:border-blue-800 disco:border-cyan-400 rounded-lg p-5">
                    <div class="flex items-start gap-3">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#0969da] dark:text-[#58a6ff] disco:text-cyan-300 disco:animate-pulse flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div class="flex-1">
                            <h3 class="text-base font-semibold text-gray-900 dark:text-gray-100 disco:text-white mb-2">Interested in adopting {dogData.name}?</h3>
                            <p class="text-sm text-gray-600 dark:text-gray-300 disco:text-white mb-4">Contact us today to arrange a meet and greet. Every dog deserves a loving home.</p>
                            <button class="px-4 py-2 bg-[#2da44e] hover:bg-[#2c974b] disco:bg-pink-600 disco:hover:bg-pink-700 text-white font-medium rounded-md text-sm transition-colors duration-200">
                                Start Adoption Process
                            </button>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    </div>
{:else}
    <div class="bg-white dark:bg-[#161b22] disco:bg-gradient-to-br disco:from-pink-500 disco:to-purple-600 rounded-lg border border-gray-300 dark:border-gray-700 disco:border-yellow-400 p-8 text-center">
        <p class="text-gray-600 dark:text-gray-400 disco:text-white">No dog information available</p>
    </div>
{/if}